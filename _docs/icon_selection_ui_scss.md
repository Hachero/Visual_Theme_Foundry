# Icon Selection UI: Main-Primary SCSS Pre-Flight

Generated: 2026-04-02

## Purpose

This document defines the SCSS-facing structure and semantic naming for an application UI section that lists Main-Primary icon roles and allows a user to select icon variants from the normalized icon sets.

This is a pre-flight spec, not implementation code. The goal is to make the intended structure obvious before wiring HTML, JS, or final theme tokens.

## Scope

This document covers only the Main-Primary icon group:

- Home
- Search
- Menu
- Close
- Add
- Edit
- Delete/Remove
- Save
- Settings
- User/Profile
- People/Team
- Notifications/Alerts
- Message/Chat
- Calendar/Schedule
- File/Document
- Folder
- Upload/Download
- Share

## Organizational Assumption

The application-facing icon inventory should be treated as the normalized icon sets only:

- icons/normalized/light/
- icons/normalized/normal/
- icons/normalized/medium/

Original source SVGs are reference assets only and should live outside the app-facing icon folder tree under:

- \_references/icons-original/

Design intent: app code should target normalized icons only. Original SVGs remain available for audit, tracing, and rebuild work, but are not part of the runtime-facing selection surface.

## UI Goal

The UI should present each Main-Primary role as a row or card with:

1. Role label
2. Role description
3. Semantic color guidance
4. A variant selector dropdown
5. A live preview area showing the selected icon in relevant states

Example mental model:

- Role: Home
- Default semantic role: navigation destination
- Recommended default token: on-surface-variant
- Recommended active token: primary
- Variant dropdown: home-outline, home-outline-01, home-01, home-02

## Semantic SCSS Naming Strategy

Use role-first naming, not file-name-first naming.

The UI should be styled around semantic application roles rather than raw icon filenames.

Recommended naming layers:

1. Section/layout selectors
2. Role-list selectors
3. Role-item selectors
4. Preview/state selectors
5. Variant-control selectors
6. Token/modifier selectors

## Suggested DOM Structure

```html
<section class="icon-role-browser icon-role-browser--main-primary">
	<header class="icon-role-browser__header">
		<h2 class="icon-role-browser__title">Main-Primary Icons</h2>
		<p class="icon-role-browser__intro">
			Choose a normalized icon variant per core app role.
		</p>
	</header>

	<div class="icon-role-list">
		<article class="icon-role-card icon-role-card--nav" data-role="home">
			<div class="icon-role-card__meta">
				<h3 class="icon-role-card__title">Home</h3>
				<p class="icon-role-card__description">
					Primary navigation destination.
				</p>
			</div>

			<div class="icon-role-card__preview-group">
				<div class="icon-preview icon-preview--default"></div>
				<div class="icon-preview icon-preview--active"></div>
			</div>

			<label class="icon-role-card__field-label" for="icon-role-home"
				>Variant</label
			>
			<select class="icon-role-card__select" id="icon-role-home"></select>
		</article>
	</div>
</section>
```

## Core Section Selectors

These selectors define structure, spacing, and grouping.

```scss
.icon-role-browser {
}
.icon-role-browser--main-primary {
}
.icon-role-browser__header {
}
.icon-role-browser__title {
}
.icon-role-browser__intro {
}

.icon-role-list {
}
.icon-role-card {
}
.icon-role-card__meta {
}
.icon-role-card__title {
}
.icon-role-card__description {
}
.icon-role-card__preview-group {
}
.icon-role-card__field-label {
}
.icon-role-card__select {
}
```

## Role-Family Modifiers

These modifiers let the UI distinguish broad role families without tying layout to a specific icon file.

```scss
.icon-role-card--nav {
}
.icon-role-card--utility {
}
.icon-role-card--action {
}
.icon-role-card--object {
}
.icon-role-card--status-entry {
}
.icon-role-card--communication {
}
```

Recommended mapping for Main-Primary:

