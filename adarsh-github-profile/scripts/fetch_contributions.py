#!/usr/bin/env python3
import argparse,json,re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

def main():
 p=argparse.ArgumentParser(); p.add_argument('username'); p.add_argument('--output',default='data/contributions.json'); a=p.parse_args()
 r=requests.get(f'https://github.com/users/{a.username}/contributions',headers={'User-Agent':'adarsh-profile-bot/1.0'},timeout=30); r.raise_for_status(); soup=BeautifulSoup(r.text,'html.parser')
 days=[]
 for c in soup.select('[data-date]'):
  d=c.get('data-date'); label=c.get('aria-label',''); m=re.search(r'(\d[\d,]*) contribution',label); lm=re.search(r'Contribution level: (\d)',label)
  if d: days.append({'date':d,'count':int(m.group(1).replace(',','')) if m else 0,'level':int(lm.group(1)) if lm else int(c.get('data-level',0) or 0)})
 if not days: raise SystemExit('No contribution cells found; GitHub markup may have changed.')
 days.sort(key=lambda x:x['date']); cur=0
 for x in reversed(days):
  if x['count']>0: cur+=1
  else: break
 longest=run=0
 for x in days: run=run+1 if x['count']>0 else 0; longest=max(longest,run)
 data={'username':a.username,'fetched_at':__import__('datetime').date.today().isoformat(),'total_contributions':sum(x['count'] for x in days),'current_streak':cur,'longest_streak':longest,'best_day':max(days,key=lambda x:x['count']),'days':days}
 Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(data,indent=2),encoding='utf-8'); print('Wrote',a.output)
if __name__=='__main__': main()
