---
name: LazyList
description: Una colección personal de media sobre arcilla de medianoche
colors:
  midnight: "#0b0a16"
  midnight-deep: "#100e20"
  midnight-dim: "#16132b"
  clay: "#221c3d"
  clay-light: "#2a2348"
  clay-bright: "#362e5c"
  clay-glint: "#403772"
  ink: "#f1effb"
  ink-muted: "#b6aed8"
  ink-faint: "#8b83b0"
  violet: "#8b5cf6"
  violet-deep: "#6d3df0"
  violet-soft: "#c4a8ff"
  rose: "#ec4899"
  blue: "#60a5fa"
  sky: "#38bdf8"
  mint: "#34d399"
  amber: "#fbbf24"
  fuchsia: "#e879f9"
  teal: "#2dd4bf"
typography:
  body:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontWeight: 500
    lineHeight: 1.5
  title:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontWeight: 800
    lineHeight: 1.28
    letterSpacing: "-0.02em"
  label:
    fontFamily: "Inter, ui-sans-serif, system-ui, -apple-system, sans-serif"
    fontWeight: 700
rounded:
  pill: "999px"
  card: "24px"
  clay: "28px"
  button: "18px"
components:
  button-primary:
    backgroundColor: "linear-gradient(180deg, #8b5cf6 0%, #6d3df0 100%)"
    textColor: "#ffffff"
    rounded: "999px"
    padding: "0.7rem 1.35rem"
  button-ghost:
    backgroundColor: "linear-gradient(150deg, #362e5c 0%, #221c3d 55%, #100e20 100%)"
    textColor: "#b6aed8"
    rounded: "18px"
    padding: "0.6rem 0.95rem"
  rail-pill:
    backgroundColor: "linear-gradient(150deg, #362e5c 0%, #221c3d 55%, #100e20 100%)"
    textColor: "#b6aed8"
    rounded: "999px"
    padding: "0.62rem 1.15rem"
  rail-pill-active:
    backgroundColor: "linear-gradient(180deg, #8b5cf6 0%, #6d3df0 100%)"
    textColor: "#ffffff"
    rounded: "999px"
    padding: "0.62rem 1.15rem"
  capture-input:
    backgroundColor: "linear-gradient(150deg, #362e5c 0%, #221c3d 50%, #100e20 100%)"
    textColor: "#f1effb"
    rounded: "999px"
    padding: "0.55rem"
  card:
    backgroundColor: "linear-gradient(150deg, #2a2348 0%, #221c3d 55%, #100e20 100%)"
    textColor: "#f1effb"
    rounded: "24px"
  chip:
    backgroundColor: "rgba(255, 255, 255, 0.06)"
    textColor: "#b6aed8"
    rounded: "999px"
    padding: "0.24rem 0.6rem"
  chip-state:
    textColor: "#38bdf8"
    rounded: "999px"
    padding: "0.26rem 0.62rem"
---

# Design System: LazyList

## Overview

**Creative North Star: "La Colección de Medianoche"**

LazyList is a personal, private media backlog tracker: a midnight-lit vault where everything the owner wants to watch, read, and play sits in soft, inflated clay cards, glowing with violet and rose accents. The interface exists to make cataloging frictionless — one paste or search turns a bare title into a fully enriched, beautifully displayed record — so the collection reads like a curated shelf, not a spreadsheet.

The world is **dark claymorphism**: surfaces are plump, "play-doh" clay chips and cards that float above a deep night background (`#0b0a16`) lit by two faint radial glows — violet top-left, rose top-right. Depth is conveyed through the signature **double shadow**: an outer drop shadow that peels the surface off the background and an inner `inset` highlight along the top edge that gives the clay its pillowed 3D volume. Color is restrained by default and loud only where it means something: violet is the single action color, rose marks adult content, and each of the ten media categories carries its own cover-gradient hue so a category is identifiable at a glance.

**Key Characteristics:**
- Dark, warm clay surfaces over a near-black midnight background with faint violet/rose ambient glows.
- One action color (violet) reserved for primary buttons, active filters, and the brand mark.
- Signature double-shadow elevation on every elevated surface; nothing flat floats.
- A single type family (Inter) across three weights (500/700/800); hierarchy via weight and scale, never display faces.
- Every interactive surface is a pill or rounded clay form (radius ≥ 18px); no sharp corners anywhere.
- Category identity lives in cover gradients; state identity lives in a colored dot chip (pendiente / en curso / terminado).
- Full-pill capture bar is the hero surface: paste a URL or search a picker to save an enriched item in one step.

