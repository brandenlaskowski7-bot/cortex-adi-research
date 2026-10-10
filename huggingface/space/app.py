"""Gradio thin client for the PUBLIC synthetic API. Run: python app.py."""
import hashlib
import hmac
import json
import os
import re
import secrets
import threading
import time
import asyncio
from contextlib import asynccontextmanager
from urllib.parse import urlsplit

os.environ['GRADIO_ANALYTICS_ENABLED'] = 'False'
import gradio as gr
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

from challenge import Challenge, Unavailable, Visitor
from scenarios import SCENARIOS, VARIANTS, steps

COOKIE = 'cortex_demo_visitor'
COLUMNS = ['Step', 'HTTP', 'Decision', 'Reason category', 'Temporal status', 'Record', 'Provenance', 'Receipt ID', 'Expected outcome']
GITHUB = 'https://github.com/brandenlaskowski7-bot/cortex-adi-research'
DOCS = GITHUB + '/blob/feature/huggingface-memory-challenge-demo'


class DemoService:
    def __init__(self, client=None):
        self.client = client or Challenge()
        self.visitors = {}
        self.guard = threading.RLock()
        self.workers = threading.BoundedSemaphore(2)

    def visitor(self, key):
        with self.guard:
            self.purge()
            if key not in self.visitors:
                if len(self.visitors) >= 24:
                    raise Unavailable('This demo is busy. Try later: ended and expired visits are automatically reclaimed. Refreshing repeatedly will not help.')
                self.visitors[key] = Visitor()
            return self.visitors[key]

    def purge(self):
        with self.guard:
            for key, visitor in list(self.visitors.items()):
                if visitor.lock.acquire(blocking=False):
                    try:
                        if time.monotonic() >= visitor.retained_until:
                            visitor.forget()
                            del self.visitors[key]
                    finally:
                        visitor.lock.release()

    def display_lifetime(self, key):
        # No network request and no renewal of the backend inactivity timer.
        with self.guard:
            self.purge()
            visitor = self.visitors.get(key)
            if not visitor or not visitor.credentials:
                return 'No active visit. Run a scenario to start a new synthetic session.', False
            remaining = max(0, int(min(visitor.absolute_deadline, visitor.idle_deadline) - time.monotonic()))
            return f'This visit ends in at most {remaining // 60}m {remaining % 60}s. Activity may extend the idle limit, never the 90-minute maximum.', True

    def perform(self, key, action, name='Temporal expiry', variant=VARIANTS[0]):
        # Validate enums before creating a visitor or making any network request.
        if action not in ('run', 'reset', 'receipt', 'end'):
            raise Unavailable('Choose a supplied action.')
        try:
            plan = steps(name, variant) if action == 'run' else []
        except (ValueError, TypeError):
            raise Unavailable('Choose a supplied synthetic scenario and set.') from None
        with self.guard:
            visitor = self.visitor(key)
            if not visitor.lock.acquire(blocking=False):
                raise Unavailable('Your previous action is still running. Please wait.')
        admitted = False
        try:
            now = time.monotonic()
            if now < visitor.next_action:
                raise Unavailable('Please wait eight seconds between actions. The lab has shared limits.')
            visitor.next_action = now + 8
            admitted = self.workers.acquire(blocking=False)
            if not admitted:
                raise Unavailable('Two visitors are already running checks. Please try again shortly.')
            if action == 'run':
                self.client.ensure_session(visitor)
                visitor.rows = []
                for step in plan:
                    status, result = self.client.request(step['operation'], visitor, step['body'])
                    if step['operation'] == 'reset' and status == 200:
                        visitor.receipts.clear()
                    if result.get('receipt_id'):
                        visitor.receipts[result['receipt_id']] = result
                    matches = status == step['status'] and result['decision'] == step['expected']
                    visitor.rows.append(row(step['label'], status, result, 'Matched' if matches else 'MISMATCH'))
                    if not matches:
                        return 'Observed result differs from the contract. Stop here and use the failure-report link with this synthetic trace.', visitor.rows, result
                return f'Completed {name}: {len(plan)} observed steps matched the expected decisions. These are live API observations, not an independent audit.', visitor.rows, result
            if action == 'reset':
                status, result = self.client.request('reset', visitor, {})
                if status == 200:
                    visitor.receipts.clear()
                    visitor.rows = [row('Reset your session', status, result, 'Matched' if result['decision'] == 'RETURN' else 'MISMATCH')]
                return 'Reset completed. Your original time limit, rate budget, and session slot remain in use.' if status == 200 else 'Reset was refused; your session was not cleared.', visitor.rows, result
            if action == 'end':
                status, result = self.client.request('end', visitor, {})
                if status == 200:
                    visitor.retained_until = visitor.next_action
                    return 'Session ended. The sandbox confirmed cleanup and released your slot. Local credentials and results were cleared.', [], {}
                return 'Session end was not confirmed. Automatic expiry still applies.', visitor.rows, {}
            if not visitor.receipts:
                raise Unavailable('Run a scenario first. Reset removes prior receipts.')
            receipt = next(reversed(visitor.receipts))
            status, result = self.client.request('receipt', visitor, receipt=receipt)
            same = status == 200 and result == visitor.receipts[receipt]
            return ('Receipt matched the original response. It records that operation; it does not re-evaluate current eligibility.' if same else 'Receipt did not match or is no longer available.'), visitor.rows, result
        except Unavailable as exc:
            # Keep a partial trace, but never label an incomplete run successful.
            return 'Not completed: ' + str(exc), visitor.rows, {}
        finally:
            if admitted:
                self.workers.release()
            visitor.lock.release()


