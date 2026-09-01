#!/usr/bin/env python3
import argparse
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageEnhance
from rembg import remove

p=argparse.ArgumentParser(); p.add_argument('input',nargs='?',default='hero.png'); p.add_argument('--output',default='source-prepped.png'); a=p.parse_args()
src=Path(a.input)
if not src.exists(): raise SystemExit(f'Input portrait not found: {src}')
raw=remove(src.read_bytes()); tmp=Path('_rembg.png'); tmp.write_bytes(raw)
img=cv2.imread(str(tmp),cv2.IMREAD_UNCHANGED)
if img is None: raise SystemExit('Could not decode rembg output.')
if img.shape[2]==4:
    alpha=img[:,:,3]; ys,xs=np.where(alpha>8)
    if len(xs):
        pad=30; img=img[max(0,ys.min()-pad):min(img.shape[0],ys.max()+pad+1),max(0,xs.min()-pad):min(img.shape[1],xs.max()+pad+1)]
lab=cv2.cvtColor(img[:,:,:3],cv2.COLOR_BGR2LAB); l,c1,c2=cv2.split(lab); l=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8)).apply(l)
enh=cv2.cvtColor(cv2.merge((l,c1,c2)),cv2.COLOR_LAB2BGR)
pil=Image.fromarray(cv2.cvtColor(enh,cv2.COLOR_BGR2RGB)).convert('RGB'); pil=ImageEnhance.Contrast(pil).enhance(1.08)
r=900/pil.height; pil=pil.resize((max(1,int(pil.width*r)),900),Image.Resampling.LANCZOS); pil.save(a.output,'PNG',optimize=True); tmp.unlink(missing_ok=True)
print('Wrote',a.output)
