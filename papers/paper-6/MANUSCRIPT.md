# The Future of AI and Institutional Memory

## Model-Independent Scoped Memory

**Branden Laskowski**
*Cortex Agentics Global*
ADI Research Series — Paper 6
Unreleased preprint candidate · 15 November 2026

## Abstract

Organizations increasingly use AI systems to work with policies, decisions,
case files, and other digital records. Those records must remain traceable,
usable, and governed when the AI systems change.

This paper proposes **model-independent scoped memory**: an architectural
approach in which a deterministic system outside the AI model governs records.
It receives records, keeps their source and history, decides who may see them,
tracks corrections and retirement, and releases only the information needed for
a task. A model may read that released context and propose work, but it cannot
directly change the canonical record base.

We evaluate that proposition with first-party synthetic tests. The evidence
covers one governed record through update, revocation, retirement, and two
encrypted restarts; deterministic handling of 1,000,000 dated records; scope
tests involving 250 named clients, 1,200 synthetic institutional principals,
and 1,000 authenticated logical clients; named cross-machine and cross-model
handoffs; and retained adversarial results. The results support a narrow claim:
in the named protocols, canonical record authority remained outside model
inference while models and clients used released context. They do not establish
production readiness, security certification, universal model compatibility, or
independent replication. In a new follow-up, five authenticated clients each
released their expected record from the 1,000-client corpus. On those five
records, Qwen 3.5 35B passed five model-consumption tasks and Qwen 3 4B
returned five responses that failed the required answer schema.

We propose a prospective correction-through-handoff test that joins two
questions studied separately in the reported evidence. Can an authorized,
source-backed correction become the current record, and can a replacement model
recover that version and its decision history from an authorized working view?
The proposed test is described in Section 6 and remains unexecuted.

**Keywords:** institutional memory; digital records; artificial deterministic
intelligence; ADI; provenance; model independence; access scope; AI agents

## 1. Introduction

Every organization has a memory. It is found in records: policies, procedures,
decisions, evidence, correspondence, historical versions, and the reasons those
records changed. Those records need to stay understandable and trustworthy as
people, software, and now AI models change around them.

Most discussions of AI memory focus on whether a model can remember more than
will fit in one prompt. That is useful, but it is not the whole question. An
institution must also know:

- What is the current record?
- Where did it come from?
- What was replaced, and why?
- Who may see it?
- Can an AI system change it on its own?

Those questions are about authority, not just retrieval. A model can produce a
plausible answer that is stale, incomplete, unsupported, or outside the user’s
scope. If that answer becomes permanent merely because the model wrote it, the
organization has allowed a probabilistic process to rewrite its memory.

This paper studies a different arrangement. The AI model is a user of memory,
not its owner. It receives a limited working view of records it is allowed to
use. It may explain, summarize, compare, or propose a correction. A deterministic record system applies institutional policy to authenticated
sources and review decisions before a proposed change can enter the canonical
record.

We call this **model-independent scoped memory**. “Model-independent” means the
records and their authority do not belong to one model, one client, or one model
session. “Scoped” means that each user, worker, or system sees only the record
context that deterministic rules allow for the task.

The work is part of Artificial Deterministic Intelligence (ADI). ADI separates
probabilistic reasoning from deterministic authority. The model is allowed to
reason. The system outside it governs identity, record admission, source,
history, scope, correction, lifecycle, verification, and release.

The question of this paper is:

> How can organizations and institutions use deterministic systems outside AI
> models to continuously absorb, preserve, organize, contextualize, govern,
> protect, verify, update, and retrieve digital records as durable memory—while
> allowing changing AI systems to use the information without altering its
> source, scope, history, or authority?

## 2. Record Governance and the Model Boundary

### 2.1 A record is more than text

A reliable institutional record is not only its words. It also includes where
the record came from, who was allowed to submit it, what it replaced, what it
means now, who may access it, and the history needed to explain it later. In
this paper, that surrounding information is called **record governance**.

The model can be very good at working with the words. It is not, by itself, a
reliable authority for the surrounding facts. A model cannot establish that a
document was authentic merely because it can describe the document well. It
cannot decide that one version should replace another merely because the new
version sounds more convincing.

### 2.2 The proposed boundary

The proposal has two sides:

| The model may do | The record system decides |
| --- | --- |
| Read released context | Whether a record is admitted |
| Summarize or explain | Which source and version are current |
| Compare evidence | Who may retrieve a record |
| Draft a proposed correction | How corrections, history, and retirement are handled |
| Return work to a user or workflow | Whether a proposal becomes a durable record |

