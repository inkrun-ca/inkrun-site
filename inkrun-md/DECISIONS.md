# Inkrun — Decision Log

A running record of decisions, so future sessions know *why* things are the way they are. Format per entry: **date — decision / rationale / what it would take to revisit.** Newest entries on top.

---

## 2026-07-18 — "Modern CMYK / Print Shop" palette

- **Decision:** The whole brand runs on the four process colors: `--ink #1A1A1A`, `--paper #FDFDF8`, `--cyan #0077A8`, `--magenta #D6255B`, `--yellow #F2B705` (plus derived `--cyan-dark #00597D` for hover and `--line #D0D0CC` for hairlines). Process cyan `#0090C8` was darkened one step to `#0077A8` so interactive text passes WCAG AA on paper (4.9:1 vs 3.5:1).
- **Rationale:** Newspaper publishers recognize the print shop instantly; it is deliberately unlike any SaaS landing page. Black on paper does 90% of the work, which keeps it readable for senior readers.
- **Revisit if:** a professional brand designer is engaged, or a real-world contrast failure is reported.

## 2026-07-18 — Accent color job assignments

- **Decision:** Cyan = interactive elements only (links, CTA, focus). Magenta = sparing emphasis (the villain's fee figures, a key word, the h2 rule line, form errors). Yellow = marker highlight *behind* ink words at 45% alpha, never text.
- **Rationale:** Fixed jobs keep the four-color system readable instead of carnival. Restraint is what makes it feel like a print shop rather than a daycare.
- **Revisit if:** a genuine use case appears that these jobs cannot cover — document the exception here before shipping it.

## 2026-07-18 — Hand-written inline CSS, no Tailwind CDN

- **Decision:** One `<style>` block in `index.html`; design tokens as CSS custom properties in `:root`.
- **Rationale:** The Tailwind CDN script blocks rendering and warns in production consoles; this page is small enough for hand-written CSS; zero dependencies means instant loads on rural connections; custom properties keep the code and `DESIGN.md` mechanically in sync.
- **Revisit if:** the site grows past a handful of pages and CSS duplication becomes real. Then: a small shared stylesheet first, a build step only if that fails.

## 2026-07-18 — System serif stack, no webfont

- **Decision:** Headlines and body on `"Iowan Old Style", "Palatino Linotype", Palatino, Georgia`; system sans for UI elements (button, labels, small-caps titles). No Google Font.
- **Rationale:** The brief allowed one webfont "if truly needed." Zero external requests keeps the page instant on rural connections, and these old-style serifs already read as print. Justification recorded in `DESIGN.md` §2 as required.
- **Revisit if:** the brand needs a distinctive display face. Budget: one font, self-hosted or Google, justified in `DESIGN.md`.

## 2026-07-18 — GitHub Pages hosting at inkrun.ca

- **Decision:** The landing page is a single static `index.html` at the repo root of `inkrun-ca/inkrun-site`, served by GitHub Pages at inkrun.ca.
- **Rationale:** Free, reliable, TLS included, and a zero-dependency page needs nothing more. Root placement is a Pages requirement.
- **Revisit if:** Inkrun needs server-side features (accounts, payments, the PDF pipeline). The landing page can stay on Pages even then; the app would live elsewhere (e.g. app.inkrun.ca).
