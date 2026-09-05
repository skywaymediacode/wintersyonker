# Winters & Yonker — homepage design comp

## Work on the source, not the build

| file | what it is |
|---|---|
| `wy-gagliano.src.html` | **edit this.** 89 KB. Assets appear as `{{IMG:key}}` / `{{VID:key}}` tokens. |
| `img/assets.json` | asset store: `{ "key": "<base64>" }`. 3.3 MB. Don't open it in an editor. |
| `build.py` | `python3 build.py` — inlines every asset into the deliverable. |
| `Winters-Yonker-Homepage.html` | **generated output. Never edit by hand.** 2.8 MB, ~23 base64 blobs. |

Editing the built file directly means scrolling past megabyte-long data URIs and
any change is destroyed by the next build.

## Assets in use

`heroposter` `herovideo` · `introphoto` `measurephoto` · `res1` `res2` `res3`
`atty01`–`atty08` · `bdg-bbb` `bdg-exp` `bdg-s21` `bdg-s25` `bdg-seal`
`wylogo` `wylockup` · `blocks` (practice-tile background)

Unused but retained: `skyway`, `tampa`, `truck`, and earlier concept art.

## External dependencies

Exactly one: the Google Fonts stylesheet (Archivo + Libre Baskerville).
Everything else — 20 images and the hero video — is inlined as data URIs and
renders with the network fully blocked. Fallback stacks are declared, so the
page degrades to Helvetica/Georgia offline rather than breaking.

## Verify after changing anything

    node verify/shot3.js       # overflow-X, page height, JS errors, desktop + mobile
    node verify/a11y3.js       # WCAG AA contrast sweep, form + accordion function
    node verify/tilecheck.js   # practice-tile contrast (the tint lives on a pseudo-element,
                               #   which the generic scanner cannot see)
    node verify/finalcheck.js  # hero video controls, sliders, tel links

Chromium: `/opt/pw-browsers/chromium`. Use `waitUntil:'load'` — `networkidle`
hangs on the Google Fonts request.

`a11y3.js` reports 12 contrast "failures" that are all false positives: the
practice tiles apply their colour via `::after`, invisible to `getComputedStyle`.
`tilecheck.js` composites the tint properly and reports the real numbers
(worst case 5.12:1, zero failures).

## Known gotchas, learned the hard way

- **`overflow:hidden` on a section kills `position:sticky` inside it.** Four
  sticky columns were silently inert because of leftover clipping rules.
- **Specificity beats source order for `.sticky-col`.** Two columns lost to a
  later `position:relative`; the rule is doubled (`.sticky-col.sticky-col`) on purpose.
- **Generic descendant selectors catch new wrappers.** `.pt span` and
  `.faq-art img` both broke when elements were added. Scope to `>` or a class.
- **Class-name collisions.** A `.ck` clock card silently deformed the `.ck`
  checkmark circles. Grep before naming.

## Open items for the client, not for code

1. **Attorney names may be on the wrong photos.** The two men in the courthouse
   photos are the founding partners, but the grid labels them Christopher M. Smith
   and Anthony LoGalbo. Mapping needs confirming before launch.
2. **Testimonials are invented.** Names, times and dollar figures are placeholder.
3. **Two of three case descriptions are placeholder** — only the amounts and
   case types came from the client. Florida Bar Rule 4-7.13(b)(2) requires
   results be objectively verifiable.
4. **TCPA consent wording** in the hero form needs an attorney's approval.
5. **"119+ years"** conflicts with "115+" on the firm's live About page.
6. In WordPress the hero video should be a separate lazy-loaded asset, not inlined.