Records change when new evidence warrants an authorized correction. An
institution assigns authority to source owners and reviewers and documents
which evidence and approvals each kind of change requires.

### 2.3 What survives a model change

A minimal governed record contains a stable record ID, a version ID, the
source pointer and content digest, the preceding version, the effective date,
the applicable scope, and a lifecycle status. A decision receipt binds the
proposal and source references to the authenticated decision-maker or
service principal, the policy version, the disposition and reason, the
decision time, and the resulting version when a version is admitted. A release
receipt identifies the requesting principal, the applied policy, and the
versions included in the released working view. This is the proposed
contract for continuity. Individual studies exercise different parts of it.

An authorized records officer or designated source owner determines whether
the evidence substantiates a correction when institutional policy calls for
judgment. A policy can also recognize a preapproved source and apply fixed
criteria. If evidence conflicts and the policy cannot resolve the conflict,
the system holds the proposal for review and retains the existing version as
current. A model can surface the conflict. The institution supplies the
authority to resolve it.

### 2.4 Governing a proposed change

**G(p, A, P, H) → (d, r)** maps a proposal p, authenticated authority A,
the applicable policy P, and prior history H to a decision d and receipt r
for fixed inputs.

A decision can admit a new version, hold a proposal for review, preserve it as
context, quarantine it, or deny it. On admission, a superseded version remains
available to authorized historical queries for the period specified by
retention policy. The decision records what the institution recognizes as
authoritative at a given time. The retained source and decision history allow
that determination to be examined and corrected.

### 2.5 Relationship to records management and digital preservation

ISO 15489-1 describes records, metadata, policies, responsibilities, and
controls [6]. OAIS treats long-term preservation as keeping information
traceable and intelligible to its designated community as technology changes
[7]. PREMIS provides a preservation metadata model for objects, events, agents,
and rights [8]. W3C PROV provides a vocabulary for describing provenance [4].

Agent-memory research also gives models access to information beyond a single
prompt through mechanisms such as external memory and context management
[1–3]. This paper studies the interface between those approaches and
institutional records management. A changing AI system receives an authorized
working view tied to record versions, and proposals to change those records
pass through the institution's decision process. The reported studies test
specific aspects of that interface. Long-term format migration, successor
archive interoperability, and compliance with the cited standards remain
outside their scope.

## 3. What This Paper Tests

The paper tests a modest but important proposition:

> When a model, client, machine, or runtime is changed, the institution can keep
> its records, history, scope, and authority in a separate governed substrate.

The proposition would fail within a test if a client or model could change a
canonical record without authority, if a record lost its source or history, if
one scope received another scope’s record, or if the evidence trail broke.

The testing sequence follows the system outward:

1. Does one governed record keep its identity and history through change and
   restart?
2. Can the lifecycle rules handle large synthetic record sets?
3. Can many named clients retrieve only the records within their scope?
4. Can different named models and machines use the same released information
   without becoming the authority over it?
5. What happened when the system was deliberately pressured or attacked?

All reported evidence is first-party and synthetic unless noted otherwise. This
matters. Synthetic evidence can test the architecture without exposing private
records, but it is not the same as independent validation or production use.

## 4. Methods

### 4.1 Continuity and lifecycle (P6-C01, P6-C02)

One continuity test used a governed synthetic record, a private sentinel record,
two consumer identities, and two encrypted runtime restarts. It checked whether
the record’s identity, updates, history, source trail, revocation, and retirement
remained intact. It also tested two attempts by consumers to change the
canonical record.

A separate lifecycle test used 1,000,000 dated synthetic records spread across
three institutions and 300 departments. It checked whether the fixed lifecycle
rules made the expected decisions about active, historical, archived, retained,
and protected records.

### 4.2 Scope and retrieval pressure (P6-S01 to P6-S03, P6-A03)

Three studies tested access boundaries. The first used stages of 50, 100, 150,
200, and 250 named synthetic clients. The second represented 1,200 synthetic
read-only principals across 300 departments and three institutions. The third
used a live local HTTP/MCP service and 1,000 authenticated logical clients.

In the 1,000-client study, a privileged synthetic path seeded the test
records. Each authenticated logical client requested its expected record.
The measured workload was authenticated recall. Section 5 reports the
separately measured model-consumption results. The
study included one designated foreign-scope request, one invalid credential, and
one replay attempt.

### 4.3 Model and machine substitution (P6-M01 to P6-M04)

