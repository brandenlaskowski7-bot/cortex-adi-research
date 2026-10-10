"""Offline client lifecycle checks; no upstream sessions are created."""
import time
from datetime import datetime, timezone, timedelta
import httpx
import pytest
from app import DemoService
from challenge import Challenge, Visitor, Unavailable

def created():
    now = datetime.now(timezone.utc)
    return dict(token='TEST-SECRET', session_id='TEST-SESSION',
                created_at=now.isoformat(), expires_at=(now+timedelta(minutes=90)).isoformat(),
                idle_expires_at=(now+timedelta(minutes=15)).isoformat())

def test_creation_requires_bounded_lifetime_and_keeps_credentials_private():
    c=Challenge(httpx.MockTransport(lambda r:httpx.Response(201,json=created())))
    v=Visitor(); c.ensure_session(v)
    assert v.absolute_deadline-time.monotonic() <= 5400
    assert v.idle_deadline-time.monotonic() <= 900
    assert set(v.credentials)=={'token','session_id'}
    assert 'TEST-SECRET' not in repr(v)
    bad=created();bad.pop('expires_at')
    other=Challenge(httpx.MockTransport(lambda r:httpx.Response(201,json=bad)))
    with pytest.raises(Unavailable, match='lifetime'):
        other.ensure_session(Visitor())

def test_end_confirms_cleanup_then_clears_only_its_visitor():
    calls=[]
    def handler(r):
        calls.append(r)
        return httpx.Response(200,json={'decision':'RETURN','reason_category':'SESSION_ENDED','cleanup_complete':True})
    c=Challenge(httpx.MockTransport(handler))
    a=Visitor(credentials={'token':'TEST-SECRET','session_id':'A'},rows=[['trace']],receipts={'receipt':'test'})
    b=Visitor(credentials={'token':'OTHER-SECRET','session_id':'B'},rows=[['other']])
    c.request('end',a,{})
    assert not a.credentials and not a.rows and not a.receipts
    assert b.credentials['token']=='OTHER-SECRET' and b.rows==[['other']]
    assert calls[0].url.path=='/v1/challenge/end'

def test_expired_credentials_are_erased_before_any_network_request():
    calls=[]
    c=Challenge(httpx.MockTransport(lambda r:calls.append(r)))
    v=Visitor(credentials={'token':'TEST-SECRET','session_id':'A'},rows=[['trace']],receipts={'receipt':'test'},absolute_deadline=time.monotonic()-1,idle_deadline=time.monotonic()+100)
    with pytest.raises(Unavailable,match='time has ended'):
        c.request('reset',v,{})
    assert not calls and not v.credentials and not v.rows and not v.receipts

def test_upstream_revocation_erases_local_results():
    c=Challenge(httpx.MockTransport(lambda r:httpx.Response(401)))
    v=Visitor(credentials={'token':'TEST-SECRET','session_id':'A'},rows=[['trace']])
    with pytest.raises(Unavailable,match='revoked'):
        c.request('reset',v,{})
    assert not v.credentials and not v.rows

def test_sweeper_reclaims_closed_browser_cache_but_preserves_other_visitor():
    s=DemoService(); a=s.visitor('a');b=s.visitor('b')
    a.credentials={'token':'TEST-SECRET','session_id':'A'};a.rows=[['trace']];a.retained_until=time.monotonic()-1
    b.credentials={'token':'OTHER-SECRET','session_id':'B'}
    s.purge()
    assert 'a' not in s.visitors and not a.credentials and not a.rows
    assert s.visitors['b'] is b and b.credentials

def test_reset_does_not_extend_local_deadlines():
    c=Challenge(httpx.MockTransport(lambda r:httpx.Response(200,json={'decision':'RETURN','reason_category':'SESSION_RESET'})))
    now=time.monotonic()
    v=Visitor(credentials={'token':'TEST-SECRET','session_id':'A'},absolute_deadline=now+200,idle_deadline=now+100)
    c.request('reset',v,{})
    assert (v.absolute_deadline,v.idle_deadline)==(now+200,now+100)
