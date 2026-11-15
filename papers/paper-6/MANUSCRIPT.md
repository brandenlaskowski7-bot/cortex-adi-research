# The Future of AI and Institutional Memory

## Model-Independent Scoped Memory

**Branden Laskowski**
*Cortex Agentics Global*
ADI Research Series — Paper 6
Unreleased preprint candidate · 15 November 2026

## Abstract

Organizations are beginning to place AI systems beside their most important
digital records: policies, decisions, case files, procedures, correspondence,
and source material. That creates a basic problem. AI models can reason over
information, but they can also be wrong, replaced, unavailable, or persuaded by
bad instructions. A model should not become the authority that silently changes
the institution's record of what is true.

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
independent replication.

The central contribution is a way to think about AI and institutional memory:
the model may change, but the organization’s governed digital record should not
become owned by the model.

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
use. It may explain, summarize, compare, or propose a correction. A separate,
deterministic record system decides whether any proposed change has adequate
evidence and authority to become part of the institutional record.

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

## 2. The Idea in Plain Terms

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

This is not an argument for preventing records from changing. Records must
change when new evidence arrives. The distinction is between a properly
supported, authorized correction and a model output that has not earned the
right to alter institutional history.

### 2.3 A simple formal statement

Let a model produce a proposed change, \(p\). The model does not directly make
that change canonical. A deterministic governing process considers the proposal
along with authenticated authority, policy, and existing history:

\[
G(p, \text{authority}, \text{policy}, \text{history})
\rightarrow (\text{decision}, \text{receipt}).
\]

The decision may admit the change, hold it for review, preserve it as context,
quarantine it, mark an earlier record as historical, or deny it. The important
point is that this decision is outside the model.

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

### 4.1 Continuity and lifecycle

One continuity test used a governed synthetic record, a private sentinel record,
two consumer identities, and two encrypted runtime restarts. It checked whether
the record’s identity, updates, history, source trail, revocation, and retirement
remained intact. It also tested two attempts by consumers to change the
canonical record.

A separate lifecycle test used 1,000,000 dated synthetic records spread across
three institutions and 300 departments. It checked whether the fixed lifecycle
rules made the expected decisions about active, historical, archived, retained,
and protected records.

### 4.2 Scope and retrieval pressure

Three studies tested access boundaries. The first used stages of 50, 100, 150,
200, and 250 named synthetic clients. The second represented 1,200 synthetic
read-only principals across 300 departments and three institutions. The third
used a live local HTTP/MCP service and 1,000 authenticated logical clients.

These are retrieval studies. They do not represent 1,000 live workers or 1,000
model inferences. In the 1,000-client study, a privileged synthetic path first
seeded the test records; clients then made expected-only recall requests. The
study included one designated foreign-scope request, one invalid credential, and
one replay attempt.

### 4.3 Model and machine substitution

A controlled handoff moved a synthetic record package from a Mac environment
using Qwen 35B to a Dell environment using Gemma 12B. A later parity test gave
those named models the same hash-bound context made from two selected synthetic
record excerpts and compared their normalized results.

An earlier model-substitution study compared scoped 4B, 8B, and 35B models with
a broad-context 35B control over twelve matched synthetic tasks per arm. A
separate comparison study tested a narrow context-admission condition and
recorded important remaining differences rather than treating them as
equivalence.

### 4.4 Adversarial results

The evidence record includes both an earlier adversarial failure and a later
passing rerun. The earlier 25-case run recorded 18 passes, one failure, six
inconclusive results, and one unauthorized effect. The later 25-case rerun
recorded 25 passes and zero unauthorized effects. Both outcomes remain in the
record. A later pass does not make an earlier failure disappear.

## 5. Results

### 5.1 Continuity through change and restart

The continuity test passed all 13 checks. One governed synthetic record kept its
identity through an update, two encrypted restarts, revocation of one client,
retirement, and preserved history. The system denied both attempts by consumers
to mutate the canonical record. It observed zero cross-scope records and
retained 80 audit events.

The proper interpretation is narrow: in this bounded sequence, the record’s
identity, history, source trail, revocation, and retirement remained outside the
control of the consumers. The test does not prove that every update path or
every deployment will behave the same way.

### 5.2 One million dated synthetic records

The lifecycle study passed for 1,000,000 dated synthetic records across three
institutions and 300 departments. Each institutional partition reported zero
protected-record violations, zero within-retention historical deletions, zero
expected archive-transition failures, successful foreign-sentinel exclusion,
reconciled action counts, and a matching deterministic digest.

This is evidence that the tested local lifecycle policy handled the stated
synthetic corpus consistently. It is not evidence of real-world retention
compliance, continuous operation over years, or general hardware capacity.

### 5.3 Scope boundaries under pressure

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
of 1,129.756 ms, p95 of 1,145.829 ms, and p99 of 1,146.946 ms. These numbers
describe that local expected-only retrieval protocol; they are not model
throughput, a public service-level objective, or a production capacity claim.

An earlier attempt reached 999/1,000 admissions and recalls. It remains a
non-pass because one separately configured shared-scope client was mapped to the
wrong seat by the runner. The corrected repeat does not rewrite that history.

### 5.4 Cross-model use of released context

The named Mac-to-Dell handoff passed its controlled synthetic protocol. In the
later parity test, Qwen 35B and Gemma 12B received the same hash-bound context
from two selected excerpts and produced the same normalized result. This shows
that, for this exact task, two named models could use the same released context
without being treated as the authority over the source records.