In the 7 November handoff, Qwen 3.5 35B on the Mac identified a synthetic
fact and its source. Cortex admitted the fact and applied a governed update
before exporting the encrypted store. The Dell imported that store, checked
current and historical state, then supplied the recalled record to
Gemma 3 12B. A later parity test gave
those named models the same hash-bound context made from two selected synthetic
record excerpts. The verifier compared the parsed answer fields, including
the product identity, update requirements, data-handling answers, and evidence
content hashes. It checked each response against the expected result and
checked that both trials used the same context and challenge hashes.

An earlier model-substitution study compared scoped 4B, 8B, and 35B models with
a broad-context 35B control over twelve matched synthetic tasks per arm. A
separate comparison study tested a narrow context-admission condition and
recorded important remaining differences rather than treating them as
equivalence.

### 4.4 Adversarial results (P6-A01, P6-A02)

The evidence record includes both an earlier adversarial failure and a later
passing rerun. The earlier 25-case run recorded 18 passes, one failure, six
inconclusive results, and one unauthorized effect. The later 25-case rerun
recorded 25 passes and zero unauthorized effects. Both outcomes remain in the
record. A later pass does not make an earlier failure disappear.

### 4.5 Follow-up inference (P6-M05, P6-M06)

On 15 November, the installed local models ran the fixed three-record
read-only fixture in Appendix D. The reference scorer evaluates the exact
response schema, open work, governing decision, failed approach, provenance
citations, and statement of action authority. The two scored responses used
different serving formats after the 4B raw requests aborted. The fixture
results are reported per configuration. Its content criteria are fixed keyword
checks, not a general semantic-comprehension measure; a response can contain a
required word while contradicting the intended meaning.

A second run selected five fixed positions across the original scale registry
(1, 250, 500, 750, and 1,000) before retrieving. An authenticated client at each
position recalled its own expected synthetic record and source through the
local service. Each of the two models then received the same record and
source for that position via native chat, with a fixed prompt, temperature
zero, and seed 7319. The scorer required exactly two JSON fields containing
the expected integer fact number and source citation. This was a five-record
paired sample. Calls were sequential.

## 5. Results

### 5.1 Continuity through change and restart (P6-C01)

The continuity test passed all 13 checks. One governed synthetic record kept its
identity through an update, two encrypted restarts, revocation of one client,
retirement, and preserved history. The system denied both attempts by consumers
to mutate the canonical record. It observed zero cross-scope records and
retained 80 audit events.

The proper interpretation is narrow: in this bounded sequence, the record’s
identity, history, source trail, revocation, and retirement remained outside the
control of the consumers. The test does not prove that every update path or
every deployment will behave the same way.

### 5.2 One million dated synthetic records (P6-C02)

The lifecycle study passed for 1,000,000 dated synthetic records across three
institutions and 300 departments. Each institutional partition reported zero
protected-record violations, zero within-retention historical deletions, zero
expected archive-transition failures, successful foreign-sentinel exclusion,
reconciled action counts, and a matching deterministic digest.

This is evidence that the tested local lifecycle policy handled the stated
synthetic corpus consistently. It is not evidence of real-world retention
compliance, continuous operation over years, or general hardware capacity.

### 5.3 Scope boundaries under pressure (P6-S01 to P6-S03, P6-A03)

The named-client pressure study passed. Across the five stages, it completed
7,500 expected retrievals. It ran 750 selected cross-scope probes and observed
zero leaks. Invalid credentials and replay attempts were denied at every stage,
and the 250-client restart recovery passed.

The human-principal study also passed. At its largest stage, 1,200 synthetic
read-only principals completed 6,000 searches across 300 departments and three
institutions. It observed zero foreign records, denied 1,200 attempted foreign
fetches, and passed 1,200-principal restart recovery.

The corrected 1,000-client local-service study passed 1,000 authenticated
logical-client recalls. The receipt reports 1,158.134 ms total wall time, p50
of 1,129.756 ms, p95 of 1,145.829 ms, and p99 of 1,146.946 ms. The audited runner measures the whole concurrent recall batch from dispatch
through completion, after seed admission. Its percentiles are elapsed
client-side times for individual authenticated requests, including response
parsing. The receipt does not bind that runner file to the execution.
Section 5.6 reports the separately measured inference follow-up.

An earlier attempt reached 999/1,000 admissions and recalls. It remains a
non-pass because one separately configured shared-scope client was mapped to the
wrong seat by the runner. The corrected repeat does not rewrite that history.

