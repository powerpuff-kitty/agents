#!/usr/bin/env python3
"""Check supported Markdown paths and source-derived catalog counts; no network."""
import argparse
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def check(root,skills=None):
 errors=[];checked=0
 for base in [root]+([skills] if skills else []):
  for file in sorted(base.rglob('*.md')):
   if any(x in file.relative_to(base).parts for x in ['.git','dist','__pycache__']):continue
   checked+=1
   for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
    target=target.split('#')[0].strip('<>')
    if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:',target) or any(x in target for x in ['<','>','{','}']):continue
    if not (file.parent/target).exists():errors.append(f'{file.relative_to(base)}: missing {target}')
 counts={kind:len(list((root/kind).glob('*/agent.json' if kind=='agents' else '*.json'))) for kind in ['agents','teams','packs']}
 text=(root/'README.md').read_text()
 for expected in [f"profiles-{counts['agents']}",f"{counts['agents']} profiles",f"{counts['teams']} team workflows",f"{counts['packs']} optional packs"]:
  if expected not in text:errors.append('README count missing/stale: '+expected)
 if skills:
  n=len(list(skills.glob('*/SKILL.md')));text=(skills/'README.md').read_text()
  for expected in [f'skills-{n}',f'{n} portable task procedures']:
   if expected not in text:errors.append('Skills README count missing/stale: '+expected)
 return {'passed':not errors,'markdown_files':checked,'counts':counts,'errors':errors,'limitations':['supported local path syntax only; no external URL, fragment, rendering or prose-truth verification']}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--skills-source',type=Path);a=p.parse_args();result=check(ROOT,a.skills_source.resolve() if a.skills_source else None);print(json.dumps(result,indent=2));raise SystemExit(0 if result['passed'] else 1)
