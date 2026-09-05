#!/usr/bin/env python3
"""Inline every asset into the deliverable comp.

Edit wy-comp.src.html, never a built file. Assets appear there as
{{IMG:key}} / {{VID:key}} tokens; this script swaps each for a data URI.

    python build/build_comp.py

Two files come out:

  wy-comp.html     the deliverable, published as the Artifact.
  wy-preview.html  the same markup wrapped in a doctype and <head>.

The wrapped copy exists because the Artifact host supplies the doctype, charset
and viewport meta at publish time. Serving the bare deliverable from a local
static server therefore renders it in QUIRKS MODE, where document.scrollingElement
becomes <body>, scroll events and IntersectionObserver misbehave, and mobile
emulation falls back to 980px. Always test against wy-preview.html.
"""
import base64
import pathlib
import urllib.parse
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "build" / "wy-comp.src.html"
OUT = ROOT / "build" / "wy-comp.html"
PREVIEW = ROOT / "build" / "wy-preview.html"
PAGE = ROOT / "src" / "pages" / "index.astro"

IMAGES = {
    "logo":        "logo.webp",
    "logoDark":    "logo-dark-supplied.webp",
    "logostack":   "WY logo 2.webp",
    "herocover":   "hero cover.webp",
    "badge1":      "Trust Badge 1.webp",
    "badge2":      "Trust Badge 2.webp",
    "badge3":      "Trust Badge 3.webp",
    "badge4":      "Trust Badge 4.webp",
    "badge5":      "Trust Badge 5.webp",
    "acc1":        "auto accident.webp",
    "acc2":        "auto accident 2.webp",
    "acc3":        "auto accident 3.webp",
    "duo":         "WY duo.webp",
    "experience":  "Experience.webp",
    "attyBill":    "Bill Winters.webp",
    "attyMarc":    "Marc Yonker.webp",
    "attyPatrick": "Patrick Douglas Brannon.webp",
    "attyMatthew": "Matthew Brown.webp",
    "attyTrevor":  "Trevor Wade Colvin.webp",
    "attyChris":   "Christopher M Smith.webp",
    "attyAnthony": "Anthony Logalbo.webp",
    "attyMax":     "Max Shevrin.webp",

    "pedestrian":    "gen pedestrian accidents.webp",
    "rideshare":     "gen uber lyft accidents.webp",
    "slipfall":      "gen slip and fall.webp",
    "construction":  "gen construction accidents.webp",
    "braininjury":   "gen brain injury.webp",
    "nursinghome":   "gen nursing home neglect.webp",
    "dogbites":      "gen dog bites.webp",
    "wrongfuldeath": "gen wrongful death.webp",
    "allpi":         "gen all personal injury.webp",
    "motorcycle":    "gen motorcycle accidents.webp",
    "highway":       "gen highway rear end.webp",
    "nighthighway":  "gen night highway.webp",
    "tampabay":      "gen tampa bay.webp",
}

VIDEOS = {
    "hero": "winters-yonker-hero-background.mp4",
}

PREVIEW_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
"""

PREVIEW_TAIL = """
</body>
</html>
"""


PAGE_HEAD = """---
// GENERATED FILE - do not edit.
// Source: build/wy-comp.src.html  ->  python build/build_comp.py
// Assets resolve to /images and /video in public/ rather than being inlined,
// so the deployed site ships cacheable files instead of one 4 MB document.
---

<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Winters &amp; Yonker, P.A. | Tampa Personal Injury Lawyers</title>
<link rel="canonical" href="https://www.winters-yonker.com/">
<meta property="og:type" content="website">
<meta property="og:title" content="Winters &amp; Yonker, P.A. | Tampa Personal Injury Lawyers">
<meta property="og:url" content="https://www.winters-yonker.com/">
<meta property="og:image" content="https://www.winters-yonker.com/images/hero%20cover.webp">
<meta name="description" content="Tampa Bay personal injury lawyers. A real person answers this phone, 24 hours a day. And we don't get paid unless you do.">
<script is:inline>
  /* resolve the stored theme before first paint to avoid a flash */
  (function(){try{var t=localStorage.getItem("wy-theme");
  if(t==="dark"||t==="light")document.documentElement.setAttribute("data-theme",t);}catch(e){}})();
</script>
"""

PAGE_MID = """</style>
</head>
<body>
"""

PAGE_TAIL = """
</body>
</html>
"""


def public_url(folder: str, name: str) -> str:
    return "/" + folder + "/" + urllib.parse.quote(name)


def data_uri(path: pathlib.Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def main() -> int:
    html = SRC.read_text(encoding="utf-8")
    missing = []

    for key, name in IMAGES.items():
        path = ROOT / "public" / "images" / name
        if not path.exists():
            missing.append(str(path))
            continue
        html = html.replace("{{IMG:%s}}" % key, data_uri(path, "image/webp"))

    for key, name in VIDEOS.items():
        path = ROOT / "public" / "video" / name
        if not path.exists():
            missing.append(str(path))
            continue
        html = html.replace("{{VID:%s}}" % key, data_uri(path, "video/mp4"))

    if missing:
        print("missing assets:", *missing, sep="\n  ")
        return 1

    leftover = sorted(set(re.findall(r"\{\{(?:IMG|VID):[A-Za-z0-9_]+\}\}", html)))
    if leftover:
        print("unresolved tokens:", *leftover, sep="\n  ")
        return 1

    OUT.write_text(html, encoding="utf-8")
    PREVIEW.write_text(PREVIEW_HEAD + html + PREVIEW_TAIL, encoding="utf-8")

    # Astro page: same markup, public asset URLs.
    page = SRC.read_text(encoding="utf-8")
    for key, name in IMAGES.items():
        page = page.replace("{{IMG:%s}}" % key, public_url("images", name))
    for key, name in VIDEOS.items():
        page = page.replace("{{VID:%s}}" % key, public_url("video", name))
    # the comp working title must not survive into the deployed page
    page = re.sub(r"<title>.*?</title>" + chr(92) + "s*", "", page, count=1, flags=re.S)
    # Astro scopes <style> by stamping data-astro-cid on both selectors and
    # elements. Anything the page creates at runtime (the theme icon, the
    # results counter) never receives that attribute, so scoped rules silently
    # stop matching it. This stylesheet is a whole document's CSS: keep it global.
    page = page.replace("<style>", "<style is:global>", 1)
    head, _, body = page.partition("</style>")
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(PAGE_HEAD + head + PAGE_MID + body + PAGE_TAIL, encoding="utf-8")

    kb = OUT.stat().st_size / 1024
    print(f"built {OUT.name}  {kb:,.0f} KB  ({kb / 1024:.1f} MB)")
    print(f"local test copy -> {PREVIEW.name}  (doctype-wrapped, standards mode)")
    print(f"astro page      -> src/pages/{PAGE.name}  ({PAGE.stat().st_size / 1024:,.0f} KB, assets by URL)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
