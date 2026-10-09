#!/usr/bin/env python3
"""Public API client and behavioral fixture runner. Python 3.9+, standard library.

No kernel code, Docker control, arbitrary shell execution, or private credentials.
Credentials exist only in process memory and are never included in the report.
"""
import argparse
import concurrent.futures
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

SAFE_FIELDS={'decision','reason_category','record_id','temporal_status','provenance_present','latency_ms','receipt_id'}

class Client:
    def __init__(self,base):
        self.base=base.rstrip('/')
        self.sessions={}
        self.receipts={}
        self.observations=[]

    def request(self,method,path,body=None,session=None,raw=None,headers=None):
        h={'Content-Type':'application/json'}
        if session:
            s=self.sessions[session]
            h.update({'X-Challenge-Session':s['session_id'],'Authorization':'Bearer '+s['token']})
        h.update(headers or {})
        data=raw.encode() if raw is not None else json.dumps(body).encode() if body is not None else None
        try:
            with urllib.request.urlopen(urllib.request.Request(self.base+path,data,h,method=method),timeout=25) as r:
                return r.status,json.load(r)
        except urllib.error.HTTPError as e:
            return e.code,json.loads(e.read())

    def initialize(self):
        for alias in ['a','b']:
            status,data=self.request('POST','/v1/challenge/session',{'synthetic':True,'scopes':['synthetic-scope-1','synthetic-scope-2']})
            assert status==201,(status,data)
            self.sessions[alias]=data

    def reset(self):
        for alias in self.sessions:
            status,data=self.request('POST','/v1/challenge/reset',{},alias)
            assert status==200,(status,data)
        self.receipts={}

    def step(self,step,restart=None):
        if step.get('action')=='restart':
            if restart is None:
                return {'status':'NOT_TESTED','reason':'Operator restart required'}
            restart();return {'status':'PASS','action':'operator_restart'}
        if step.get('action')=='parallel':
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                results=list(pool.map(lambda child:self.step(child,restart),step['steps']))
            decisions=sorted(r['response']['decision'] for r in results)
            assert decisions==sorted(step['expected_decisions']),(decisions,step['expected_decisions'])
            return {'status':'PASS','parallel':results}
        path=step['path']
        if step.get('receipt_from'):path='/v1/challenge/result/'+self.receipts[step['receipt_from']]['receipt_id']
        status,data=self.request(step.get('method','POST'),path,step.get('body'),step.get('session','a'),step.get('raw'),step.get('headers'))
        assert set(data)<=SAFE_FIELDS,('unexpected_public_fields',sorted(set(data)-SAFE_FIELDS))
        assert status==step.get('expected_status',200),(status,data,step)
        for k,v in step.get('expected',{}).items():assert data.get(k)==v,(k,v,data)
        if 'same_as' in step:assert data==self.receipts[step['same_as']],('non_idempotent',data)
        if status==200:assert 'receipt_id' in data,('missing_receipt',data)
        if step.get('save'):self.receipts[step['save']]=data
        return {'status':'PASS','http_status':status,'response':data}

    def run(self,fixture,restart=None):
        self.reset()
        steps=[]
        for step in fixture['steps']:
            result=self.step(step,restart)
            steps.append(result)
            if result['status']=='NOT_TESTED':break
        result={'id':fixture['id'],'status':'NOT_TESTED' if any(s['status']=='NOT_TESTED' for s in steps) else 'PASS','steps':steps}
        self.observations.append(result)
        return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument('fixture',type=Path)
    p.add_argument('--base',default='http://127.0.0.1:8808')
    p.add_argument('--operator-restart',action='store_true',help='Pause for the operator to restart their own sandbox')
    args=p.parse_args()
    c=Client(args.base);c.initialize()
    def restart():input('Restart only your challenge service, then press Enter: ')
    files=sorted(args.fixture.glob('*.json')) if args.fixture.is_dir() else [args.fixture]
    for file in files:
        try:result=c.run(json.loads(file.read_text()),restart if args.operator_restart else None)
        except Exception as e:
            print(json.dumps({'id':file.stem,'status':'FAIL','error':str(e)}));raise SystemExit(1)
        print(json.dumps(result))
    tested=sum(r['status']=='PASS' for r in c.observations)
    print(json.dumps({'passed':tested,'not_tested':len(c.observations)-tested,'total':len(c.observations)}))

if __name__=='__main__':main()