def row(label, status, result, expected):
    return [label, status, result['decision'], result.get('reason_category', '—'), result.get('temporal_status', '—'), result.get('record_id', '—'), str(result.get('provenance_present', '—')), result.get('receipt_id', '—'), expected]


CSS = '''
.gradio-container { max-width: 1180px !important; margin: auto; }
#hero { padding: 28px 30px; border-radius: 18px; background: #102a43; color: #f0f6fc; margin-bottom: 20px; }
#hero h1, #hero p { color: #f0f6fc; }
#hero h1 { font-size: 2.2rem; line-height: 1.15; }
#eyebrow { color: #6ee7c2; font-size: .8rem; letter-spacing: .12em; font-weight: 700; }
#result { border-left: 4px solid #20a984; padding: 12px 18px; }
'''


def create_app(service=None):
    service = service or DemoService()
    secret = secrets.token_bytes(32)
    def issue_cookie():
        payload = str(int(time.time())) + '.' + secrets.token_urlsafe(32)
        return payload + '.' + hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()
    def valid_cookie(value):
        if not isinstance(value, str) or len(value) > 160:
            return False
        try:
            stamp, nonce, sig = value.split('.')
            return (0 <= time.time() - int(stamp) < 86400 and len(nonce) == 43 and
                    hmac.compare_digest(sig, hmac.new(secret, f'{stamp}.{nonce}'.encode(), hashlib.sha256).hexdigest()))
        except (ValueError, TypeError):
            return False

    @asynccontextmanager
    async def lifespan(server):
        async def clean_visitors():
            while True:
                await asyncio.sleep(15)
                if hasattr(service, 'purge'):
                    service.purge()
        task = asyncio.create_task(clean_visitors())
        try:
            yield
        finally:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    server = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=lifespan)
    server.state.demo_service = service

    @server.middleware('http')
    async def boundary(request: Request, call_next):
        path = request.url.path
        value = request.cookies.get(COOKIE)
        valid = valid_cookie(value)
        # Only direct request/response callbacks are enabled. No shared Gradio
        # state or queues are used, so a client-supplied session_hash grants nothing.
        if path.startswith('/gradio_api/'):
            if not (path.startswith('/gradio_api/run/') or path.startswith('/gradio_api/heartbeat/')):
                return JSONResponse({'detail': 'This demo exposes only its bounded UI actions.'}, status_code=403)
            if not valid:
                return JSONResponse({'detail': 'Open the app page first. Enable cookies, or open the Space in its own tab.'}, status_code=401)
            origin = request.headers.get('origin')
            if origin and urlsplit(origin).netloc != request.headers.get('host'):
                return JSONResponse({'detail': 'Cross-origin actions are not accepted.'}, status_code=403)
        if request.method == 'POST':
            # Bound actual streamed bytes, including bodies without Content-Length.
            raw = bytearray()
            async for part in request.stream():
                raw.extend(part)
                if len(raw) > 4096:
                    return JSONResponse({'detail': 'Request too large.'}, status_code=413)
            request._body = bytes(raw)
        response = await call_next(request)
        if path == '/' and request.method == 'GET' and not valid:
            response.set_cookie(COOKIE, issue_cookie(), max_age=86400, httponly=True,
                                secure=bool(os.environ.get('SPACE_ID')) or request.url.scheme == 'https',
                                samesite='none' if os.environ.get('SPACE_ID') else 'lax', path='/')
        if path == '/' or path.startswith('/gradio_api/run/'):
            response.headers['Cache-Control'] = 'no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response

    def invoke(request, action, name='Temporal expiry', variant=VARIANTS[0]):
        value = request.cookies.get(COOKIE)
        if not valid_cookie(value):
            return 'Open the app in its own tab and allow cookies, then reload.', [], {}
        try:
            return service.perform(value, action, name, variant)
        except Unavailable as exc:
            return str(exc), [], {}
        except Exception:
            # Never reflect exception repr, headers, input, or credentials.
            return 'The demo could not finish this action. No automatic retry was made. Please report the scenario name only.', [], {}

    def run_scenario(name, variant, request: gr.Request):
        return invoke(request, 'run', name, variant)
    def reset_session(request: gr.Request):
        return invoke(request, 'reset')
    def retrieve_receipt(request: gr.Request):
        return invoke(request, 'receipt')
    def end_session(request: gr.Request):
        return invoke(request, 'end')
    def session_lifetime(request: gr.Request):
        value = request.cookies.get(COOKIE)
        if not valid_cookie(value):
            return 'Open this app in its own tab and allow cookies.', gr.skip(), [], {}
        message, active = service.display_lifetime(value)
        return (message, gr.skip(), gr.skip(), gr.skip()) if active else (message, 'No active visit. Local results are cleared.', [], {})
    def describe(name, variant):
        try:
            plan = steps(name, variant)
            return SCENARIOS[name], [{'step': s['label'], 'operation': s['operation'], 'synthetic_body': s['body'], 'expected_decision': s['expected']} for s in plan]
        except (ValueError, TypeError):
            return 'Choose a supplied scenario.', []

    with gr.Blocks(title='Cortex · Governed Memory Challenge', analytics_enabled=False) as demo:
        gr.HTML('<div id="hero"><div id="eyebrow">CORTEX / DEVELOPER LAB / v0.1</div><h1>When should memory be trusted?</h1><p>Explore six small, synthetic experiments. Watch the public API return, hold, deny, expire, or supersede a record — with a receipt for each decision.</p></div>')
        gr.Markdown('**Synthetic records only · No language model · Public API client**\n\nPick a scenario, inspect the synthetic inputs, then run it. Each run resets **only your visitor session**. No names, prompts, files, secrets, or real-world records can be entered.')
        with gr.Row():
            with gr.Column(scale=2):
                scenario = gr.Dropdown(list(SCENARIOS), value='Temporal expiry', label='1 · Choose an experiment', allow_custom_value=False)
                variant = gr.Radio(VARIANTS, value=VARIANTS[0], label='2 · Choose a synthetic subject/key set')
                guidance = gr.Markdown(SCENARIOS['Temporal expiry'])
                run = gr.Button('Run synthetic scenario', variant='primary')
                gr.Markdown('A session starts only when you run. **90-minute maximum · 15-minute idle cutoff · Automatic cleanup.** End your session when finished. Reset clears the experiment without extending your visit. The lab allows 32 concurrent sessions; this demo allows 24 visitors and two concurrent actions.')
                lifetime = gr.Markdown('No active visit. The timer begins when you run a scenario.')
            with gr.Column(scale=3):
                status = gr.Markdown('**Ready to explore.** No live operation has run yet.', elem_id='result')
                with gr.Accordion('Inspect the exact synthetic requests', open=False):
                    preview = gr.JSON(describe('Temporal expiry', VARIANTS[0])[1], label='Request preview — not results')
        trace = gr.Dataframe(headers=COLUMNS, datatype=['str'] * len(COLUMNS), interactive=False, label='Observed decision trace', wrap=True)
        with gr.Row():
            receipt = gr.Button('Verify latest receipt')
            reset = gr.Button('Reset my synthetic session')
            end = gr.Button('End session and erase my experiment')
        with gr.Accordion('Latest safe response', open=False):
            detail = gr.JSON(label='Public response fields only')
        gr.Markdown('''### Read the result
**RETURN** on admission means accepted; on query it means current. **HOLD** means an unresolved candidate or key; it is often the intended result. **DENY** refuses an operation, including an undeclared scope. **HISTORICAL** means expired. **SUPERSEDED** identifies a replaced predecessor. **UNRESOLVED** means no eligible match.

A receipt preserves the original response. Provenance presence means a synthetic source reference exists, not that an assertion is true. Scenario matching checks expected HTTP status and decision; it is not exhaustive verification of every invariant.

### Limits and privacy
Structured symbolic synthetic records only; no free-text or LLM inference, no production Cortex, and no independent security audit. This Space is a thin HTTPS client, with no private kernel, production memory, or deployment access. Service availability and capacity are finite. Busy or full responses stop the run without automatic retries.

Challenge credentials stay in server memory and are never displayed or logged. A signed HttpOnly cookie binds your browser; Gradio session hashes are not credentials. Cookies expire after 24 hours, while API access lasts at most 90 minutes and ends after 15 idle minutes. Closing the browser does not stop the sandbox cleanup timer. Valid record/query activity renews only the idle limit; reset, receipt reads, and this display do not. End session revokes access immediately and confirms cleanup before releasing capacity. Expiry revokes access at the deadline, with cleanup attempted every 10 seconds and retried if needed. Failed cleanup keeps the slot unavailable.

The Space clears expired credentials and its cached trace within 15 seconds, even after a browser closes. An open browser clears its display on the next timer update; offline tabs or saved screenshots cannot be remotely erased. Managed synthetic stores and receipts are deleted; this is not a guarantee of forensic disk erasure or deletion of separately retained host backups or provider connection metadata. No production memory is present. This client requires the lifecycle v0.2 API.
''')
        gr.Markdown(f'[ADI paper · DOI 10.5281/zenodo.23265200](https://doi.org/10.5281/zenodo.23265200) · [Public API contract]({DOCS}/challenges/governed-memory/API.md) · [GitHub challenge]({GITHUB}/tree/main/challenges/governed-memory) · [v0.1 release]({GITHUB}/releases/tag/memory-challenge-v0.1) · [Report a synthetic failure]({GITHUB}/issues/new?template=challenge-failure.yml)')
        for component in (scenario, variant):
            component.change(describe, [scenario, variant], [guidance, preview], queue=False, preprocess=False, api_visibility='private')
        run.click(run_scenario, [scenario, variant], [status, trace, detail], queue=False, preprocess=False, api_name='run_scenario', api_visibility='private')
        reset.click(reset_session, [], [status, trace, detail], queue=False, api_name='reset_session', api_visibility='private')
        receipt.click(retrieve_receipt, [], [status, trace, detail], queue=False, api_name='retrieve_receipt', api_visibility='private')
        end.click(end_session, [], [status, trace, detail], queue=False, api_name='end_session', api_visibility='private')
        gr.Timer(15).tick(session_lifetime, [], [lifetime, status, trace, detail], queue=False, api_name='session_lifetime', api_visibility='private')
    return gr.mount_gradio_app(server, demo, path='/', show_error=False, enable_monitoring=False,
                               mcp_server=False, ssr_mode=False, footer_links=[], run_history=False,
                               theme=gr.themes.Soft(primary_hue='teal', neutral_hue='slate'), css=CSS)


app = create_app()
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0' if os.environ.get('SPACE_ID') else '127.0.0.1', port=7860,
                access_log=False, log_level='warning', proxy_headers=False)
