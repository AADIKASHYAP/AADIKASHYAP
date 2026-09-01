#!/usr/bin/env python3
"""Fetch the public GitHub contribution calendar."""
import json,re
from datetime import date
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME="AADIKASHYAP"; OUT=Path("data/contributions.json")

def main():
    r=requests.get(f"https://github.com/users/{USERNAME}/contributions",headers={"User-Agent":"adarsh-profile"},timeout=30); r.raise_for_status()
    soup=BeautifulSoup(r.text,"html.parser"); days=[]
    for cell in soup.select("[data-date]"):
        d=cell.get("data-date");
        if not d: continue
        label=cell.get("aria-label",""); cm=re.search(r"(\d[\d,]*) contribution",label); lm=re.search(r"Contribution level: (\d)",label)
        days.append({"date":d,"count":int(cm.group(1).replace(",","")) if cm else 0,"level":int(lm.group(1)) if lm else int(cell.get("data-level",0) or 0)})
    if not days: raise RuntimeError("GitHub contribution markup changed; no contribution cells found.")
    days.sort(key=lambda x:x["date"]); current=0
    for x in reversed(days):
        if x["count"]>0: current+=1
        else: break
    longest=run=0
    for x in days:
        run=run+1 if x["count"]>0 else 0; longest=max(longest,run)
    result={"username":USERNAME,"fetched_at":date.today().isoformat(),"total_contributions":sum(x["count"] for x in days),"current_streak":current,"longest_streak":longest,"best_day":max(days,key=lambda x:x["count"]),"days":days}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(result,indent=2),encoding="utf-8"); print("Contribution data updated.")

if __name__ == "__main__": main()
