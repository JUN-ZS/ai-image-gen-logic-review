#!/usr/bin/env python3
"""Verify R10.1 package: ACCEPT root==complete, job plan, PNG SHAs, runner SHA."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

def main(root: Path):
    errs = []
    acc_root = root / 'ACCEPT_R10_1.json'
    acc_c = root / 'complete' / 'ACCEPT_R10_1.json'
    if not acc_root.exists() or not acc_c.exists():
        print('FAIL missing ACCEPT'); return 2
    if acc_root.read_bytes() != acc_c.read_bytes():
        errs.append('root ACCEPT != complete ACCEPT')
    acc = json.loads(acc_c.read_text())
    man = json.loads((root / 'complete' / 'MANIFEST_SHA256_R10_1.json').read_text())
    if sha(root / 'run_r10_1.py') != acc['runner']['sha256']:
        errs.append('runner file sha != ACCEPT.runner.sha256')
    if sha(acc_c) != man['accept_sha256']:
        errs.append('ACCEPT sha != MANIFEST.accept_sha256')
    if len(acc['jobs']) != len(acc['job_plan']):
        errs.append(f"jobs {len(acc['jobs'])} != plan {len(acc['job_plan'])}")
    for j, p in zip(acc['jobs'], acc['job_plan']):
        if j['tag'] != p['tag'] or j['method'] != p['method']:
            errs.append(f"job order mismatch {j} vs {p}")
    for j in acc['jobs']:
        if j['status'] != 'OK':
            continue
        p = Path(j['path']) if j.get('path') else root / 'complete' / f"{j['tag']}_{j['method']}.png"
        if not p.exists():
            p = root / 'complete' / f"{j['tag']}_{j['method']}.png"
        if not p.exists():
            errs.append(f"missing png {j['tag']}_{j['method']}")
            continue
        if sha(p) != j['sha256']:
            errs.append(f"sha mismatch {p.name}")
    # inputs
    for im in acc['input_manifest']:
        ip = root / 'inputs' / im['name']
        if not ip.exists():
            errs.append(f"missing input {im['name']}")
        elif sha(ip) != im['sha256']:
            errs.append(f"input sha mismatch {im['name']}")
    if errs:
        print('VERIFY FAIL')
        for e in errs:
            print(' -', e)
        return 1
    print('VERIFY PASS')
    print('runner', acc['runner']['sha256'])
    print('accept', man['accept_sha256'])
    print('jobs', acc['n_jobs'], 'formal', acc['n_pass_formal'], 'skip', acc['n_skip'])
    return 0

if __name__ == '__main__':
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    raise SystemExit(main(root))
