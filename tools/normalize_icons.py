"""
tools/normalize_icons.py — SVG icon normalizer for VisualThemeFoundry.

Purpose:
    Port of _docs/normalize-icons-200.ps1 to Python stdlib (zero external deps).
    Reads source SVG files and produces three stroke-weight variants at 200×200 px.

Weight runs and stroke-width values (matching the PowerShell original):
    light  — stroke-width  7  (~0.7 px at 20 px display, visual weight ~200)
    normal — stroke-width 10  (~1.0 px at 20 px display, visual weight ~300–400)
    medium — stroke-width 13  (~1.3 px at 20 px display, visual weight ~500)

Outline detection (same heuristic as PS script):
    An SVG is treated as an outline icon when any of the following are true:
      1. The filename contains "outline" (case-insensitive).
      2. Any element inside the SVG carries an explicit stroke attribute (value ≠ "none").
      3. The root <svg> element itself carries a non-"none" stroke attribute.
    Outline icons receive stroke-width replaced by the run value and the weight
    suffix appended before the .svg extension (e.g. home-outline.svg →
    home-outline-light.svg / -normal.svg / -medium.svg).
    Filled icons are written once per weight folder unchanged (stroke-width
    replacement has no visible effect on them).

Output layout:
    icons/normalized/light/   — all icons, outline variants carry -light suffix
    icons/normalized/normal/  — all icons, outline variants carry -normal suffix
    icons/normalized/medium/  — all icons, outline variants carry -medium suffix

Collision handling:
    If two source files would produce the same output filename, the second one
    gets a -dup suffix (or -dup-2, -dup-3, ...).

Transform strategy:
    Source viewBox is scaled to fit inside 200×200 preserving aspect ratio.
    All children are wrapped in a <g transform="translate(tx ty) scale(s)"> so
    the icon occupies the full canvas uniformly.

Namespace handling:
    SVG files may or may not declare the SVG namespace on the root element.
    Both bare-tag and namespaced-tag files are handled.  On output, the SVG
    namespace is registered as the default namespace so output remains clean.

Usage (standalone):
    python tools/normalize_icons.py
    python tools/normalize_icons.py --source icons --output icons/normalized
    python tools/normalize_icons.py --source path/to/svgs --output path/to/out

Usage (imported by server for on-demand normalization):
    from tools.normalize_icons import normalize_svg_content, WEIGHT_RUNS

    for weight, stroke_w in WEIGHT_RUNS:
        normalized_xml = normalize_svg_content(svg_text, base_name, weight, stroke_w)

Internal API:
    normalize_svg_content(svg_text, base_name, weight_label, stroke_width)
        → str | None   — normalized SVG XML string, or None on parse failure

    normalize_directory(source_root, output_root)
        → dict[str, list[str]]  — {weight: [output_file_names]}

Constants:
    WEIGHT_RUNS  — list of (weight_label: str, stroke_width: int) tuples
    SVG_NS       — "http://www.w3.org/2000/svg"
    TARGET_SIZE  — 200.0  (canvas dimension in px)

Logging levels:
    INFO    — per-weight summary (processed / outline / renamed counts)
    DEBUG   — per-file decisions (outline detection, collision renaming)

Internal variable DEFAULT_VERBOSE controls log level when run standalone.
Set to 1 for debug output, 0 for info-only.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

# ── Module-level toggles (override via CLI --verbose at runtime) ───────────
DEFAULT_VERBOSE = 0

LOGGER = logging.getLogger(__name__)

SVG_NS = "http://www.w3.org/2000/svg"
SVG_TAG_PREFIX = f"{{{SVG_NS}}}"

TARGET_SIZE = 200.0

WEIGHT_RUNS: list[tuple[str, int]] = [
    ("light",  7),
    ("normal", 10),
    ("medium", 13),
]

NOISE_ATTR_PATTERNS = re.compile(
    r"^(\{http://www\.inkscape\.org/namespaces/inkscape\}"
    r"|\{http://sodipodi\.sourceforge\.net/DTD/sodipodi-0\.0\.dtd\}"
    r"|\{http://www\.w3\.org/2000/svg\}id"
    r"|id$)",
)

SHAPE_TAGS = {
    "path", "circle", "ellipse", "line",
    "polyline", "polygon", "rect",
}


# ── Namespace registration ─────────────────────────────────────────────────
ET.register_namespace("",      SVG_NS)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


# ── Internal helpers ───────────────────────────────────────────────────────

def _local(tag: str) -> str:
    """
    Strip namespace prefix from an ElementTree tag string.

    Args:
        tag: Raw tag like "{http://www.w3.org/2000/svg}path" or "path".

    Returns:
        Local name string, e.g. "path".

    Example:
        _local("{http://www.w3.org/2000/svg}path")
        # → "path"
    """
    return tag.split("}")[-1] if "}" in tag else tag


def _get_viewbox(root: ET.Element) -> tuple[float, float, float, float]:
    """
    Extract viewBox as (min_x, min_y, width, height) from an SVG root element.
    Falls back to width/height attributes, then to (0, 0, 24, 24).

    Args:
        root: Root <svg> ElementTree element.

    Returns:
        Four-tuple of floats: (min_x, min_y, vb_width, vb_height).

    Example:
        _get_viewbox(root)
        # → (0.0, 0.0, 24.0, 24.0)
    """
    vb = root.get("viewBox") or root.get("viewbox") or ""
    if vb:
        parts = re.split(r"[,\s]+", vb.strip())
        nums = []
        for p in parts:
            try:
                nums.append(float(p))
            except ValueError:
                pass
        if len(nums) == 4 and nums[2] > 0 and nums[3] > 0:
            return (nums[0], nums[1], nums[2], nums[3])

    for attr in ("width", "height"):
        val = root.get(attr, "")
        m = re.search(r"[-+]?\d*\.?\d+", val)
        if not m:
            break
    else:
        try:
            w = float(re.search(r"[-+]?\d*\.?\d+", root.get("width", "0")).group())  # type: ignore[union-attr]
            h = float(re.search(r"[-+]?\d*\.?\d+", root.get("height", "0")).group())  # type: ignore[union-attr]
            if w > 0 and h > 0:
                return (0.0, 0.0, w, h)
        except (AttributeError, ValueError):
            pass

    return (0.0, 0.0, 24.0, 24.0)


def _remove_noise_attrs(element: ET.Element) -> None:
    """
    Recursively remove inkscape/sodipodi namespace attributes and bare 'id'
    from an element and all its descendants.

    Args:
        element: ElementTree element to clean in-place.

    Returns:
        None.

    Example:
        _remove_noise_attrs(root)
    """
    to_remove = [
        k for k in list(element.attrib)
        if k == "id"
        or k.startswith("{http://www.inkscape.org")
        or k.startswith("{http://sodipodi.sourceforge")
    ]
    for k in to_remove:
        del element.attrib[k]
    for child in element:
        _remove_noise_attrs(child)


def _remove_metadata(element: ET.Element) -> None:
    """
    Recursively remove <metadata>, <title>, <desc>, and XML comments from an
    element tree.  Comment nodes in ElementTree are ET.Comment elements.

    Args:
        element: ElementTree element to prune in-place.

    Returns:
        None.

    Example:
        _remove_metadata(root)
    """
    for child in list(element):
        local = _local(child.tag)
        if local in ("metadata", "title", "desc") or callable(child.tag):
            element.remove(child)
        else:
            _remove_metadata(child)


def _iter_elements(element: ET.Element):
    """
    Yield element and all descendants (recursive depth-first).

    Args:
        element: Root element to iterate.

    Returns:
        Generator of ET.Element.

    Example:
        for el in _iter_elements(root): ...
    """
    yield element
    for child in element:
        yield from _iter_elements(child)


def _has_explicit_stroke(root: ET.Element) -> bool:
    """
    Return True if any element in the tree carries a non-"none" stroke attribute.

    Args:
        root: Root SVG element.

    Returns:
        True when a non-"none" stroke attribute exists anywhere in the tree.

    Example:
        _has_explicit_stroke(root)
        # → True
    """
    for el in _iter_elements(root):
        stroke = el.get("stroke", "")
        if stroke and stroke.lower() != "none":
            return True
    return False


def _is_outline(root: ET.Element, base_name_lower: str) -> bool:
    """
    Determine if an SVG should be treated as an outline (stroke-based) icon.
    Mirrors the PS script heuristic:
      1. Filename contains "outline".
      2. Any element has an explicit non-"none" stroke.
      3. Root <svg> has a non-"none" stroke attribute.

    Args:
        root: Parsed SVG root element.
        base_name_lower: Lowercase base filename (no extension).

    Returns:
        True when the icon is an outline variant.

    Example:
        _is_outline(root, "home-outline-01")
        # → True
    """
    if "outline" in base_name_lower:
        return True
    root_stroke = root.get("stroke", "")
    if root_stroke and root_stroke.lower() != "none":
        return True
    return _has_explicit_stroke(root)


def _apply_stroke_width(root: ET.Element, stroke_width: int) -> None:
    """
    Replace all stroke-width attributes across the tree with the given value
    and set vector-effect="non-scaling-stroke" on each stroked element.
    If the root carries the stroke but child shapes do not, the stroke and
    stroke-linecap/linejoin attributes are pushed down to child shapes first
    (mirrors PS root-stroke propagation logic).

    Args:
        root: SVG root element.
        stroke_width: Integer stroke-width to apply.

    Returns:
        None.

    Example:
        _apply_stroke_width(root, 10)
    """
    sw_str = str(stroke_width)

    # Remove all existing stroke-width and vector-effect from every element
    for el in _iter_elements(root):
        el.attrib.pop("stroke-width", None)
        el.attrib.pop("vector-effect", None)

    # Find elements that have an explicit stroke
    stroked = [
        el for el in _iter_elements(root)
        if el.get("stroke", "").lower() not in ("", "none")
    ]

    # Root-only stroke: propagate to child shapes
    root_stroke = root.get("stroke", "")
    if not stroked and root_stroke and root_stroke.lower() != "none":
        for el in _iter_elements(root):
            local = _local(el.tag)
            if local in SHAPE_TAGS:
                if "stroke" not in el.attrib:
                    el.set("stroke", root_stroke)
                for prop in ("stroke-linecap", "stroke-linejoin"):
                    if prop in root.attrib and prop not in el.attrib:
                        el.set(prop, root.get(prop))
                if "fill" in root.attrib and "fill" not in el.attrib:
                    el.set("fill", root.get("fill"))
        stroked = [
            el for el in _iter_elements(root)
            if el.get("stroke", "").lower() not in ("", "none")
        ]

    for el in stroked:
        el.set("stroke-width", sw_str)
        el.set("vector-effect", "non-scaling-stroke")


def normalize_svg_content(
    svg_text: str,
    base_name: str,
    weight_label: str,
    stroke_width: int,
) -> str | None:
    """
    Parse, clean, and normalize one SVG string to 200×200 canvas.

    Steps:
      1. Parse XML. Fails gracefully → returns None.
      2. Remove metadata nodes and noise attributes.
      3. Extract viewBox; compute scale + translate to fit 200×200.
      4. Wrap all children in a <g transform="translate(tx ty) scale(s)">.
      5. Set root viewBox="0 0 200 200" width="200" height="200".
      6. Detect outline; apply stroke-width if outline.
      7. Serialize to UTF-8 XML string (no XML declaration).

    Args:
        svg_text: Raw SVG file content as a string.
        base_name: Source file base name (no extension), used for outline detection.
        weight_label: One of "light", "normal", "medium" (informational only here).
        stroke_width: Integer stroke-width to apply to outline elements.

    Returns:
        Normalized SVG XML string, or None if the input cannot be parsed.

    Example:
        xml = normalize_svg_content(Path("home.svg").read_text(), "home", "normal", 10)
    """
    # Suppress namespace warnings from ET parser
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        LOGGER.debug("XML parse failure for %s: %s", base_name, exc)
        return None

    if _local(root.tag) != "svg":
        LOGGER.debug("Root tag is not <svg> for %s — skipping", base_name)
        return None

    _remove_metadata(root)
    _remove_noise_attrs(root)

    min_x, min_y, vb_w, vb_h = _get_viewbox(root)
    if vb_w <= 0 or vb_h <= 0:
        min_x, min_y, vb_w, vb_h = 0.0, 0.0, 24.0, 24.0

    scale = min(TARGET_SIZE / vb_w, TARGET_SIZE / vb_h)
    tx = (-min_x * scale) + ((TARGET_SIZE - vb_w * scale) / 2.0)
    ty = (-min_y * scale) + ((TARGET_SIZE - vb_h * scale) / 2.0)

    # Build transform group wrapping all movable children
    ns = root.tag.split("}")[0].lstrip("{") if "}" in root.tag else ""
    g_tag = f"{{{ns}}}g" if ns else "g"
    g = ET.Element(g_tag)
    g.set(
        "transform",
        f"translate({tx:.6f} {ty:.6f}) scale({scale:.6f})",
    )

    children = list(root)
    for child in children:
        local = _local(child.tag)
        if local in ("title", "desc"):
            continue
        root.remove(child)
        g.append(child)
    root.append(g)

    # Rewrite root dimensions
    for attr in ("width", "height", "viewBox", "viewbox"):
        root.attrib.pop(attr, None)
    root.set("viewBox", "0 0 200 200")
    root.set("width", "200")
    root.set("height", "200")

    # Stroke normalization
    base_lower = base_name.lower()
    if _is_outline(root, base_lower):
        _apply_stroke_width(root, stroke_width)

    return ET.tostring(root, encoding="unicode", xml_declaration=False)


def normalize_directory(
    source_root: Path,
    output_root: Path,
) -> dict[str, list[str]]:
    """
    Normalize all SVG files under source_root into three weight subfolders
    under output_root.

    Scans source_root recursively for *.svg files, excluding any path that
    already contains "normalized" (avoids re-processing output).

    Args:
        source_root: Directory containing source SVG files (recursive scan).
        output_root: Root for normalized output; weight subfolders created here.

    Returns:
        Dict mapping weight label → list of output file names written.

    Example:
        result = normalize_directory(Path("icons"), Path("icons/normalized"))
        # → {"light": ["home-outline-light.svg", ...], "normal": [...], "medium": [...]}
    """
    svg_files = sorted(
        p for p in source_root.rglob("*.svg")
        if "normalized" not in p.as_posix().lower()
    )
    total = len(svg_files)
    LOGGER.info("Found %d source SVG files under %s", total, source_root)

    results: dict[str, list[str]] = {}

    for weight_label, stroke_width in WEIGHT_RUNS:
        target_dir = output_root / weight_label
        target_dir.mkdir(parents=True, exist_ok=True)

        used_names: dict[str, bool] = {}
        written: list[str] = []
        outline_count = 0
        rename_count = 0

        for svg_path in svg_files:
            svg_text = svg_path.read_text(encoding="utf-8", errors="replace")
            base = svg_path.stem
            base_lower = base.lower()

            normalized = normalize_svg_content(svg_text, base, weight_label, stroke_width)
            if normalized is None:
                continue

            # Determine whether this was treated as outline
            try:
                root_check = ET.fromstring(svg_text)
                is_ol = _is_outline(root_check, base_lower)
            except ET.ParseError:
                is_ol = "outline" in base_lower

            if is_ol:
                outline_count += 1
                candidate = f"{base}-{weight_label}.svg"
            else:
                candidate = f"{base}.svg"

            candidate_key = candidate.lower()
            if candidate_key in used_names:
                rename_count += 1
                n = 1
                while True:
                    tag = f"-dup" if n == 1 else f"-dup-{n}"
                    if is_ol:
                        candidate = f"{base}{tag}-{weight_label}.svg"
                    else:
                        candidate = f"{base}{tag}.svg"
                    candidate_key = candidate.lower()
                    if candidate_key not in used_names:
                        break
                    n += 1
                LOGGER.debug("Collision → renamed to %s", candidate)

            used_names[candidate_key] = True
            (target_dir / candidate).write_text(normalized, encoding="utf-8")
            written.append(candidate)

        LOGGER.info(
            "[%s] Written: %d/%d  | Outline (stroke-width %d): %d | Renamed: %d",
            weight_label, len(written), total, stroke_width, outline_count, rename_count,
        )
        results[weight_label] = written

    return results


def _parse_args() -> argparse.Namespace:
    """
    Parse CLI arguments for standalone execution.

    Returns:
        Parsed argparse namespace with source, output, verbose fields.

    Example:
        args = _parse_args()
    """
    parser = argparse.ArgumentParser(
        description="Normalize SVG icons to 200×200 in three stroke-weight variants."
    )
    parser.add_argument(
        "--source",
        default=str(Path(__file__).resolve().parent.parent / "icons"),
        help="Source directory containing SVG files (recursive). Default: icons/",
    )
    parser.add_argument(
        "--output",
        default=str(Path(__file__).resolve().parent.parent / "icons" / "normalized"),
        help="Output root directory. Weight subfolders created here. Default: icons/normalized/",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable DEBUG logging."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    log_level = logging.DEBUG if (args.verbose or DEFAULT_VERBOSE) else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stdout,
    )

    source = Path(args.source).resolve()
    output = Path(args.output).resolve()

    if not source.is_dir():
        LOGGER.error("Source directory not found: %s", source)
        sys.exit(1)

    LOGGER.info("Source: %s", source)
    LOGGER.info("Output: %s", output)

    normalize_directory(source, output)
    LOGGER.info("Done.")