from pathlib import Path
import json,re
root=Path('/private/tmp/independent-audit-skills')
issues=[]
skills=list(root.glob('*/SKILL.md'))
for skill in skills:
    pieces=skill.read_text().split('---',2)
    if len(pieces)<3:
        issues.append([str(skill.relative_to(root)),'missing frontmatter']);continue
    name=re.search(r'^name: (.+)$',pieces[1],re.M)
    desc=re.search(r'^description: (.+)$',pieces[1],re.M)
    if not name or name[1]!=skill.parent.name or not desc:
        issues.append([str(skill.relative_to(root)),'name or description mismatch'])
    if not (skill.parent/'LICENSE').is_file():issues.append([str(skill),'missing license'])
for path in root.rglob('*.json'):
    try:json.loads(path.read_text())
    except Exception as exc:issues.append([str(path.relative_to(root)),str(exc)])
for path in root.rglob('*.md'):
    for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',path.read_text()):
        target=target.split('#')[0]
        if not target or '://' in target or target.startswith(('mailto:','<')):continue
        if not (path.parent/target).exists():issues.append([str(path.relative_to(root)),target])
print(json.dumps({'skills':len(skills),'json_files':len(list(root.rglob('*.json'))),'md_files':len(list(root.rglob('*.md'))),'issues':issues},indent=2))
raise SystemExit(bool(issues))