### 5.4 Cross-model use of released context (P6-M01 to P6-M04)

The Mac-to-Dell handoff passed. The Mac model passed four extraction checks,
the Dell importer passed 16 checks, and the Dell model passed five
consumption checks on the updated record. The import checks covered
governed identity, current state, prior history, provenance, and restart.

In the later parity test, the Mac ran Qwen 3.5 35B and the Dell ran Gemma 3 12B.
Both received the same hash-bound context from two selected excerpts and
produced the same normalized result. A separate Dell package checked
admission, recall, and post-restart recall for 98 records. The model challenge
used only the two selected excerpts. This shows
that, for this exact task, two named models could use the same released context
without being treated as the authority over the source records.

In the historical substitution study, acceptance required a complete, parseable
answer that met the frozen factual, citation, historical-record, scope, and
boundary checks. The scoped 8B and 35B arms accepted 12 of 12 matched tasks; the scoped 4B arm accepted 11 of 12;
the broad-context 35B control accepted 9 of 12. This is not a general ranking of
models. It is evidence that, in the named synthetic benchmark, selecting scope
before inference changed what the model received while retaining the governed
record-selection contract.

The separate context-admission comparison remains **partial**. Eight narrow
post-change trials met the stated condition, but material differences in
authorization, temporal handling, and context assembly remained. This result
must not be used to claim that two systems are equivalent.

### 5.5 Adversarial evidence (P6-A01, P6-A02)

The 11 September run recorded one unauthorized deletion effect involving a
disposable evidence fixture (A21). The 4 November run passed its 25-case
matrix with zero unauthorized effects. Its report records a denial for the
same A21 label and passing outcomes for the six previously inconclusive
case labels (A08, A11, A16, A22, A24, and A25). The September harness could
not observe those six boundaries. The case labels connect the reports.
The change in observability limits comparisons across the runs.

### 5.6 Model inference on the fixed fixture and authenticated recalls (P6-M05, P6-M06)

Qwen 3.5 35B passed all six criteria on the fixed fixture. Qwen 3 4B returned
a scoreable response via native chat after two raw requests aborted. It met
five of six criteria, with a failure on exact provenance citations.

In the live scoped follow-up, all five authenticated requests returned the
expected record and exact source. Both models generated responses on all five
records. Qwen 3.5 35B passed all five fact-and-citation tasks. Qwen 3 4B failed
the exact response-schema criterion on all five. Because the scorer gates
fact and citation checks on a valid schema, those failures do not identify a
specific factual or citation error. The sample measures this prompt and
configuration and is too small to rank the models generally.

## 6. Discussion and Proposed Correction-Through-Handoff Test

### 6.1 What the observed studies establish

The continuity study exercised governed state changes and restart. The
7 November handoff already showed that a replacement model on the Dell could
recover a fact after a governed update and encrypted transfer from the Mac.
The next question is whether the successor can explain why the updated
version governs when it faces a competing, unsupported proposal. The
prospective test adds that comparison, explicit citation and decision-history
checks, and revocation within the same sequence.

### 6.2 Hypothesis and fixture

For fixed institutional policy and a named pair of models, an authorized,
source-backed correction should survive model replacement with the same
record ID, current version, source lineage, and access rules. The replacement
model should be able to reconstruct the correction from its released view.

Use a synthetic policy record whose first version sets a routine review
interval of 30 days. A dated, authenticated amendment changes it to 45 days.
The fixture also specifies an unsupported competing proposal of 60 days.
Freeze the initial record, amendment, expected version chain, policy version,
reviewer authority, query time, and exact expected citations before execution.
Set the query time after the amendment takes effect. Give the authorized
successor access to the current version and the history needed to explain
the correction. Grant a second client the same read scope initially so the
test can measure access before and after revocation.

### 6.3 Procedure and comparison

1. Start the originating model in a fresh session with the initial policy and
   amendment. Collect its source-backed proposal and an unsupported competing
   proposal through the same proposal interface. Score the originating
   model's proposal quality separately. If either planned proposal is missing
   or malformed, retain that result. A frozen substitute proposal may be used
   in a separately labeled governance control.
2. Have an authenticated records officer review both proposals against the
   same versioned policy. Record both dispositions. The expected state is
   version 2 at 45 days, with version 1 at 30 days retained as history and
   the 60-day proposal absent from current authority. Verify that the second
   client can read the corrected record before revoking its grant.