| Role                 | Card Modifier                   |
| -------------------- | ------------------------------- |
| Home                 | `icon-role-card--nav`           |
| Search               | `icon-role-card--utility`       |
| Menu                 | `icon-role-card--utility`       |
| Close                | `icon-role-card--utility`       |
| Add                  | `icon-role-card--action`        |
| Edit                 | `icon-role-card--action`        |
| Delete/Remove        | `icon-role-card--action`        |
| Save                 | `icon-role-card--action`        |
| Settings             | `icon-role-card--nav`           |
| User/Profile         | `icon-role-card--object`        |
| People/Team          | `icon-role-card--object`        |
| Notifications/Alerts | `icon-role-card--status-entry`  |
| Message/Chat         | `icon-role-card--communication` |
| Calendar/Schedule    | `icon-role-card--object`        |
| File/Document        | `icon-role-card--object`        |
| Folder               | `icon-role-card--object`        |
| Upload/Download      | `icon-role-card--action`        |
| Share                | `icon-role-card--action`        |

## Preview Selectors

These selectors are for showing semantic state without changing the underlying file inventory.

```scss
.icon-preview {
}
.icon-preview--default {
}
.icon-preview--active {
}
.icon-preview--selected {
}
.icon-preview--disabled {
}
.icon-preview--emphasis-low {
}
.icon-preview--emphasis-high {
}
```

Recommended use:

- `icon-preview--default`: baseline app-state preview
- `icon-preview--active`: selected/current/engaged state preview
- `icon-preview--disabled`: optional muted preview
- `icon-preview--emphasis-low` and `icon-preview--emphasis-high`: optional hierarchy demos

## Material-Inspired Semantic Color Hooks

Do not style icons by filename. Style them by semantic role/state.

Recommended hook classes:

```scss
.icon-tone--default {
}
.icon-tone--muted {
}
.icon-tone--active {
}
.icon-tone--on-filled {
}
.icon-tone--danger {
}
.icon-tone--warning {
}
.icon-tone--success {
}
.icon-tone--info {
}
```

Recommended token mapping:

| Tone Class             | Intended Token                                                     |
| ---------------------- | ------------------------------------------------------------------ |
| `icon-tone--default`   | `on-surface` or `on-surface-variant`                               |
| `icon-tone--muted`     | `on-surface-variant`                                               |
| `icon-tone--active`    | `primary`                                                          |
| `icon-tone--on-filled` | matching `on-*` token for the container                            |
| `icon-tone--danger`    | `error`                                                            |
| `icon-tone--warning`   | `warning` or `error-container` fallback if no warning token exists |
| `icon-tone--success`   | `success` or `primary` fallback if no success token exists         |
| `icon-tone--info`      | `tertiary` or `primary` fallback                                   |

## Main-Primary Semantic Role Map

This table is the contract the UI should expose.

