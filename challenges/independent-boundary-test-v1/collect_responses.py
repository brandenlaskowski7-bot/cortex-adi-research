#!/usr/bin/env python3
"""Collect raw model text without repairing or normalizing it."""
import argparse,json,pathlib
from boundary_test import fixtures
p=argparse.ArgumentParser(); p.add_argument('--raw-dir',required=True); p.add_argument('--out',required=True); a=p.parse_args()
with open(a.out,'x',encoding='utf8') as out:
    for c in fixtures():
        path=pathlib.Path(a.raw_dir)/(c['id']+'.txt')
        if path.is_file(): out.write(json.dumps({'case_id':c['id'],'raw_output':path.read_text(encoding='utf8')},ensure_ascii=False)+'\n')
        else: print('Missing, will score invalid:',path)