3. End the originating model session. Read from the same governed state with
   a different pinned model in a clean session with no inherited transcript.
   Ask what policy applies as of the fixed query time, what it replaced,
   which source authorized the change, and why the competing proposal did
   not govern. Retry the record request with the revoked client. Measure
   revocation against new releases.
4. Compare the replacement model with a fresh session of the original model
   using the same committed state, authorized query, and released context.
   Add an unapproved-amendment control in which version 1 must remain
   current. Treat any restart or machine migration as a separately reported
   extension. Register the model revisions, fixture variants, run order,
   repetition count, and scoring rules before execution.

### 6.4 Outcomes and evidence

| Outcome | Passing condition |
| --- | --- |
| Governed state | Stable record ID, exact current version and source, intact historical version, receipt for each disposition, and no canonical transition from the unsupported proposal. |
| Authorized release | The approved reader receives the expected versions, decision evidence, and exact citations under the current policy. A new request from the revoked client releases no protected record. |
| Model interpretation | The successor identifies 45 days as current and 30 days as prior, gives the correct effective date, cites the expected sources, and identifies the 60-day proposal as non-authoritative. |

Record proposal and response hashes, model and runtime identities, exposed
settings, policy and fixture hashes, release and decision receipts, and
criterion-level scores. A wrong model answer fails the interpretation
criterion. A wrong record, broken lineage, unauthorized transition, or
release to the revoked client fails the relevant governing criterion even if
the model answer is correct. Report infrastructure interruptions and any
diagnostic reruns under their own run identifiers. The proposed experiment
has no results in this draft.

## 7. Limitations

1. All evidence is first-party and synthetic; independent replication has not
   yet been completed.
2. The studies are bounded local protocols, not a production customer
   deployment, wide-area availability test, or regulatory-compliance audit.
3. The 1,000-client result measures authenticated retrieval capacity for its
   local workload. Model-consumption results have their own sample sizes.
4. The negative probes are selected tests, not exhaustive penetration testing.
5. Cross-model results concern named models, fixtures, and released contexts.
   They do not establish universal provider compatibility.
6. The Dell 98-record admission/recall/restart package was not a 98-record
   model-consumption test; models consumed two selected excerpts in the parity
   task.
7. The earlier adversarial failure materially limits blanket safety or security
   claims even though a later rerun passed.
8. Historical benchmark figures are historical local baselines, not current
   production-performance claims.
9. Non-public implementation details and raw receipts limit full independent
   reconstruction, although the public materials can support black-box testing.
10. The mixed-model correction-through-handoff experiment in Section 6 is
    proposed. Long-term preservation across format and archive migrations
    also remains to be evaluated.

## 8. Evidence Integrity and Reproducibility

The companion evidence package provides a public reconciliation ledger, a
machine-readable catalog, and SHA-256 checksums. The catalog records what each
study tested, the result, its source pointer or receipt hash, and what the study
does not establish. It preserves non-passes, mixed outcomes, partial results,
and infrastructure failures. A checksum identifies artifact bytes. For an
execution claim, the receipt should also bind the executed runner revision,
runtime or image digest, fixture, and result in the same run. Appendix B
records the missing execution binding for the 1,000-client receipt.

An independent evaluator should report the exact source revision, environment,
model and runtime identity, exposed inference settings, fixture version,
criterion-level results, and hashes of sanitized receipts or outputs. Missing or
unavailable fields must remain visible. An external run would add evidence; the
existence of a public protocol is not itself independent replication.

## 9. Conclusion

The future of AI and institutional memory should not depend on a single model
remembering correctly. Institutions need a digital record layer that can stay in
order as models, clients, and AI workforces change. Model-independent scoped
memory is a proposal for that layer: records remain governed by deterministic
rules outside the model, while AI systems receive only the context they are
allowed to use.

The reported evidence supports this proposition under named first-party
synthetic conditions from record continuity through lifecycle scale, scope
pressure, model handoff, and adversarial testing. It does not prove universal
security or production readiness. It does establish a concrete research program:
test whether a replacement model can use and explain a governed correction
while the authoritative version, lineage, and access rules remain with the
institution.

## Declarations

### Data and code availability

