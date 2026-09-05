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
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "build" / "wy-comp.src.html"
OUT = ROOT / "build" / "wy-comp.html"
PREVIEW = ROOT / "build" / "wy-preview.html"

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

    kb = OUT.stat().st_size / 1024
    print(f"built {OUT.name}  {kb:,.0f} KB  ({kb / 1024:.1f} MB)")
    print(f"local test copy -> {PREVIEW.name}  (doctype-wrapped, standards mode)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
