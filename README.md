# Winters &amp; Yonker, P.A. — homepage rebuild

Static homepage comp for the Tampa personal injury firm, rebuilt from Jeremy's
December design comp. Skyway Media.

## Work on the source, not the build

| path | what it is |
|---|---|
| `build/wy-comp.src.html` | **edit this.** Assets appear as `{{IMG:key}}` / `{{VID:key}}` tokens. |
| `build/build_comp.py` | `python build/build_comp.py` — inlines every asset as a data URI. |
| `build/wy-comp.html` | **generated. Never edit by hand.** ~4 MB. Not in git. |
| `build/wy-preview.html` | **generated.** The same markup wrapped in a doctype — this is what you open locally. Not in git. |
| `src/pages/index.astro` | **generated, but committed.** Same markup with assets by URL. The host has no Python, so re-run the build and commit this file whenever the source changes. |
| `Images/` | photography, logos, trust badges, generated practice-area imagery |
| `Video/` | hero background video |
| `wy-handoff/` | Jeremy's original comp, kept for reference |

Editing a built file means scrolling past megabyte-long data URIs, and any
change is destroyed by the next build.

## Build

    python build/build_comp.py

Needs Python 3 and Pillow (`pip install pillow`) only if you regenerate imagery.
The build itself has no dependencies.

### Always test against `wy-preview.html`

`wy-comp.html` deliberately has no `<!doctype html>` or `<head>` — the Artifact
host supplies those at publish time. Serving the bare file from a static server
renders it in **quirks mode**, where `document.scrollingElement` becomes
`<body>`, scroll events and IntersectionObserver misbehave, and mobile emulation
falls back to 980px. `wy-preview.html` is the same markup wrapped to match the
host. Test with that one.

    python -m http.server 8901 --directory build

## Design system

Colour and type are specified separately; the short version:

| token | light | dark | role |
|---|---|---|---|
| `--oxblood` | `#822227` | — | the red. Dark grounds, headlines and buttons on light. |
| `--oxblood-black` | `#1A0E10` | — | the quiet dark. Pairs beside oxblood, never two reds. |
| `--signal` | `#AF352B` | — | Jeremy's bright red, kept. Pops only, never a ground. |
| `--gold` | `#F5BB2E` | — | the logo gold. Text on dark grounds **only**. |
| `--gold-deep` | `#7C5512` | `#F5BB2E` | the light-ground counterpart. |
| `--page` / `--panel` / `--surface` | `#FFFFFF` / `#F8F5F5` / `#FFFFFF` | `#1B1013` / `#140C0F` / `#22151A` | neutral grounds |
| `--text` / `--muted` | `#1A1310` / `#5F5459` | `#FFFFFF` / `#C6B6B8` | copy |

Type is Archivo (variable, width axis 62–125 — condense before adding weight)
and Newsreader for pull quotes only, under about 5% of the page.

Brand grounds do not flip with the theme. Hero, results, deadlines, FAQ, contact
and footer stay oxblood in both; only the neutrals switch.

## Gotchas, learned the hard way

- **Specificity beats source order.** `nav.nav .lg` (0,2,1) out-ranks a bare
  `.lg-dark` (0,1,0), which rendered both logos at once in light mode. Every
  logo swap rule is scoped to `nav.nav .lg-*` on purpose.
- **Don't gate scroll handlers behind `requestAnimationFrame`.** A backgrounded
  or occluded tab never fires rAF, which leaves a `ticking` flag stuck true and
  kills every scroll effect permanently. The handler runs directly.
- **Reveals must not depend on an observer.** Elements are flagged visible
  *before* the parked state is applied, so the first painted frame is never
  blank and no-JS readers lose nothing.
- **Flex `align-items: stretch` with no child defining a height** resolved the
  nav controls to 77px and pushed the bar to 108px. Both use `--ctl-h` now.
- **The trust badges are artwork on solid white plates**, and white also appears
  inside the design — no PNG export fixes them. They sit on a white band in
  light, and are inverted in dark.

## Open items for the client, not for code

1. **Two of three case results** carry only amounts and case types. Florida Bar
   Rule 4-7.13(b)(2) requires results be objectively verifiable.
2. **Testimonials are placeholder.** Names and quotes must be replaced with
   real, attributable reviews.
3. **TCPA consent wording** in both forms needs an attorney's sign-off.
4. **"119+ years" vs "115+".** The live site (wintersandyonker.com/about) still
   says "over 115 years of combined experience". The comp says 119+. Unchanged
   pending the firm's answer — it is a credential claim, not a copy choice.
5. **Headshots needed for Scott Brown and Courtney Yonker.** Both are listed on
   the firm's live attorney page but were not in the supplied photography, so
   they currently render as monogram placeholders marked "photo pending".
6. ~~`auto accident 3.webp` shows readable third-party signage.~~ **Resolved** —
   it no longer appears on the page; the results slider uses generated imagery.
7. Attorney photo mapping is **resolved** — the supplied files are individually
   named, closing Jeremy's original open item.
