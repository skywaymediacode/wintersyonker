#!/usr/bin/env python3
"""Inline every asset into the deliverable.
   wy-gagliano.src.html  +  img/assets.json  ->  Winters-Yonker-Homepage.html"""
import json, re, os, sys
a = json.load(open('img/assets.json'))
h = open('wy-gagliano.src.html', encoding='utf-8').read()
def img(m):
    k = m.group(1)
    if k not in a: sys.exit('missing image asset: ' + k)
    return 'data:image/webp;base64,' + a[k]
def vid(m):
    k = m.group(1)
    if k not in a: sys.exit('missing video asset: ' + k)
    return 'data:video/mp4;base64,' + a[k]
out = re.sub(r'\{\{IMG:([a-z0-9\-]+)\}\}', img, h)
out = re.sub(r'\{\{VID:([a-z0-9\-]+)\}\}', vid, out)
left = re.findall(r'\{\{[^}]+\}\}', out)
if left: sys.exit('unresolved tokens: %s' % left)
open('Winters-Yonker-Homepage.html', 'w', encoding='utf-8').write(out)
print('built Winters-Yonker-Homepage.html  %.2f MB' % (os.path.getsize('Winters-Yonker-Homepage.html')/1048576))
