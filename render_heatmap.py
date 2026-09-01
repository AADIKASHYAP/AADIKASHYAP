#!/usr/bin/env python3
"""Render a self-contained contribution heatmap SVG."""
import json,math
from pathlib import Path
DATA=Path("data/contributions.json"); OUT=Path("assets/contribution-heatmap.svg")

def main():
    data=json.loads(DATA.read_text(encoding="utf-8")); days=data["days"]; colors=["#161b22","#3b3020","#6b5122","#9a7629","#D4AF37"]; cell,gap=12,4; left,top=45,52; cols=math.ceil(len(days)/7); width,height=left+cols*(cell+gap)+20,155
    rects=[]
    for i,item in enumerate(days):
        col,row=divmod(i,7); x,y=left+col*(cell+gap),top+row*(cell+gap); level=max(0,min(4,int(item.get("level",0))))
        rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{colors[level]}"><title>{item["date"]}: {item["count"]} contributions</title></rect>')
    legend="".join(f'<rect x="{width-180+i*20}" y="18" width="12" height="12" rx="3" fill="{c}"/>' for i,c in enumerate(colors))
    svg='''<svg xmlns="http://www.w3.org/2000/svg" width="WIDTH" height="155" viewBox="0 0 WIDTH 155"><rect x="1" y="1" width="BW" height="153" rx="18" fill="#0b0d10" stroke="#D4AF37" stroke-opacity=".25"/><text x="20" y="28" fill="#D4AF37" font-family="monospace" font-size="13">TOTAL contributions</text><text x="210" y="28" fill="#858c96" font-family="monospace" font-size="12">current CURRENT · longest LONGEST</text>LEGENDRECTS</svg>'''.replace("WIDTH",str(width)).replace("BW",str(width-2)).replace("TOTAL",str(data["total_contributions"])).replace("CURRENT",str(data["current_streak"])).replace("LONGEST",str(data["longest_streak"])).replace("LEGENDRECTS",legend+"".join(rects))
    OUT.write_text(svg,encoding="utf-8"); print("Contribution heatmap rendered.")
if __name__=="__main__": main()
