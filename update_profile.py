#!/usr/bin/env python3
"""Update project cards from real public GitHub repositories."""
import json, re
from pathlib import Path
import requests

USERNAME = "AADIKASHYAP"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "repositories.json"
README = ROOT / "README.md"
START, END = "<!-- PROJECTS:START -->", "<!-- PROJECTS:END -->"

def get_repos():
    result, page = [], 1
    while True:
        r = requests.get(f"https://api.github.com/users/{USERNAME}/repos", params={"per_page":100,"page":page,"type":"owner","sort":"updated"}, headers={"Accept":"application/vnd.github+json","User-Agent":"adarsh-profile"}, timeout=30)
        r.raise_for_status(); batch = r.json()
        if not batch: break
        result.extend(batch)
        if len(batch) < 100: break
        page += 1
    return [x for x in result if not x.get("fork") and not x.get("archived")]

def render(repos):
    if not repos:
        return '<div align="center"><img src="./assets/projects-placeholder.svg" width="100%" alt="No public repositories found"></div>'
    repos = sorted(repos, key=lambda x:(x.get("stargazers_count",0),x.get("forks_count",0),x.get("updated_at","")), reverse=True)[:6]
    rows=["<table>"]
    for i in range(0,len(repos),2):
        rows.append("<tr>")
        for repo in repos[i:i+2]:
            name=repo["name"].replace("<","&lt;").replace(">","&gt;")
            desc=(repo.get("description") or "No description provided.").replace("<","&lt;").replace(">","&gt;")
            lang=repo.get("language") or "Code"; stars=repo.get("stargazers_count",0)
            rows.append(f'<td width="50%" valign="top">\n\n### [{name}]({repo["html_url"]})\n{desc}\n\n`{lang}` · ⭐ {stars}\n\n</td>')
        rows.append("</tr>")
    rows.append("</table>"); return "\n".join(rows)

def main():
    repos=get_repos(); DATA.parent.mkdir(parents=True,exist_ok=True); DATA.write_text(json.dumps(repos,indent=2),encoding="utf-8")
    text=README.read_text(encoding="utf-8"); replacement=START+"\n"+render(repos)+"\n"+END
    README.write_text(re.sub(re.escape(START)+r".*?"+re.escape(END),replacement,text,flags=re.S),encoding="utf-8")
    print(f"Updated profile with {len(repos)} public repositories.")

if __name__ == "__main__": main()