## Colors

The palette is a midnight base with warm violet-lavender clay neutrals and a small set of high-chroma accents that are always earned. Ink text is cool lavender-white so it reads warm against the clay without ever going gray.

### Primary
- **Violet** (`#8b5cf6`, deep `#6d3df0`): the one action color. Primary buttons, active rail pills, active segmented filters, the brand mark, focus rings, selection. Used on ≤10% of any given screen — its rarity is the point.
- **Violet Soft** (`#c4a8ff`): the "en curso" state and empty-state glyph; a lighter, gentler echo of the action color for status, not actions.

### Secondary
- **Rose** (`#ec4899`): reserved exclusively for adult-content signals — the NSFW badge gradient (`#f472b6` → `#db2777`), the NSFW flag icon, and the películas category cover. Never used for anything else; its meaning depends on that exclusivity.
- **Amber** (`#fbbf24`): the demo-content badge. Signals "this item is sample data," always in a soft `rgba(251,191,36,0.12)` pill.

### Neutral
- **Midnight** (`#0b0a16`): the page background. Deep, near-black violet-navy.
- **Midnight Deep** (`#100e20`): the darkest stop of every clay gradient and card shadow falloff.
- **Midnight Dim** (`#16132b`): secondary dark stops.
- **Clay** (`#221c3d`): the core clay body tone.
- **Clay Light** (`#2a2348`) / **Clay Bright** (`#362e5c`) / **Clay Glint** (`#403772`): progressively lighter gradient stops that model the clay's lit top edge.
- **Ink** (`#f1effb`): primary text, always on clay.
- **Ink Muted** (`#b6aed8`): secondary text, chip labels, inactive controls.
- **Ink Faint** (`#8b83b0`): tertiary text, placeholders, hints, stat lines.

### Named Rules
**The One Action Color Rule.** Violet is the only color that ever means "do this." Every primary button, every active filter, every selected pill is the same violet gradient. If it's interactive and active, it's violet; if it's not, it's clay.

**The Rose-Only-For-NSFW Rule.** Rose is the adult-content color and nothing else. A rose accent anywhere else dilutes the one signal users rely on to keep private content private.

## Typography

**Display/Title Font:** Inter (with ui-sans-serif, system-ui fallback)
**Body Font:** Inter
**Label Font:** Inter

**Character:** A single neutral, highly legible family carries the entire system. No display faces, no italics, no letter-spaced uppercase labels — personality comes from the clay surfaces and the color language, not from typographic decoration. The scale is a fixed rem hierarchy tuned for scanning.

### Hierarchy
- **Brand word** (Inter 800, 1.3rem, -0.02em): the LazyList logotype in the sticky header.
- **Card title** (Inter 700, 1.05rem, 1.28): the media title on each card; truncates to two lines.
- **Empty-state title** (Inter 800, 1.5rem, -0.02em): the one moment a large title appears.
- **Body** (Inter 500, 0.98rem, 1.6): empty-state copy, capped at 34rem (≈ 55–60ch).
- **Label** (Inter 700, 0.72–0.9rem): chips, pills, buttons, stat lines, field labels; no uppercase.

### Named Rules
**The Weight-and-Scale-Only Rule.** Hierarchy is built from Inter's 500/700/800 weights and a fixed rem scale. If a heading needs more presence, increase weight or size — never add a second family, italic, or uppercase treatment.

## Layout

The app is a single column under a sticky header. The header hosts the brand, the capture bar, and settings; the body is a category rail, a filter toolbar, and the card grid. Everything is centered in a `max-width: 88rem` container with `2rem` gutters on desktop.

- **Grid:** `repeat(auto-fill, minmax(15.5rem, 1fr))` with a `1.5rem` gap — cards reflow fluidly as the viewport narrows.
- **Responsive steps:** at `≤ 860px` the header wraps (capture bar drops to its own full-width row, min-width 0 to prevent overflow), gutters shrink to `1.1rem`, and the grid tightens to `minmax(12.5rem, 1fr)`. At `≤ 560px` the grid becomes `minmax(10rem, 1fr)`, the capture category picker hides, and card padding compresses.
- **The rail** scrolls horizontally (scrollbar hidden) so all ten categories stay one swipe away on small screens.
- **Vertical rhythm:** ~0.4rem–1.1rem between header rows; a 1.4rem breathing space under the filter toolbar.

