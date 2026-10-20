"""Fixed synthetic examples derived from the public v0.1 contract/fixtures."""
from copy import deepcopy

SCENARIOS = {
    'Temporal expiry': 'A fact is current before its expiry, historical at the exact expiry boundary, and absent before its effective time.',
    'Supersession': 'An explicit correction replaces its predecessor from the correction date. An earlier query still sees the predecessor.',
    'Conflict / HOLD': 'A different value without a valid correction is held. Current recall also holds instead of silently choosing a winner.',
    'Provenance': 'A candidate without a synthetic source is held. A source reference records provenance presence, not real-world truth.',
    'Scope isolation': 'A fact in scope 1 is absent from scope 2. Undeclared scope 3 is denied. Both are expected protections.',
    'Reset': 'Reset clears only your session records, receipts, and replay keys. It preserves credentials, scopes, rate budgets, and the occupied session slot.',
}
VARIANTS = ('Synthetic set 1', 'Synthetic set 2', 'Synthetic set 3')


def steps(name, variant):
    if name not in SCENARIOS or variant not in VARIANTS:
        raise ValueError('Select one of the supplied synthetic scenarios and sets.')
    n = VARIANTS.index(variant) + 1
    record = dict(record_id='synthetic-record-1', subject=f'synthetic-subject-{n}', scope='synthetic-scope-1', key=f'synthetic-key-{n}', value='synthetic-value-1', provenance='synthetic-source-1', effective_at='2026-01-01T00:00:00.000Z', idempotency_key='synthetic-request-1')
    query = {k: record[k] for k in ('subject', 'scope', 'key')}
    query['as_of'] = '2026-10-09T00:00:00.000Z'
    plan = []
    def add(label, op, body, decision, status=200):
        plan.append(dict(label=label, operation=op, body=deepcopy(body), expected=decision, status=status))
    add('Clear your previous scenario', 'reset', {}, 'RETURN')
    if name == 'Temporal expiry':
        record['expires_at'] = '2026-06-01T00:00:00.000Z'
        add('Admit a time-bounded fact', 'admit', record, 'RETURN')
        add('One millisecond before expiry', 'query', dict(query, as_of='2026-05-31T23:59:59.999Z'), 'RETURN')
        add('Exactly at expiry', 'query', dict(query, as_of=record['expires_at']), 'HISTORICAL')
        add('Before effective time', 'query', dict(query, as_of='2025-12-31T23:59:59.999Z'), 'UNRESOLVED')
    elif name == 'Supersession':
        add('Admit original fact', 'admit', record, 'RETURN')
        add('Admit explicit correction', 'admit', dict(record, record_id='synthetic-record-2', value='synthetic-value-2', idempotency_key='synthetic-request-2', supersedes='synthetic-record-1', effective_at='2026-06-01T00:00:00.000Z'), 'RETURN')
        add('Current recall uses correction', 'query', query, 'RETURN')
        add('Inspect predecessor now', 'query', dict(query, record_id='synthetic-record-1'), 'SUPERSEDED')
        add('Recall before correction', 'query', dict(query, as_of='2026-05-01T00:00:00.000Z'), 'RETURN')
    elif name == 'Conflict / HOLD':
        add('Admit first value', 'admit', record, 'RETURN')
        add('Submit conflicting value', 'admit', dict(record, record_id='synthetic-record-2', value='synthetic-value-2', idempotency_key='synthetic-request-2'), 'HOLD')
        add('Recall refuses a silent winner', 'query', query, 'HOLD')
    elif name == 'Provenance':
        record.pop('provenance')
        add('Submit without a source', 'admit', record, 'HOLD')
        add('Recall held candidate', 'query', query, 'HOLD')
    elif name == 'Scope isolation':
        add('Admit in scope 1', 'admit', record, 'RETURN')
        add('Query declared scope 2', 'query', dict(query, scope='synthetic-scope-2'), 'UNRESOLVED')
        add('Query undeclared scope 3', 'query', dict(query, scope='synthetic-scope-3'), 'DENY', 403)
    else:
        add('Admit before reset', 'admit', record, 'RETURN')
        add('Recall before reset', 'query', query, 'RETURN')
        add('Reset your session', 'reset', {}, 'RETURN')
        add('Recall after reset', 'query', query, 'UNRESOLVED')
    return plan
