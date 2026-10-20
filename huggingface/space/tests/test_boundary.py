import json
import sys
from pathlib import Path
from fastapi.testclient import TestClient
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import COOKIE, DemoService, create_app
from challenge import Unavailable


class StubService:
    def __init__(self):
        self.seen=[]
    def perform(self, key, action, name, variant):
        self.seen.append((key, action))
        return 'Synthetic stub only', [], {'decision': 'RETURN'}


def invoke(browser, action='run_scenario', data=None, session='identical-untrusted-hash'):
    return browser.post('/gradio_api/run/'+action, json={'data':data or ['Temporal expiry','Synthetic set 1'],'session_hash':session})


def test_cookie_isolation_even_with_identical_gradio_hash():
    service=StubService()
    app=create_app(service)
    with TestClient(app) as a, TestClient(app) as b:
        r=a.get('/')
        b.get('/')
        assert 'HttpOnly' in r.headers['set-cookie']
        assert r.headers['cache-control']=='no-store'
        assert a.cookies[COOKIE] != b.cookies[COOKIE]
        assert invoke(a).status_code==200
        assert invoke(b).status_code==200
        assert service.seen[0][0] != service.seen[1][0]
        # Sharing a Gradio session hash never selects the other visitor.
        assert invoke(a).status_code==200
        assert service.seen[0][0] == service.seen[2][0]


def test_cookie_origin_body_and_unneeded_routes_are_rejected():
    service=StubService()
    app=create_app(service)
    with TestClient(app) as b:
        assert invoke(b).status_code==401
        b.cookies.set(COOKIE,'forged')
        assert invoke(b).status_code==401
        b.cookies.clear()
        b.get('/')
        assert b.post('/gradio_api/run/run_scenario', json={'data':[]},headers={'origin':'https://attacker.example'}).status_code==403
        assert b.post('/gradio_api/run/run_scenario',content=b'x'*4097).status_code==413
        for route in ('call/run_scenario','queue/join','file=/etc/passwd','upload','proxy=https://example.com','stream/1'):
            assert b.get('/gradio_api/'+route).status_code==403
        assert not service.seen


def test_hosted_cookie_is_secure(monkeypatch):
    monkeypatch.setenv('SPACE_ID','owner/example')
    with TestClient(create_app(StubService())) as b:
        cookie=b.get('/').headers['set-cookie']
        assert 'Secure' in cookie and 'SameSite=none' in cookie


def test_service_rejects_input_before_network_and_caps_visitors():
    service=DemoService()
    try:
        service.perform('test','run','private-prompt','Synthetic set 1')
        assert False
    except Unavailable:
        pass
    assert service.visitors=={}
    for n in range(24):
        service.visitor(str(n))
    try:
        service.visitor('25')
        assert False
    except Unavailable:
        pass
    assert len(service.visitors)==24


def test_crafted_input_is_not_echoed_in_ui_or_logs(caplog):
    app=create_app(DemoService())
    with TestClient(app) as b:
        b.get('/')
        response=invoke(b,data=['SECRET-SENTINEL-OUTSIDE-SYNTHETIC','Synthetic set 1'])
        assert response.status_code==200
        assert 'Choose a supplied' in response.text
        assert 'SECRET-SENTINEL' not in response.text
        assert 'SECRET-SENTINEL' not in caplog.text
        assert not app.state.demo_service.visitors


def test_self_hosted_cookie_and_public_prefix(monkeypatch):
    import app as module
    monkeypatch.setattr(module, 'SELF_HOSTED', True)
    with TestClient(create_app(StubService()), base_url='https://challenge.aiadvantage.shop') as b:
        response = b.get('/')
        cookie = response.headers['set-cookie']
        assert 'Secure' in cookie and 'HttpOnly' in cookie
        assert 'SameSite=none' in cookie and 'Path=/demo' in cookie
        assert b.get('/config').json()['root'].endswith('/demo')
        assert b.get('/healthz').json() == {'ok': True, 'client_only': True}
