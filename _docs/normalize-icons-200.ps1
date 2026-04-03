Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Normalization runs: produces three weight variants of outline icons.
#   light  — stroke-width  7  (~0.7px at 20px, visual weight ~200)
#   normal — stroke-width 10  (~1.0px at 20px, visual weight ~300-400)
#   medium — stroke-width 13  (~1.3px at 20px, visual weight ~500)
#
# Filled (non-outline) icons are written once to each weight subfolder
# unchanged (stroke-width setting has no effect on them).
# Outline icons receive a weight suffix appended before the .svg extension:
#   e.g.  home-outline.svg  →  home-outline-light.svg  /  -normal.svg  /  -medium.svg

$sourceRoot = Join-Path $PSScriptRoot '..\icons'
$sourceRoot = [System.IO.Path]::GetFullPath($sourceRoot)
$normalizedRoot = Join-Path $sourceRoot 'normalized'

$runs = @(
    @{ Weight = 'light';  StrokeWidth = '7'  },
    @{ Weight = 'normal'; StrokeWidth = '10' },
    @{ Weight = 'medium'; StrokeWidth = '13' }
)

function Get-ViewBoxParts {
    param([System.Xml.XmlElement]$svg)

    $vb = $svg.GetAttribute('viewBox')
    if ($vb) {
        $parts = ($vb -split '[,\s]+' | Where-Object { $_ -ne '' })
        if ($parts.Count -eq 4) {
            return @([double]$parts[0], [double]$parts[1], [double]$parts[2], [double]$parts[3])
        }
    }

    $w = $svg.GetAttribute('width')
    $h = $svg.GetAttribute('height')
    if ($w -and $h) {
        $wNum = [regex]::Match($w, '[-+]?[0-9]*\.?[0-9]+').Value
        $hNum = [regex]::Match($h, '[-+]?[0-9]*\.?[0-9]+').Value
        if ($wNum -and $hNum) {
            return @(0.0, 0.0, [double]$wNum, [double]$hNum)
        }
    }

    return @(0.0, 0.0, 24.0, 24.0)
}

function Remove-NoiseAttributes {
    param([System.Xml.XmlNode]$node)

    if ($node.Attributes) {
        $toRemove = @()
        foreach ($a in $node.Attributes) {
            $name = $a.Name
            if ($name -like 'inkscape:*' -or $name -like 'sodipodi:*' -or $name -eq 'xmlns:inkscape' -or $name -eq 'xmlns:sodipodi' -or $name -eq 'id') {
                $toRemove += $name
            }
        }
        foreach ($n in $toRemove) {
            [void]$node.Attributes.RemoveNamedItem($n)
        }
    }

    foreach ($child in @($node.ChildNodes)) {
        Remove-NoiseAttributes -node $child
    }
}

function Remove-MetadataNodes {
    param([System.Xml.XmlNode]$node)

    foreach ($child in @($node.ChildNodes)) {
        if ($child.NodeType -eq [System.Xml.XmlNodeType]::Comment) {
            [void]$node.RemoveChild($child)
            continue
        }
        if ($child.LocalName -eq 'metadata') {
            [void]$node.RemoveChild($child)
            continue
        }
        Remove-MetadataNodes -node $child
    }
}

$files = Get-ChildItem -Path $sourceRoot -Recurse -File -Filter *.svg | Where-Object { $_.FullName -notmatch '\\normalized\\' }
$total = $files.Count