The companion package in the Paper Six working directory includes the
manuscript, evidence summaries, reconciliation ledger, machine-readable
catalog, synthetic fixtures, and checksums. The
[versioned evidence-review baseline](https://github.com/brandenlaskowski7-bot/cortex-adi-research/tree/92600425278f6f1b21e1c68fba5e7fe818517c97/papers/paper-6)
identifies the starting revision for this working draft. Consult the matching
checksum manifest in the revised review package for the current files. The
package excludes private source code, credentials, personal and customer
records, raw private receipts, and non-public deployment details.

### Ethics and privacy

The reported studies used synthetic records and did not involve human subjects,
medical records, customer records, or intentionally collected personal data.

### Competing interests

The author is affiliated with Cortex Agentics Global, developer of the evaluated
Cortex Continuum substrate, and may have a commercial interest in the work.

### Funding

No external funding source is asserted for this preprint candidate.

## References

1. Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., &
   Bernstein, M. S. (2023). *Generative Agents: Interactive Simulacra of Human
   Behavior*. UIST. https://arxiv.org/abs/2304.03442
2. Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., &
   Gonzalez, J. E. (2023). *MemGPT: Towards LLMs as Operating Systems*.
   https://arxiv.org/abs/2310.08560
3. Sumers, T. R., Yao, S., Narasimhan, K., & Griffiths, T. L. (2023).
   *Cognitive Architectures for Language Agents*.
   https://arxiv.org/abs/2309.02427
4. Groth, P., & Moreau, L. (Eds.). (2013). *PROV-Overview: An Overview of the
   PROV Family of Documents*. W3C Working Group Note.
   https://www.w3.org/TR/prov-overview/
5. Laskowski, B. (2026). *Artificial Deterministic Intelligence:
   Probabilistic Reasoning, Deterministic Authority*. ADI Research Series.
   https://doi.org/10.5281/zenodo.23265200
6. International Organization for Standardization. (2016). *Information and
   documentation — Records management — Part 1: Concepts and principles*.
   [ISO 15489-1:2016](https://www.iso.org/standard/62542.html).
7. Consultative Committee for Space Data Systems. (2024). *Reference Model
   for an Open Archival Information System (OAIS)*.
   [CCSDS 650.0-M-3](https://ccsds.org/Pubs/650x0m3.pdf).
8. PREMIS Editorial Committee. (2015). *PREMIS Data Dictionary for
   Preservation Metadata*, version 3.0.
   [Library of Congress](https://www.loc.gov/standards/premis/v3/index.html).

## Appendix A. Evidence Map

| ID | Study | Result | What it supports |
| --- | --- | --- | --- |
| P6-C01 | 13-check invariant sequence | Pass | One bounded record lifecycle across two encrypted restarts and two denied consumer mutations. |
| P6-C02 | Million-record temporal pressure | Pass | Deterministic classification of 1,000,000 dated synthetic records across three institutions and 300 departments. |
| P6-S01 | Named-client pressure | Pass | 7,500 expected retrievals through 250 named clients; 750 selected foreign-scope probes observed zero leaks. |
| P6-S02 | Human-principal pressure | Pass | 1,200 synthetic principals, zero observed foreign records, 1,200 denied foreign fetches. |
| P6-S03 | Live local 1,000-client protocol | Pass after retained non-pass | 1,000 authenticated logical-client expected recalls. |
| P6-M01 | Mac-to-Dell handoff | Pass | One controlled synthetic handoff between named environments. |
| P6-M02 | Qwen 35B / Gemma 12B parity | Verified | Same hash-bound two-record context and same normalized result. |
| P6-M03 | Historical-memory model study | Mixed retained | Scoped 8B/35B: 12/12; scoped 4B: 11/12; broad-context 35B: 9/12. |
| P6-M04 | Context-admission differential | Partial | Eight narrow trials with material differences retained. |
| P6-M05 | Fixed read-only fixture | Mixed | 35B met 6/6 criteria. The 4B native-chat result met 5/6 after two raw requests aborted. |
| P6-M06 | Inference on authenticated recalls | Mixed | Five matching recalls. 35B passed 5/5 tasks. 4B ran all five and passed 0/5 under the exact-schema rule. |
| P6-A01 | 11 Sep suite | Fail retained | 18/25 pass, one failure, six inconclusive, one unauthorized effect. |
| P6-A02 | 4 Nov rerun | Pass | 25/25 named cases with zero unauthorized effects. |
| P6-A03 | First 1,000-client execution | Retained non-pass | 999/1,000 admissions and recalls before the runner's scope-seat mapping was corrected. |
| P6-H01 | Kernel pressure baseline | Pass | Historical local in-memory 100/1,000/10,000-record baseline. |
| P6-H02 | Governed queue baseline | Pass | Historical deterministic queue/control benchmark; excludes model/tool/connector/external effects. |

See `EVIDENCE_CATALOG_20261115.md` and `evidence/CATALOG.json` for source
pointers and integrity identifiers.
