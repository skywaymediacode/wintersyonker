import io, os, urllib.request
from PIL import Image

BASE = "https://cdn.openart.ai/openart-ai/production/2026-09/create-image/LMtEkyhchOo5aRzlawjK/"
JOBS = {
 "pedestrian":    "gpt-image-2-1_1788559634531_44ee288b.png",
 "rideshare":     "gpt-image-2-1_1788559633937_12891bb8.png",
 "slipfall":      "gpt-image-2-1_1788559640245_d8bf00e2.png",
 "construction":  "gpt-image-2-1_1788559644972_93794562.png",
 "braininjury":   "gpt-image-2-1_1788559648406_9e09fff6.png",
 "nursinghome":   "gpt-image-2-1_1788559652307_4f092a35.png",
 "dogbites":      "gpt-image-2-1_1788559660124_e8f8d69c.png",
 "wrongfuldeath": "gpt-image-2-1_1788559658447_b3462ca6.png",
}
NAMES = {
 "pedestrian":"gen pedestrian accidents","rideshare":"gen uber lyft accidents",
 "slipfall":"gen slip and fall","construction":"gen construction accidents",
 "braininjury":"gen brain injury","nursinghome":"gen nursing home neglect",
 "dogbites":"gen dog bites","wrongfuldeath":"gen wrongful death",
 "allpi":"gen all personal injury",
}
TARGET_W = 1200
os.makedirs("Images", exist_ok=True)
total = 0
for key, fn in JOBS.items():
    req = urllib.request.Request(BASE + fn, headers={"User-Agent":"Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=90).read()
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = im.size
    im = im.resize((TARGET_W, round(h * TARGET_W / w)), Image.LANCZOS)
    out = os.path.join("Images", NAMES[key] + ".webp")
    im.save(out, "WEBP", quality=80, method=6)
    s = os.path.getsize(out); total += s
    print(f"{s:8,d}  {im.size[0]}x{im.size[1]}  {NAMES[key]}.webp")
print(f"\ntotal {total:,d} bytes ({total/1048576:.2f} MB)")