foreach ($run in $runs) {
    $weightSuffix = $run.Weight
    $strokeWidth  = $run.StrokeWidth
    $targetRoot   = Join-Path $normalizedRoot $weightSuffix

    if (-not (Test-Path $targetRoot)) {
        New-Item -ItemType Directory -Path $targetRoot | Out-Null
    }

    $processed    = 0
    $outlineCount = 0
    $renameCount  = 0
    $usedOutputNames = @{}

    foreach ($file in $files) {
        $doc = New-Object System.Xml.XmlDocument
        $doc.PreserveWhitespace = $false
        $doc.Load($file.FullName)

        $svg = $doc.DocumentElement
        if (-not $svg -or $svg.LocalName -ne 'svg') {
            continue
        }

        Remove-MetadataNodes -node $svg
        Remove-NoiseAttributes -node $svg

        $vb = Get-ViewBoxParts -svg $svg
        $minX = $vb[0]
        $minY = $vb[1]
        $vbW  = $vb[2]
        $vbH  = $vb[3]

        if ($vbW -le 0 -or $vbH -le 0) {
            $vbW  = 24.0
            $vbH  = 24.0
            $minX = 0.0
            $minY = 0.0
        }

        $scale = [Math]::Min(200.0 / $vbW, 200.0 / $vbH)
        $tx = (-$minX * $scale) + ((200.0 - ($vbW * $scale)) / 2.0)
        $ty = (-$minY * $scale) + ((200.0 - ($vbH * $scale)) / 2.0)

        [void]$svg.RemoveAttribute('width')
        [void]$svg.RemoveAttribute('height')
        $svg.SetAttribute('viewBox', '0 0 200 200')
        $svg.SetAttribute('width', '200')
        $svg.SetAttribute('height', '200')

        $ns = $svg.NamespaceURI
        $g  = if ([string]::IsNullOrWhiteSpace($ns)) { $doc.CreateElement('g') } else { $doc.CreateElement('g', $ns) }
        $txS = [Math]::Round($tx,    6).ToString([System.Globalization.CultureInfo]::InvariantCulture)
        $tyS = [Math]::Round($ty,    6).ToString([System.Globalization.CultureInfo]::InvariantCulture)
        $scS = [Math]::Round($scale, 6).ToString([System.Globalization.CultureInfo]::InvariantCulture)
        $g.SetAttribute('transform', "translate($txS $tyS) scale($scS)")

        $movable = @()
        foreach ($child in @($svg.ChildNodes)) {
            if ($child.NodeType -eq [System.Xml.XmlNodeType]::Element -and ($child.LocalName -eq 'title' -or $child.LocalName -eq 'desc')) {
                continue
            }
            $movable += $child
        }
        foreach ($m in $movable) {
            [void]$svg.RemoveChild($m)
            [void]$g.AppendChild($m)
        }
        [void]$svg.AppendChild($g)

        $rawName              = $file.Name.ToLowerInvariant()
        $explicitStrokeNodes  = $svg.SelectNodes('//*[@stroke]')
        $hasExplicitStroke    = $false
        foreach ($sn in $explicitStrokeNodes) {
            $sv = $sn.GetAttribute('stroke')
            if ($sv -and $sv -ne 'none') {
                $hasExplicitStroke = $true
                break
            }
        }

        $rootStroke = $svg.GetAttribute('stroke')
        $hasRootStroke = $rootStroke -and $rootStroke -ne 'none'
        $isOutline = $rawName.Contains('outline') -or $hasExplicitStroke -or $hasRootStroke

        if ($isOutline) {
            $outlineCount++

            foreach ($n in $svg.SelectNodes('//*[@stroke-width]')) {
                [void]$n.RemoveAttribute('stroke-width')
            }
            [void]$svg.RemoveAttribute('stroke-width')
            [void]$svg.RemoveAttribute('vector-effect')

            $targetStrokeNodes = @($svg.SelectNodes('//*[@stroke and @stroke != "none"]'))

            # Some outline sources place stroke on root <svg> only.
            if ($targetStrokeNodes.Count -eq 0 -and $hasRootStroke) {
                $targetStrokeNodes = @($svg.SelectNodes('//*[self::path or self::circle or self::ellipse or self::line or self::polyline or self::polygon or self::rect]'))
                foreach ($shape in $targetStrokeNodes) {
                    if (-not $shape.HasAttribute('stroke')) {
                        $shape.SetAttribute('stroke', $rootStroke)
                    }
                    if ($svg.HasAttribute('stroke-linecap') -and -not $shape.HasAttribute('stroke-linecap')) {
                        $shape.SetAttribute('stroke-linecap', $svg.GetAttribute('stroke-linecap'))
                    }
                    if ($svg.HasAttribute('stroke-linejoin') -and -not $shape.HasAttribute('stroke-linejoin')) {
                        $shape.SetAttribute('stroke-linejoin', $svg.GetAttribute('stroke-linejoin'))
                    }
                    if ($svg.HasAttribute('fill') -and -not $shape.HasAttribute('fill')) {
                        $shape.SetAttribute('fill', $svg.GetAttribute('fill'))
                    }
                }
            }

            foreach ($sn in $targetStrokeNodes) {
                $sn.SetAttribute('stroke-width', $strokeWidth)
                $sn.SetAttribute('vector-effect', 'non-scaling-stroke')
            }
        }

        # Flat output per weight folder. Outline icons get weight suffix.
        # If a filename collision occurs, Ionicons files get -ionicons and
        # any further collisions get numeric suffixes.
        $sourceRelative  = $file.FullName.Substring($sourceRoot.Length).TrimStart('\')
        $isFromIonicons  = $sourceRelative -like 'ionicons-svg\*'
        $baseName        = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        $ext             = [System.IO.Path]::GetExtension($file.Name)
        $candidateName   = if ($isOutline) { "$baseName-$weightSuffix$ext" } else { "$baseName$ext" }
        $candidateKey    = $candidateName.ToLowerInvariant()

        if ($usedOutputNames.ContainsKey($candidateKey)) {
            $renameCount++
            $suffixBase = if ($isFromIonicons) { "$baseName-ionicons" } else { "$baseName-dup" }
            $n = 1
            do {
                $indexedBase = if ($n -eq 1) { $suffixBase } else { "$suffixBase-$n" }
                $candidateName = if ($isOutline) { "$indexedBase-$weightSuffix$ext" } else { "$indexedBase$ext" }
                $candidateKey  = $candidateName.ToLowerInvariant()
                $n++
            } while ($usedOutputNames.ContainsKey($candidateKey))
        }

        $usedOutputNames[$candidateKey] = $true
        $outPath = Join-Path $targetRoot $candidateName

        $settings = New-Object System.Xml.XmlWriterSettings
        $settings.Indent              = $true
        $settings.OmitXmlDeclaration  = $true
        $settings.NewLineChars        = "`n"
        $settings.Encoding            = New-Object System.Text.UTF8Encoding($false)

        $writer = [System.Xml.XmlWriter]::Create($outPath, $settings)
        $doc.Save($writer)
        $writer.Close()

        $processed++
    }

    Write-Host ("[{0}] Normalized: {1}/{2}  |  Outline (stroke-width {3}): {4}  |  Renamed: {5}" -f $weightSuffix, $processed, $total, $strokeWidth, $outlineCount, $renameCount)
}

Write-Host ("Output root: {0}" -f $normalizedRoot)
