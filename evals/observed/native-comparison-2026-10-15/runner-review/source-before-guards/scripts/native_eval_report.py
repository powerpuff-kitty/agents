#!/usr/bin/env python3
"""Report a frozen native trial roster offline, retaining missing/failed outcomes.

Source bytes and observed instruction events are not provider-token savings.
Independent acceptance can be attached only to the exact result artifact hash.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import statistics


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def instruction_events(messages):
    roles, skills, tools, states, reads = Counter(), Counter(), Counter(), Counter(), []
    result_failures = 0
    skill_text_bytes = 0
    for rows in messages.values():
        for row in rows:
            if row.get('type') == 'user':
                for attachment in row.get('skills', []):
                    if attachment.get('text'):
                        skills[attachment['id']] += 1
                        skill_text_bytes += len(attachment['text'].encode())
            if row.get('type') == 'skill':
                skills[row['skill']] += 1
                skill_text_bytes += len(row.get('text', '').encode())
            if row.get('type') == 'assistant':
                roles[row['agent']] += 1
                for part in row.get('content', []):
                    if part.get('type') != 'tool':
                        continue
                    tool, state = part['name'], part['state']
                    tools[tool] += 1
                    states[state['status']] += 1
                    metadata = state.get('metadata', {})
                    if state.get('error') or metadata.get('error') is True or (isinstance(metadata.get('exit'), int) and metadata['exit'] != 0):
                        result_failures += 1
                    if tool == 'skill' and state['status'] == 'completed':
                        name = state.get('input', {}).get('id')
                        if name:
                            skills[name] += 1
                    if tool == 'read':
                        path = state.get('input', {}).get('path', '')
                        if '/.agents/skills/' in path or '/.opencode/agents/' in path:
                            reads.append({'path': path, 'status': state['status']})
    return {'assistant_messages_by_agent': dict(roles), 'skill_events': dict(skills),
            'skill_message_utf8_bytes': skill_text_bytes, 'tool_calls': dict(tools),
            'tool_statuses': dict(states), 'tool_result_failures': result_failures, 'instruction_file_reads': reads,
            'limits': 'Events can overlap attachments and skill calls; not distinct token loads or proof of adherence.'}


def summarize(root, review_path=None):
    root = Path(root)
    if sha(root / 'plan.json') != (root / 'plan.sha256').read_text().strip():
        raise ValueError('Plan identity mismatch')
    plan = json.loads((root / 'plan.json').read_text())
    decisions = {}
    if review_path:
        review = json.loads(Path(review_path).read_text())
        for item in review['runs']:
            if item['id'] in decisions or item['acceptance'] not in {'pass', 'fail', 'blocked', 'unverified'}:
                raise ValueError('Invalid/duplicate independent decision')
            decisions[item['id']] = item
        unknown = decisions.keys() - {item['id'] for item in plan['runs']}
        if unknown:
            raise ValueError('Review refers to unplanned runs')
    rows, fixtures = [], defaultdict(set)
    groups = defaultdict(list)
    for entry in plan['runs']:
        run = root / entry['id']
        fixtures[entry['case']].add(entry['fixture_sha256'])
        row = {'id': entry['id'], 'case': entry['case'], 'mode': entry['mode'], 'repeat': entry['repeat'],
               'status': 'not_run', 'acceptance': 'unverified', 'usage': None, 'seconds': None,
               'instruction_events': None}
        if (run / 'result.json').exists():
            result = json.loads((run / 'result.json').read_text())
            if result['entry'] != entry:
                raise ValueError('Result/plan mismatch: ' + entry['id'])
            row.update({k: result.get(k) for k in ['status', 'usage', 'seconds', 'invariants']})
            row['result_sha256'] = sha(run / 'result.json')
            if entry['id'] in decisions:
                decision = decisions[entry['id']]
                if decision['result_sha256'] != row['result_sha256']:
                    raise ValueError('Review applies to another result: ' + entry['id'])
                row['acceptance'] = decision['acceptance']
                row['review_notes'] = decision.get('notes', '')
            if (run / 'messages.json').exists():
                row['instruction_events'] = instruction_events(json.loads((run / 'messages.json').read_text()))
            if (run / 'preflight.json').exists():
                inventory = json.loads((run / 'preflight.json').read_text())['inventory']
                row['registered_source_bytes'] = {kind: sum(v['utf8_bytes'] for v in inventory[kind].values())
                                                  for kind in ['skills', 'agents']}
        elif entry['id'] in decisions:
            decision = decisions[entry['id']]
            if decision['acceptance'] != 'unverified' or decision.get('result_sha256') is not None:
                raise ValueError('Cannot certify an absent result')
        rows.append(row)
        groups[(entry['case'], entry['mode'])].append(row)
    stats = []
    for (case, mode), values in sorted(groups.items()):
        item = {'case': case, 'mode': mode, 'planned': len(values),
                'statuses': dict(Counter(v['status'] for v in values)),
                'independent_acceptance': dict(Counter(v['acceptance'] for v in values)), 'metrics': {}}
        for key in ['input', 'output', 'cache_read', 'cache_write', 'reported_cost', 'seconds']:
            samples = [v['seconds'] if key == 'seconds' else (v.get('usage') or {}).get(key) for v in values]
            observed = [x for x in samples if isinstance(x, (int, float))]
            item['metrics'][key] = {'observed': len(observed), 'missing': len(samples) - len(observed),
                                    'mean': statistics.mean(observed) if observed else None,
                                    'min': min(observed) if observed else None,
                                    'max': max(observed) if observed else None}
        stats.append(item)
    return {'format_version': 1, 'plan_sha256': sha(root / 'plan.json'), 'planned': len(rows),
            'same_starting_file_hashes_per_case': {k: len(v) == 1 for k, v in fixtures.items()},
            'runs': rows, 'groups': stats, 'review_sha256': sha(Path(review_path)) if review_path else None,
            'limits': ['Built-in build is explicitly pinned for ordinary/skill controls; named-agent changes that primary.',
                       'Role and skill treatments are different interventions, not a context-only savings experiment.',
                       'Source bytes, instruction events, host-reported tokens/cache and billed costs are distinct.',
                       'Unexposed auxiliary calls/settings remain unknown; sample sizes do not establish statistical reliability.',
                       'No task success is inferred from host outcome, artifact invariants or a lower token count.']}


def markdown(report):
    lines = ['# Matched native trial measurements', '',
             '| Task | Mode | Planned | Status | Acceptance | Input mean (range) | Cost mean |',
             '| --- | --- | ---: | --- | --- | ---: | ---: |']
    for group in report['groups']:
        metric = group['metrics']['input']; cost = group['metrics']['reported_cost']['mean']
        count = 'unknown' if metric['mean'] is None else f"{metric['mean']:.1f} ({metric['min']}–{metric['max']}); {metric['missing']} missing"
        lines.append(f"| {group['case']} | {group['mode']} | {group['planned']} | {group['statuses']} | {group['independent_acceptance']} | {count} | {cost if cost is not None else 'unknown'} |")
    lines.extend(['', *[f'- {limit}' for limit in report['limits']], ''])
    return '\n'.join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True, type=Path, help='Existing frozen trial directory')
    p.add_argument('--review', type=Path)
    args = p.parse_args()
    report = summarize(args.output, args.review)
    (args.output / 'measurements.json').write_text(json.dumps(report, indent=2) + '\n')
    (args.output / 'measurements.md').write_text(markdown(report))
    print(json.dumps({'planned': report['planned'], 'groups': len(report['groups']),
                      'independent_decisions': sum(row['acceptance'] != 'unverified' for row in report['runs'])}))


if __name__ == '__main__':
    main()
