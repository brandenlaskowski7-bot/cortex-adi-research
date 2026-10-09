"""Opt-in first-party E2E. Run app.py first; consumes TWO finite API slots.
No credentials or raw request headers are printed, saved, or returned.
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import sys
import httpx
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scenarios import SCENARIOS

BASE='http://127.0.0.1:7860'
report={'started_utc':datetime.now(timezone.utc).isoformat(),'kind':'first-party local UI HTTP to public HTTPS API','scenario_results':[], 'checks': []}
a=httpx.Client(base_url=BASE, timeout=120, trust_env=False)
b=httpx.Client(base_url=BASE, timeout=120, trust_env=False)
last={}
def call(browser, action, inputs):
    time.sleep(max(0, 8.2-(time.monotonic()-last.get(id(browser),0))))
    last[id(browser)]=time.monotonic()
    response=browser.post('/gradio_api/run/'+action,json={'data':inputs,'session_hash':'deliberately-identical-test-hash'})
    assert response.status_code==200, 'Local callback refused'
    payload=response.json()
    assert 'data' in payload, 'Callback failed'
    rendered=json.dumps(payload)
    assert 'Bearer ' not in rendered and '"token"' not in rendered and '"session_id"' not in rendered, 'Credential-shaped output'
    return payload['data']

try:
    assert a.get('/').status_code==200
    assert b.get('/').status_code==200
    for name in SCENARIOS:
        data=call(a,'run_scenario',[name,'Synthetic set 1'])
        if not data[0].startswith('Completed '):
            report['blocked_message']=data[0]
            raise RuntimeError('Scenario incomplete; see sanitized report')
        trace=data[1]['data']
        assert all(row[-1]=='Matched' for row in trace)
        report['scenario_results'].append({'scenario':name,'matched_steps':len(trace),'status':'PASS'})
        print(json.dumps(report['scenario_results'][-1]),flush=True)
    a_result=call(a,'run_scenario',['Temporal expiry','Synthetic set 1'])
    b_result=call(b,'run_scenario',['Supersession','Synthetic set 2'])
    assert b_result[0].startswith('Completed ')
    assert a_result[2]['receipt_id'] != b_result[2]['receipt_id']
    assert b_result[1]['data'][-1][5]=='synthetic-record-1'
    report['checks'].append('Distinct receipts for two cookie jars using identical Gradio session_hash')
    receipt=call(b,'retrieve_receipt',[])
    assert receipt[0].startswith('Receipt matched')
    report['checks'].append('Authenticated receipt retrieval equals original safe response')
    reset=call(a,'reset_session',[])
    assert reset[0].startswith('Reset completed')
    receipt=call(b,'retrieve_receipt',[])
    assert receipt[0].startswith('Receipt matched')
    report['checks'].append('Visitor A reset leaves visitor B receipt unchanged')
    assert a.post('/gradio_api/call/run_scenario',json={'data':[]}).status_code==403
    report['checks'].append('Alternate queue/call path blocked')
    report['checks'].append('No token, session_id, or Authorization in local UI responses')
    report['status']='PASS'
finally:
    cleanup=[]
    for browser in (a,b):
        try:
            result=call(browser,'reset_session',[])
            cleanup.append(result[0].startswith('Reset completed'))
        except Exception:
            cleanup.append(False)
        browser.close()
    report['cleanup_resets']=cleanup
    report['finished_utc']=datetime.now(timezone.utc).isoformat()
    print(json.dumps(report,indent=2),flush=True)
