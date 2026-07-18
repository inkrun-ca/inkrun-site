# Inkrun Design System — "Modern CMYK / Print Shop"

A modern take on the four process colors, rendered as a hand-crafted print shop: block print, letterpress, woodblock. Colorful but always readable. Human, not startup.

This is the living source of truth for anything built on-brand. The machine-readable copy of this palette lives in the `:root` block of `index.html` — the two must stay in sync. If you change one, change both.

---

## 1. Color palette

| Token | Hex | Job | Contrast on `--paper` |
|---|---|---|---|
| `--ink` | `#1A1A1A` | Body text, headlines, rules, structure | 17.0:1 (AAA) |
| `--paper` | `#FDFDF8` | Page background ("paper white") | — |
| `--cyan` | `#0077A8` | **Interactive only**: links, CTA, focus states | 4.9:1 (AA) |
| `--cyan-dark` | `#00597D` | CTA hover/active | white text on it: 7.7:1 (AAA) |
| `--magenta` | `#D6255B` | **Sparing emphasis**: a key word, the h2 rule line, the villain's fee figures, form error text | 4.8:1 (AA) |
| `--yellow` | `#F2B705` | **Highlight behind ink words only** (used at 45% alpha, marker-style) | ink on full yellow: 9.6:1; ink on 45% over paper: ~13:1 (AAA) |
| `--line` | `#D0D0CC` | Hairline rules (≈ ink at 20% on paper) | decorative only, never text |

White (`#FFFFFF`) appears in exactly one place: text on `--cyan`/`--cyan-dark` buttons (5.0:1 / 7.7:1).

`--cyan` is the brand's process cyan (`#0090C8`) darkened one step so interactive text passes WCAG AA on paper. `#0090C8` itself (3.5:1) is reserved for large graphical accents only, never text.

### Color rules (enforce strictly)

- Black on paper does 90% of the work. **Body text is always `--ink`.**
- If it isn't clickable, it isn't cyan. Cyan never appears as decoration or body text.
- Magenta is a spice, not a sauce: fee figures, one key word, the 3px rule under each h2, the form error. Never large fills, never backgrounds, never body text.
- **Yellow is never text.** It only sits *behind* `--ink` words, at `rgba(242, 183, 5, 0.45)`, marker-style. Yellow text on white/paper fails contrast and is forbidden.
- Forbidden combinations: yellow text anywhere; magenta backgrounds behind text; cyan text on magenta or vice versa; any text on yellow except `--ink`; text over `--line`.

---

## 2. Typography

### Stacks (no webfonts — see rationale)

- Serif (headlines + body): `"Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Times New Roman", serif`
- Sans (UI: buttons, labels, small caps titles): `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`

**Why no Google Font:** the brief allows one "if truly needed." It isn't. Zero external requests keeps the page instant on rural connections, and these old-style serifs already carry print character (Iowan on Apple devices, Palatino elsewhere, Georgia as the universal floor). Revisit only if the brand needs a distinctive display face; if so, one font, justified here.

### Scale and rules

- Root is `font-size: 100%` and everything is in `rem`, so the reader's own font-size setting wins. This is deliberate: our readers skew senior.
- Body: `1.25rem` (20px), line-height 1.6. Body copy never goes below 20px.
- h1: `clamp(2.4rem, 7vw, 3.6rem)`, line-height 1.12.
- h2: `clamp(1.75rem, 5vw, 2.25rem)`, line-height 1.2, with the magenta rule (`::after`, 3rem × 3px).
- Lede: `1.375rem`, line-height 1.5.
- Fine print (footer, form helper): `1rem` minimum, always `--ink` — no greyed-out small text.
- Measure: `max-width: 34em` on paragraphs (≈ 65–70 characters). Column: `max-width: 40rem`.
- Ragged right, never justified. Sentence case headings.

---

## 3. Craft vocabulary

Texture is suggestion, not costume.

**Woodcut motifs** (inline SVG, single color `currentColor` at ~55–80% opacity, stroke-based, round caps/joins, slightly irregular coordinates for the hand-drawn feel). The canon:

1. **Ink roller (brayer)** — masthead, section dividers
2. **Folded newspaper** — section dividers, favicon (in `--cyan`)
3. **Platen press** — section dividers

New motifs must match this style (stroke ~2.4, `stroke-linecap="round"`, no fills except tiny accents) and are always decorative: `aria-hidden="true" focusable="false"`.

**Allowed textures and rules:**

- Exactly **one** paper grain: the inline SVG `feTurbulence` noise in `body` background (~3.5% alpha black, ~350 bytes). Never a second texture.
- Letterpress hairlines (`--line`) as section dividers, with a centered motif (`.rule`).
- The classic thick/thin press rule (`.pressrule`: 3px + 1px `--ink`) for the masthead. Use once per page, top only.

**Forbidden:** gradients (including "subtle" ones), hero blobs, stock illustrations, heavy grunge overlays, drop shadows on text, card grids with shadows, pill navbars — anything that reads as "SaaS template."

---

## 4. Component patterns (established by index.html)

- **`.btn`** — cyan fill, 2px `--ink` border, 4px radius, white bold sans 1.25rem, `min-height: 64px`. Hover: `--cyan-dark`. Active: `translateY(1px)`. No shadow.
- **Links** — `--cyan`, always underlined (1.5px, offset 0.16em); never color-only. Hover `--cyan-dark`.
- **Focus** — `:focus-visible` 3px `--cyan` outline, 3px offset, everywhere.
- **h2 + magenta rule** — the only systematic magenta accent.
- **`mark`** — yellow marker highlight behind ink words; `box-decoration-break: clone` for multi-line.
- **`.fee`** — magenta bold, reserved for the villain's money figures.
- **`.rule`** — hairline divider + centered woodcut motif.
- **`.pressrule`** — thick/thin double rule, masthead only.
- **`.value` blocks** — 1px `--ink` top border, sans small-caps title (`1rem`, 0.06em tracking), 20px serif body; 1 column on mobile, 2 columns ≥ 44rem.
- **`.form-frame`** — 1px `--line` border, white background, 620px iframe; always paired with a visible direct link under it (the first fallback) and the JS-revealed `#form-fallback` block (the second).
- **Footer** — hairline top border; contact links at 1.25rem with 64px tap height; fine print 1rem.

---

## 5. Accessibility commitments

- WCAG **AA minimum** on every text/background pair; body text sits at AAA (17:1).
- 20px base font, `rem` units, reader font-size settings respected.
- **64px minimum tap targets** on buttons, the fallback submit, and footer contact links.
- Links are always underlined; meaning never rides on color alone.
- `prefers-reduced-motion`: smooth scroll and button transition only exist inside `@media (prefers-reduced-motion: no-preference)`.
- Decorative SVGs are `aria-hidden`; the Tally iframe has a `title`; one `h1`; skip link present.
- The highlight and selection colors keep ink text at AAA.

---

## 6. Performance budget

- Single self-contained `index.html`: inline CSS, zero webfonts, zero JS dependencies.
- Total page weight under **80KB** (currently ~19KB). The only external request allowed is the Tally iframe.
- Every texture and motif is inline SVG or CSS — no image files.
