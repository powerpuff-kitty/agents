#!/usr/bin/env python3
"""Verify retained evidence and regenerate reports in memory, without inference.

Hashes establish consistency, not reviewer identity, truth or model reliability.
The explicit index avoids reinterpreting older evidence formats as current runs.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

import native_eval_report

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value:
                raise ValueError('Duplicate JSON key: ' + key)
            value[key] = item
        return value

    def invalid(value):
        raise ValueError('Nonfinite JSON value: ' + value)

    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs, parse_constant=invalid)


def child(root, name):
    path = PurePosixPath(name)
    if not name or not path.parts or path.is_absolute() or '..' in path.parts or str(path) != name or '\\' in name:
        raise ValueError('Unsafe evidence path: ' + name)
    candidate = root.joinpath(*path.parts)
    for part in [candidate, *candidate.parents]:
        if part == root.parent:
            break
        if part.is_symlink():
            raise ValueError('Linked evidence: ' + name)
    return candidate


def verify_bundle(root, spec):
    bundle = child(root, spec['path'])
    manifest = load(bundle / 'manifest.json')['files_sha256']
    actual = {}
    for path in bundle.rglob('*'):
        if path.is_symlink():
            raise ValueError('Linked evidence: ' + str(path))
        if path.is_file() and path != bundle / 'manifest.json':
            actual[path.relative_to(bundle).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not manifest or actual != manifest:
        raise ValueError('Evidence manifest differs: ' + spec['path'])
    for name in manifest:
        child(bundle, name)
        if name.endswith('.json'):
            load(child(bundle, name))
    reports = []
    for report in spec['reports']:
        trials = child(bundle, report['path'])
        review = child(bundle, report['review'])
        plan = load(trials / 'plan.json')
        ids = [entry['id'] for entry in plan['runs']]
        if not ids or len(set(ids)) != len(ids):
            raise ValueError('Empty/duplicate planned run IDs')
        for run_id in ids:
            if '/' in run_id:
                raise ValueError('Run ID must be a single directory name')
            child(trials, run_id)
        load(review)
        fresh = native_eval_report.summarize(trials, review)
        stored = load(trials / 'measurements.json')
        if fresh != stored:
            raise ValueError('Retained report differs from regenerated evidence: ' + report['path'])
        if (trials / 'measurements.md').read_text() != native_eval_report.markdown(fresh):
            raise ValueError('Retained Markdown report differs: ' + report['path'])
        reports.append({'path': report['path'], 'planned': fresh['planned'],
                        'classified': sum(row['acceptance'] != 'unverified' for row in fresh['runs'])})
    return {'path': spec['path'], 'artifacts': len(actual), 'reports': reports}


def verify(root=ROOT, index=None):
    root = Path(root).resolve()
    index = Path(index) if index else root / 'evals/evidence-checks.json'
    specs = load(index)['bundles']
    paths = [spec['path'] for spec in specs]
    if not specs or len(paths) != len(set(paths)):
        raise ValueError('Empty/duplicate evidence bundles')
    return {'verified': True, 'model_calls': 0,
            'bundles': [verify_bundle(root, spec) for spec in specs],
            'limits': 'Integrity and report consistency only; no authentication of reviewers, task judgments or exhaustive billing.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--index', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.root, args.index), indent=2))
    except (ValueError, KeyError, OSError, TypeError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