## Elevation & Depth

This system is **explicitly elevated** — depth is the medium. Every interactive and container surface is modeled clay floating over the midnight background, and depth comes from the **double shadow**, not borders or hairlines. There are no flat panels and no 1px strokes holding things together; separation is always volumetric.

### Shadow Vocabulary
- **Clay** (`0 26px 52px -18px rgba(3,2,10,0.9), inset 0 1px 0 rgba(255,255,255,0.11), inset 0 -16px 28px -14px rgba(0,0,0,0.55)`): the hero surface — capture bar, dialogs, toast, empty state.
- **Clay Md** (`0 16px 34px -14px rgba(3,2,10,0.85), inset 0 1px 0 rgba(255,255,255,0.09), inset 0 -12px 20px -10px rgba(0,0,0,0.5)`): default cards and the capture bar.
- **Clay Sm** (`0 8px 18px -8px rgba(3,2,10,0.8), inset 0 1px 0 rgba(255,255,255,0.07), inset 0 -8px 14px -8px rgba(0,0,0,0.45)`): pills, chips, buttons, small controls.
- **Clay Press** (`0 3px 8px -3px rgba(3,2,10,0.8), inset 0 4px 12px rgba(0,0,0,0.6), inset 0 -1px 0 rgba(255,255,255,0.04)`): the active/pressed state — surfaces physically squash down.
- **Violet** (`0 14px 34px -10px rgba(109,61,240,0.55), inset 0 1px 0 rgba(255,255,255,0.25), inset 0 -10px 18px -8px rgba(0,0,0,0.35)`): violet-active surfaces (primary buttons, selected pills) glow with a colored halo.
- **Focus** (`0 0 0 3px rgba(139,92,246,0.45)`): the violet focus ring, replacing the default browser outline.

### Named Rules
**The Double-Shadow Rule.** A floating surface always has two shadows: an outer drop to peel it off the background and an inner top highlight to round the clay. A surface with only one or neither reads as broken.

## Shapes

The form language is **fully rounded clay**. Every elevated surface uses a pill (`999px`) or a large-radius rounded form (`18–28px`). There are no hard corners, no square tiles, and no mixed-radius cards — roundness is a system invariant that sells the "play-doh" material.

- **Pills:** buttons, rail pills, segmented filters, chips, the capture bar, state chips, toasts, demo badge, NSFW badge.
- **24px:** cards, results dropdown, view toggle.
- **28px (`--radius-clay`):** dialogs, the largest clay surfaces.
- **16–18px:** ghost buttons, icon buttons, form fields, empty-state glyph, result rows.
- Covers are rectangular with their own subtle inner shadows but inherit the card's `24px` radius via `overflow: hidden`.

## Components

### Buttons
- **Shape:** pill (999px) for primary; 18px for ghost/icon.
- **Primary:** violet gradient (`#8b5cf6` → `#6d3df0`), white text, Inter 700, padding `0.7rem 1.35rem`, `--shadow-violet`. Hover: brightness 1.07 + lift 1px. Active: `--shadow-clay-press` + press 1px.
- **Ghost:** clay gradient (`#362e5c` → `#100e20`), ink-muted text, `--shadow-clay-sm`. Hover: ink text + lift 1px.
- **Icon button:** 2.85rem square clay pill (18px radius); hover lifts 1px.

### Capture Bar (signature component)
The hero surface: a full-pill clay form (`#362e5c` → `#100e20`, `--shadow-clay-md`) holding a prefix icon, a transparent text input (placeholder ink-faint), a category picker pill, and a violet **Guardar** submit button. Focus-within swaps the shadow for `--shadow-focus` + `--shadow-clay-md`. Typing a URL or a title opens an absolute-positioned results dropdown (`--radius-clay`, 22rem max height) with per-result covers, titles, and years; picking one runs the detail fetch and saves.

