#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageOps
from xml.sax.saxutils import escape
RAMP=' .`:-=+*cs#%@'; src=Path('source-prepped.png'); out=Path('hxni-ascii.svg')
if not src.exists(): raise SystemExit('source-prepped.png not found. Add hero.png and run prep_photo.py first.')
im=Image.open(src).convert('L'); cols=76; scale=min(1,cols/im.width); w=max(1,int(im.width*scale)); h=max(1,int(im.height*scale*.52)); im=ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS)
lines=[]
for y in range(h):
    lines.append(''.join(RAMP[max(0,min(len(RAMP)-1,int((255-im.getpixel((x,y)))/256*len(RAMP))))] for x in range(w)).rstrip())
texts=''.join('<text x="28" y="{}" class="ascii" style="animation-delay:{:.3f}s">{}</text>'.format(82+i*9,i*.012,escape(s)) for i,s in enumerate(lines))
W=760; H=max(160,92+len(lines)*9)
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><defs><style>.ascii{fill:#D4AF37;font-family:Consolas,monospace;font-size:8px;opacity:0;animation:fin .55s ease forwards}@keyframes fin{from{opacity:0;transform:translateY(4px)}to{opacity:.96;transform:translateY(0)}}</style></defs><rect width="%d" height="%d" rx="22" fill="#0d0d0d" stroke="#D4AF37" stroke-opacity=".45"/><rect width="%d" height="44" fill="#171717"/><circle cx="24" cy="22" r="6" fill="#ff5f57"/><circle cx="44" cy="22" r="6" fill="#febc2e"/><circle cx="64" cy="22" r="6" fill="#28c840"/><text x="88" y="28" fill="#aaa" font-family="monospace" font-size="12">ADARSH@CIPHER — ASCII PORTRAIT</text><g>%s</g><rect x="0" y="44" width="0" height="2" fill="#D4AF37"><animate attributeName="width" from="0" to="%d" dur="1.8s" fill="freeze"/></rect></svg>'''%(W,H,W,H,W,H,W,texts,W)
out.write_text(svg,encoding='utf-8'); print('Wrote',out)
