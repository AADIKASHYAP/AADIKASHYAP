#!/usr/bin/env python3
import json,math
from pathlib import Path
d=json.loads(Path('data/contributions.json').read_text(encoding='utf-8')); days=d['days']; cell,gap=14,4; left,top=58,54; cols=math.ceil(len(days)/7); W=left+cols*(cell+gap)+20; H=top+7*(cell+gap)+50; colors=['#161b22','#3b3020','#6b5122','#9a7629','#D4AF37']; rects=[]
for i,x in enumerate(days):
 col,row=divmod(i,7); xx=left+col*(cell+gap); yy=top+row*(cell+gap); lv=max(0,min(4,int(x.get('level',0)))); rects.append(f'<rect x="{xx}" y="{yy}" width="{cell}" height="{cell}" rx="3" fill="{colors[lv]}"><title>{x["date"]}: {x["count"]} contributions</title></rect>')
legend=''.join(f'<rect x="{left+38+i*20}" y="{H-25}" width="14" height="14" rx="3" fill="{c}"/>' for i,c in enumerate(colors))
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d"><style>.bg{fill:#0d0d0d;stroke:#D4AF37;stroke-opacity:.3}.txt{fill:#8e8e8e;font:12px monospace}.stat{fill:#D4AF37;font:600 13px monospace}</style><rect class="bg" x="1" y="1" width="%d" height="%d" rx="18"/><text x="18" y="22" class="stat">%d contributions · current streak %d · longest %d</text>%s<text x="%d" y="%d" class="txt">Less</text>%s<text x="%d" y="%d" class="txt">More</text></svg>'''%(W,H,W-2,H-2,d['total_contributions'],d['current_streak'],d['longest_streak'],''.join(rects),left,H-13,legend,left+145,H-13)
Path('contrib-heatmap.svg').write_text(svg,encoding='utf-8'); print('Wrote contrib-heatmap.svg')
