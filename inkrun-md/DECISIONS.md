# Inkrun — Decision Log

A running record of decisions, so future sessions know *why* things are the way they are. Format per entry: **date — decision / rationale / what it would take to revisit.** Newest entries on top.

---

## 2026-07-20 — New headline: "Your paper. Your readers. Your paper online."

- **Decision:** The hero headline is now "Your paper. Your readers. Your paper online." (replacing "One flat rate. Your readers stay yours."). An alternate — "Your paper, online. Your readers, yours." — sits in an HTML comment directly above the `h1` for manual swapping. The subheadline now carries the pricing in two sentences, without figures: "one flat monthly rate, in USD or CAD."
- **Rationale:** Lead with ownership and identity, not price. The rate is now stated once, as a fact, in the pricing section — the headline's job is to say whose paper it is.
- **Revisit if:** waitlist conversion data says otherwise, or publisher interviews surface a stronger line.

## 2026-07-20 — Price fixed at $42 USD / $56 CAD per month; annual at 15% off

- **Decision:** The $35–$40 range is retired. One flat price, dual currency: **$42 USD / $56 CAD per month**; annual **$428 USD / $571 CAD**, billed once (15% off). Each figure appears exactly once per location, wrapped in `<!-- PRICE ... -->` comments (pricing section, plus the Inkrun column of the comparison table) for find-and-replace. All other copy — subheadline, value blocks, meta description — says "one flat monthly rate" and quotes no numbers. The old "One flat rate" value block was folded into this section and removed from "What we are building instead," so the price claim lives in exactly one place.
- **Rationale:** A range reads as undecided; a single number reads as a utility rate card. Dual currency matches the market: Canadian publishers think and are billed in CAD, and the USD figure keeps the price legible across the border — the pair sits at roughly the prevailing exchange rate while staying round in both currencies. The 15% annual discount rewards commitment without lock-in: "cancel anytime" stays true either way.
- **Revisit if:** publisher interviews show price resistance, costs change materially, or the exchange rate drifts far enough that one currency looks wrong.

## 2026-07-20 — Advertising narrative removed from the page

- **Decision:** Every reference to selling ads or blocked local advertising is gone from the prose of `index.html` (the "hardware store on Main Street" paragraph was cut whole). The facts that remain about the villains: the $2,000 renewal, the upkeep fee skimmed at reader checkout, the entry fee, zero equity. Note: `BRAND.md` still documents the full villain narrative including the blocked advertiser — left as-is for now; update it if this removal proves permanent.
- **Rationale:** Advertising is no longer part of the story. The new comparison table carries the contrast, so the prose can state facts calmly instead of arguing.
- **Revisit if:** ads become part of the product story again — restore deliberately, in one place, not piecemeal.

## 2026-07-20 — Comparison table added; competitor tone de-escalated

- **Decision:** A three-column table (Legacy flipbook platforms / National newsstand collectives / Inkrun) sits directly after the pricing section: monthly cost, checkout fee, subscriber-list ownership, merchant of record (with a Stripe Connect link, `rel="noopener"`), ads, equity. Hairline rules, generous padding, no shading; the Inkrun column header alone uses `--cyan` — this is the documented exception called for by the accent-jobs entry below. Below 768px it restacks into one labeled block per competitor, CSS only. Prose across the page was cut by roughly a quarter to a third and de-escalated: the figures kept, the "We are done paying them" energy dropped.
- **Rationale:** A table of facts makes the contrast better than heated prose can. Publishers trust numbers over adjectives; the calmer tone reads as confidence, not surrender.
- **Revisit if:** a competitor changes its terms (keep the table accurate), or a fourth column is ever needed.

## 2026-07-20 — Registration strip added to the masthead

- **Decision:** A printer's color-control strip — five solid squares (`--cyan`, `--magenta`, `--yellow`, `--ink`, 18% grey `#D1D1D1`) at the 32px height of the logo mark — sits right-justified on the wordmark line. Each square is offset vertically 1–3px in a varying direction for deliberate misregistration. Below ~480px the squares shrink to 24px and the strip wraps to a second line, still right-justified. Pure CSS, `aria-hidden`. Documented in `DESIGN.md` as the "registration strip"; it is the one sanctioned place the process colors appear as pure swatches.
- **Rationale:** The color-control strip is the pressman's craft mark — it says "print shop" before a word is read, and the misregistration keeps it human rather than pixel-perfect.
- **Revisit if:** it reads as clutter in real feedback, or a designed logo replaces the woodcut mark.

## 2026-07-20 — Content column widened 40rem → 48rem

- **Decision:** `.wrap` and `.rule` `max-width` went from 40rem to 48rem (~+20%). Paragraph measure stays at 34em; mobile layout is unchanged.
- **Rationale:** The comparison table needs the breathing room; paragraphs keep their own measure, so reading comfort is untouched.
- **Revisit if:** a genuinely wide component (dashboard-style UI) arrives — then rethink the grid as a whole, not just the number.

## 2026-07-18 — "Modern CMYK / Print Shop" palette

- **Decision:** The whole brand runs on the four process colors: `--ink #1A1A1A`, `--paper #FDFDF8`, `--cyan #0077A8`, `--magenta #D6255B`, `--yellow #F2B705` (plus derived `--cyan-dark #00597D` for hover and `--line #D0D0CC` for hairlines). Process cyan `#0090C8` was darkened one step to `#0077A8` so interactive text passes WCAG AA on paper (4.9:1 vs 3.5:1).
- **Rationale:** Newspaper publishers recognize the print shop instantly; it is deliberately unlike any SaaS landing page. Black on paper does 90% of the work, which keeps it readable for senior readers.
- **Revisit if:** a professional brand designer is engaged, or a real-world contrast failure is reported.

## 2026-07-18 — Accent color job assignments

- **Decision:** Cyan = interactive elements only (links, CTA, focus). Magenta = sparing emphasis (the villain's fee figures, a key word, the h2 rule line, form errors). Yellow = marker highlight *behind* ink words at 45% alpha, never text.
- **Rationale:** Fixed jobs keep the four-color system readable instead of carnival. Restraint is what makes it feel like a print shop rather than a daycare.
- **Revisit if:** a genuine use case appears that these jobs cannot cover — document the exception here before shipping it. (2026-07-20: two exceptions now documented — the comparison table's Inkrun column header, and the registration strip swatches.)

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