The earlier model-substitution study was deliberately mixed. The scoped 8B and
35B arms accepted 12 of 12 matched tasks; the scoped 4B arm accepted 11 of 12;
the broad-context 35B control accepted 9 of 12. This is not a general ranking of
models. It is evidence that, in the named synthetic benchmark, selecting scope
before inference changed what the model received while retaining the governed
record-selection contract.

The separate context-admission comparison remains **partial**. Eight narrow
post-change trials met the stated condition, but material differences in
authorization, temporal handling, and context assembly remained. This result
must not be used to claim that two systems are equivalent.

### 5.5 Adversarial evidence

The adversarial record is intentionally not reduced to a slogan. The earlier run
failed and contained an unauthorized effect. The later rerun passed its stated
25-case matrix with zero unauthorized effects. The correct conclusion is that a
later first-party synthetic rerun passed its named cases while an earlier run
failed and remains available for review. Neither result is a security
certification.

## 6. Discussion

### 6.1 The key result is the separation of roles

The evidence supports an architectural claim: a model can use governed
institutional memory without owning it. That is different from saying a model
has perfect memory or that all models will answer equally well. Models varied in
the substitution studies. The record substrate, in the named continuity and
scope tests, remained governed outside of them.

This separation matters for AI workforces. Different workers may use different
models. A strong model might draft a complex analysis; a smaller model might
answer a narrow operational question. If each worker's model session is the
memory authority, the organization risks fragmentation and silent mutation. If
the digital record layer remains separate, changing workers does not require
changing who owns institutional truth.

### 6.2 Correct change versus unsupported change

No useful memory system can refuse all change. A policy is updated; a case is
corrected; a record becomes historical. The issue is whether a model's text is
enough to make that happen. In the proposed architecture, a change must travel
through a deterministic decision path with evidence, authority, history, and a
recorded outcome. A model may suggest a change, but an unsupported or
out-of-scope suggestion does not become canonical simply because it sounds
reasonable.

### 6.3 Scope is part of memory integrity

Memory is not intact if the wrong person or agent receives it. The scope studies
do not prove exhaustive isolation, but they make the boundary testable. Expected
retrievals, foreign-scope probes, credential failures, replay attempts, restarts,
and receipts can all be reported separately. This is a better basis for a
commercial or scientific discussion than a general assertion that an AI system
is “secure.”

### 6.4 What this does and does not propose

This paper does not claim that this architecture is the only valid way to build
AI memory, nor that all competing systems give models record authority. It does
not make a universal novelty claim. It proposes a testable institutional-memory
model: keep records and their governance external to models, expose only
authorized working context, and retain the evidence required to explain changes.

## 7. Limitations

1. All evidence is first-party and synthetic; independent replication has not
   yet been completed.
2. The studies are bounded local protocols, not a production customer
   deployment, wide-area availability test, or regulatory-compliance audit.
3. The 1,000-client result is a logical-client retrieval study with no model
   inference. It is not a 1,000-agent inference test.
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

## 8. Evidence Integrity and Reproducibility

The companion evidence package provides a public reconciliation ledger, a
machine-readable catalog, and SHA-256 checksums. The catalog records what each
study tested, the result, its source pointer or receipt hash, and what the study
does not establish. It preserves non-passes, mixed outcomes, partial results,
and infrastructure failures.

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
test whether records remain protected, traceable, current, and properly scoped
while changing AI systems work on top of them.

## Declarations

### Data and code availability

The public Paper 6 package includes the manuscript, evidence summaries,
reconciliation ledger, machine-readable evidence catalog, public fixtures, and
checksums. It excludes private implementation source, credentials, personal or
customer records, raw receipts, and non-public topology.

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

## Appendix: Evidence map

| Layer | Study | Result | What it supports |
| --- | --- | --- | --- |
| Continuity | 13-check invariant sequence | Pass | One bounded record lifecycle across two encrypted restarts and two denied consumer mutations. |
| Lifecycle | Million-record temporal pressure | Pass | Deterministic classification of 1,000,000 dated synthetic records across three institutions and 300 departments. |
| Scope | Named-client pressure | Pass | 7,500 expected retrievals through 250 named clients; 750 selected foreign-scope probes observed zero leaks. |
| Scope | Human-principal pressure | Pass | 1,200 synthetic principals, zero observed foreign records, 1,200 denied foreign fetches. |
| Scope | Live local 1,000-client protocol | Pass after retained non-pass | 1,000 authenticated logical-client expected recalls; no model inference. |
| Substitution | Mac-to-Dell handoff | Pass | One controlled synthetic handoff between named environments. |
| Substitution | Qwen 35B / Gemma 12B parity | Verified | Same hash-bound two-record context and same normalized result. |
| Substitution | Historical-memory model study | Mixed retained | Scoped 8B/35B: 12/12; scoped 4B: 11/12; broad-context 35B: 9/12. |
| Comparison | Context-admission differential | Partial | Eight narrow trials; material differences retained. |
| Adversarial | 11 Sep suite | Fail retained | 18/25 pass, one failure, six inconclusive, one unauthorized effect. |
| Adversarial | 4 Nov rerun | Pass | 25/25 named cases; zero unauthorized effects; not certification. |
| Historical | Kernel pressure baseline | Pass | Historical local in-memory 100/1,000/10,000-record baseline; no model/provider calls. |
| Historical | Governed queue baseline | Pass | Historical deterministic queue/control benchmark; excludes model/tool/connector/external effects. |

See `EVIDENCE_CATALOG_20261115.md` and `evidence/CATALOG.json` for source
pointers and integrity identifiers.