### Cards
- **Corner Style:** 24px.
- **Background:** clay gradient (`#2a2348` → `#221c3d` → `#100e20`).
- **Shadow Strategy:** `--shadow-clay-md` at rest, `--shadow-clay` on hover; hover also lifts the card 4px.
- **Structure:** a 2:2.85 gradient cover (per-category hue) with the title's initial letter, a meta row of genre chips, the title (two-line clamp), a subtitle, and a state chip + action buttons. The state chip carries a glowing dot in sky (pendiente), violet-soft (en curso), or mint (terminado). A rated item adds a violet rating chip (solid star + value, `rgba(139,92,246,0.16)`) in the meta row. Clicking the card (or Enter on it) opens the detail dialog.
- **NSFW gating:** hidden by default; adult items are removed from the grid entirely (no cards, no counts). Revealing is a hidden function (undocumented keyboard shortcut, not exposed anywhere in the UI) that shows the rose badge, without reload.

### Chips
- **Style:** `rgba(255,255,255,0.06)` over clay, ink-muted text, 999px, inset top highlight. State chips use a colored dot (`currentColor`, 0.42rem, glowing).

### Inputs / Fields
- **Style:** clay gradient field, 16px radius, ink text, `--shadow-clay-sm`.
- **Focus:** `--shadow-focus` violet ring replaces the outline.
- **Placeholders:** ink-faint, weight 500.

### Navigation
- **Category rail:** horizontally scrolling pills (clay, ink-muted, `--shadow-clay-sm`); the active category becomes the violet gradient with `--shadow-violet`. Hover lifts 1px.
- **Header:** sticky, night gradient with 8px backdrop blur; brand mark is a violet-gradient rounded square with a bookmark glyph.

### Dialogs
- `--radius-clay` (28px), clay gradient (`#2b2450` → `#221c3d` → `#100e20`), `--shadow-clay` + a 1px white ring. Backdrop is `rgba(4,3,12,0.66)` with 4px blur. Settings rows are separated by a faint white hairline (the one sanctioned border) and drive clay switches; the toggle knob is a white pill on a violet gradient when active.

### Detail dialog
- **Shape:** the shared dialog shell widened to `min(34rem, calc(100vw - 2.5rem))`; a hero row (per-category gradient cover tile, 4.4×5.8rem, with the title's initial centered and the category glyph top-right) beside the title (Inter 800), subtitle, and meta chips. The rose NSFW badge pins to the cover's bottom-left when the item is adult.
- **Rating:** five star controls on a 1–5 scale with half steps. Click the left half of a star for `.5`, the right half for the whole number; `Shift+Enter` gives `.5` on the keyboard. Filled stars render as a violet fill (`var(--color-violet)`) over an ink-faint outline, clipped by `clip-path` for partial fills. A readout shows the value ("4,5 / 5") and a ghost "Quitar" clears it. Keyboard focus returns to the interacted star after re-render.
- **Notas:** a clay textarea (16px radius, 6.5rem min-height, vertical resize) that autosaves with a 350ms debounce; a mint "Guardado" hint appears next to the label. State can be changed in place via the segmented control, and the item deleted from the footer (ghost rose hover). Values persist to the localStorage item on every change.

### Toast
- Bottom-center pill (999px), clay gradient, `--shadow-clay` + 1px ring; slides up 200ms and fades, mint check icon.

## Do's and Don'ts

### Do:
- **Do** float everything: any new surface needs the full double shadow (outer drop + inner top highlight).
- **Do** reserve violet for the one active/action state — primary buttons, selected pills, selected filters.
- **Do** use rose only for adult-content signals, and the amber badge only for demo data.
- **Do** build hierarchy with Inter's three weights and the fixed rem scale; never reach for a display face.
- **Do** keep every corner rounded to the system radii (999px pills, 18px controls, 24px cards, 28px dialogs).
- **Do** let each category's cover gradient carry identity; keep the rest of the card clay-muted.
- **Do** give the capture bar the hero shadow — it is the app's single most-used surface.
- **Do** show focus as the violet `--shadow-focus` ring, never the default outline.

### Don't:
- **Don't** use flat surfaces, hard corners, hairline borders, or outline-only cards — they contradict the modeled-clay material.
- **Don't** add a second accent color to a screen; violet is the action color, and everything else is status or category hue.
- **Don't** introduce uppercase, letter-spaced, italic, or display-font text anywhere in the UI.
- **Don't** build decorative animated load sequences; arrivals are a single 320ms ease-out seat-in, and reduced-motion kills all of it.
- **Don't** place the NSFW badge anywhere but pinned to the cover's bottom-left of an adult card, with rose exclusivity intact.