| Main-Primary Role    | Typical App Role                  | Default Tone Class                   | Active Tone Class                               | Notes                                                  |
| -------------------- | --------------------------------- | ------------------------------------ | ----------------------------------------------- | ------------------------------------------------------ |
| Home                 | Navigation destination            | `icon-tone--muted`                   | `icon-tone--active`                             | Selected route should promote clearly                  |
| Search               | Utility action / input affordance | `icon-tone--muted`                   | `icon-tone--active`                             | Search field icon can stay muted until focus           |
| Menu                 | UI chrome toggle                  | `icon-tone--default`                 | `icon-tone--active`                             | Neutral in most app bars                               |
| Close                | Dismiss/cancel                    | `icon-tone--default`                 | `icon-tone--default`                            | Do not use danger unless destructive                   |
| Add                  | Constructive action               | `icon-tone--active` when primary CTA | `icon-tone--on-filled` when button is filled    | Low emphasis variants can fall back to default tone    |
| Edit                 | Secondary action                  | `icon-tone--default`                 | `icon-tone--active`                             | Generic edit should not read as semantic state         |
| Delete/Remove        | Destructive action                | `icon-tone--danger`                  | `icon-tone--on-filled` on destructive container | Explicit semantic exception                            |
| Save                 | Commit/persist action             | `icon-tone--active` when emphasized  | `icon-tone--on-filled` on filled button         | Neutral is acceptable if save is present but secondary |
| Settings             | Preferences/navigation            | `icon-tone--muted`                   | `icon-tone--active`                             | Usually route-level or panel-level navigation          |
| User/Profile         | Identity/account                  | `icon-tone--muted`                   | `icon-tone--active`                             | Avatar fallback icons remain neutral by default        |
| People/Team          | Object/category                   | `icon-tone--default`                 | `icon-tone--active`                             | Category/object icons should stay calm                 |
| Notifications/Alerts | Status entry point                | `icon-tone--muted`                   | `icon-tone--active`                             | Badge carries true semantic signal                     |
| Message/Chat         | Communication                     | `icon-tone--muted`                   | `icon-tone--active`                             | Unread should not require full icon recolor            |
| Calendar/Schedule    | Object/action hybrid              | `icon-tone--default`                 | `icon-tone--active`                             | Neutral by default                                     |
| File/Document        | Object type                       | `icon-tone--default`                 | `icon-tone--active`                             | Avoid random category coloring                         |
| Folder               | Object/container                  | `icon-tone--default`                 | `icon-tone--active`                             | Same as file/document                                  |
| Upload/Download      | Directional action                | `icon-tone--default`                 | `icon-tone--active`                             | Progress needs separate feedback                       |
| Share                | Outbound action                   | `icon-tone--default`                 | `icon-tone--active`                             | Keep neutral in context menus                          |

## Variant Dropdown Contract

The dropdown is a file-selector control, but its labeling should remain semantic and human-readable.

Recommended behavior:

1. Group options by role, not by source pack.
2. Show normalized-compatible variant labels.
3. Store the selected normalized asset path as the actual value.
4. Optionally show the weight family independently from the glyph variant.

Recommended option model:

```text
Label: Home / Outline 01
Value: icons/normalized/light/home-outline-01-light.svg
```

Better long-term model:

1. Variant dropdown selects glyph family: `home-outline-01`
2. Weight control selects weight family: `light | normal | medium`
3. Final asset path is composed from both

That structure prevents duplicating essentially identical dropdown choices three times.

## Suggested Control Selectors

```scss
.icon-variant-control {
}
.icon-variant-control__label {
}
.icon-variant-control__select {
}
.icon-weight-control {
}
.icon-weight-control__label {
}
.icon-weight-control__select {
}
```

Recommended control split:

- Variant control = selects glyph family
- Weight control = selects light/normal/medium

## Suggested State/Data Hooks

Prefer state/data hooks for JS rather than styling directly off filenames.

```html
<article
	class="icon-role-card icon-role-card--nav"
	data-role="home"
	data-tone="muted"
	data-variant="home-outline-01"
	data-weight="light"
></article>
```

Useful hooks:

- `data-role`
- `data-role-family`
- `data-variant`
- `data-weight`
- `data-tone`
- `data-selected`

## SCSS Responsibility Boundaries

SCSS should own:

1. Layout
2. Spacing
3. Typography
4. Tone/state styling
5. Preview framing
6. Control affordances

SCSS should not own:

1. Variant inventory generation
2. Role-to-file matching logic
3. JSON/icon metadata parsing
4. Selection persistence logic

Those belong in data preparation and UI behavior code.

## Recommended First Implementation Order

1. Build the semantic HTML shell using the selectors in this document.
2. Hardcode 2 or 3 Main-Primary roles first: Home, Search, Save.
3. Add preview states: default + active.
4. Add variant dropdown.
5. Add separate weight control.
6. Then wire the rest of the Main-Primary roles.

## Summary

The key idea is simple:

- filenames identify assets
- role names identify UI meaning
- SCSS selectors should express UI meaning
- semantic tone classes should express palette behavior
- weight and variant should be separate controls whenever possible

If the UI follows that split, the icon picker remains understandable even as the icon inventory grows.
