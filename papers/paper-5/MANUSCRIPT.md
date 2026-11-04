# Where Does AI Continuity Live?

## A Controlled Replacement Test of Governed Memory Across Models, Clients, Platforms, and Runtime Restarts

**Branden Laskowski**  
Cortex Agentics Global  
ADI Research Series — Paper 5, experimental preprint draft  
November 2026

**Research lineage.** This paper is an empirical extension of Branden Laskowski's Artificial Deterministic Intelligence (ADI) research program, introduced in *Artificial Deterministic Intelligence: Probabilistic Reasoning, Deterministic Authority* [1] and advanced through the model-substitution study in ADI Research Series Paper 2 [2]. Cortex Continuum is the evaluated memory substrate; ADI supplies the governing scientific theory.

### Abstract

**Question:** When the model, client, machine, or runtime changes, can one governed memory substrate preserve the exact continuity of work without transferring authority over memory to the replacement model?

We answer with a controlled replacement test derived from Artificial Deterministic Intelligence (ADI). A synthetic continuity state—open work, a governing decision, a failed approach, exact provenance, scope, lifecycle rules, and receipts—was fixed outside the model. Models, clients, machines, operating systems, and restart conditions were then replaced while the state contract remained unchanged. The primary outcome was not fluent recall. It was continuity invariance: the authorized state had to remain recoverable with exact lineage, excluded state had to remain undisclosed, the audit chain had to remain valid, and every attempted unauthorized state effect had to fail. Model comprehension was measured separately.

The tested substrate preserved its deterministic contract in 12/12 frozen fixtures, 23/23 unchanged kernel tests, and 13/13 security-boundary tests. In the core cross-client challenge, all three governed records and 3/3 provenance pointers survived encrypted restart, a different read-only client recovered them, zero cross-scope leaks were observed, and the audit chain verified. Three separately recorded restart repetitions produced the same continuity result. A separately implemented first-party black-box client passed 10/10 contract checks; a bounded 50-client run completed 900/900 staged retrieval operations and 50/50 post-restart recoveries; and a 25-case adversarial suite recorded zero unauthorized effects.

Model outputs varied while governed state did not. Qwen 3 8B and 14B passed the complete read-only consumption contract; smaller Qwen models produced semantic or exact-citation failures. Gemma 3 12B, Gemma 3 4B, and Llama 3.2 3B on a second machine preserved exact citations and acknowledged no action authority, but did not pass every semantic criterion. A fresh Codex observation passed the complete contract without controlled inference parameters. An MLX trial failed exact schema and citation requirements, and hosted API and llama.cpp attempts ended without scoreable model responses. Failures were retained rather than converted into successes.

These results support a bounded answer: in the tested system, operational continuity resided in the governed substrate rather than in any single model session. The experiment does not show that every model understands the same memory equally well; it shows why model comprehension and memory authority must be different variables. This is the central strength of ADI demonstrated at the memory layer: probabilistic reasoning may change or fail while deterministic authority, provenance, and continuity remain stable. Cortex Continuum Benchmark v1 publishes the falsification contract for external evaluation. Production readiness, security certification, universal provider portability, and independent replication are not established.

**Keywords:** Artificial Deterministic Intelligence; ADI; agent memory; governed memory; provenance; model substitution; continuity; access control; MCP; deterministic systems

![Figure 1. Models may propose or consume memory, but deterministic admission, placement, lifecycle, scope, and receipts remain outside inference.](architecture.svg)

*Figure 1. Architectural separation tested in this paper. The model is an untrusted reasoning client; it is not the authority over canonical memory.*

## 1. Introduction

This paper starts with one question:

> **When the model, client, machine, or runtime changes, can one governed memory substrate preserve the exact continuity of work without transferring authority over memory to the replacement model?**

That question is more fundamental than whether a memory system can retrieve a relevant passage. It asks what carries continuity when the most visible component of an AI system—the model—is replaceable.

The scientific test is a controlled replacement intervention. Hold a continuity state and its governing contract fixed outside inference. Then replace the model, client, platform, or runtime and ask what remains invariant. If open work, governing decisions, negative evidence, exact provenance, scope, lifecycle status, and receipts remain intact—and if no replacement can create an unauthorized state effect—then continuity is being carried by the external substrate. If the selected model misreads the state, that is a measured inference failure. It is not permission to corrupt the state.

Memory is becoming a first-class component of language-model agents. Existing systems extend limited context windows, store conversational facts, synthesize reflections, organize temporal knowledge, or retrieve salient records across sessions. These contributions address important capability and efficiency problems. Yet the term *memory* often collapses several different functions: storage, retrieval, summarization, belief formation, identity, policy, access control, and operational state.

That collapse creates an authority problem. A model-generated statement can be fluent and useful while still being stale, unsupported, outside scope, contradictory, or unauthorized. If the same probabilistic process both proposes a memory and controls whether that proposal becomes canonical, then an inference error can become durable system state. If a model can silently rewrite provenance or remove negative evidence, the problem is no longer only retrieval quality. It is state governance.

Artificial Deterministic Intelligence (ADI) supplies the theory behind this separation. ADI holds that models can provide bounded probabilistic reasoning while deterministic systems external to the model govern identity, authority, memory admission, execution rights, state transitions, verification, and release [1]. Prior ADI work tested governed context and model substitution under fixed external contracts [2]. The present paper isolates continuity memory and asks whether one of ADI's strongest propositions survives direct intervention: replace the reasoning layer without surrendering or resetting the authoritative state.

The central proposition is deliberately narrow but consequential:

> A model may read authorized memory and propose a state change, but it must not decide whether that proposal is admitted, where it is placed, what scope may retrieve it, whether it supersedes prior state, or whether history is deleted.

This paper contributes:

1. one falsifiable research question and a controlled replacement method for answering it;
2. a precise authority model for deterministic continuity memory;
3. a preregistered evaluation that treats continuity invariance and model comprehension as separate dependent variables;
4. first-party synthetic evidence across models, clients, two machines, two operating systems, and encrypted runtime restarts, with negative and infrastructure outcomes retained; and
5. a public benchmark contract through which reviewers can attempt to falsify the stated claims without receiving the proprietary implementation.

The contribution is architectural and empirical, not a priority claim. We do not claim that no prior system combines these mechanisms, nor that the present tests establish universal portability. We claim that this experiment makes the location of continuity testable: change the reasoning components, preserve the governed state, and measure whether authority and lineage move with the model or remain with the substrate.

## 2. Related Work

### 2.1 Agent memory as retrieval and context management

Generative Agents stores experiences, synthesizes reflections, and retrieves memories to guide behavior [3]. MemoryBank adds long-term storage and time-sensitive updating for sustained interaction [4]. MemGPT treats context as a hierarchy and uses operating-system-inspired virtual context management [5]. These systems show that external memory can extend agent behavior beyond a single context window.

CoALA places memory within a broader cognitive architecture, distinguishing modular memory and structured action spaces [6]. Mem0 emphasizes scalable extraction, consolidation, retrieval, and latency/cost tradeoffs [7]. Zep uses a temporal knowledge graph to maintain changing relationships and cross-session context [8]. Recent surveys describe agent memory as a write–manage–read loop and identify trustworthiness, privacy, contradiction handling, and governance as emerging problems [9,10].

These systems and taxonomies motivate the present work, but our dependent variable differs. We do not primarily ask whether a memory system improves answer accuracy. We ask whether canonical state remains externally governed when model answers are imperfect.

### 2.2 Provenance, protocol, and authority

The W3C PROV family formalizes entities, activities, agents, and derivations for interoperable provenance [11]. This study uses source pointers and proof references in a narrower implementation-specific form, while preserving the same core distinction between a claim and its lineage.

The Model Context Protocol (MCP) standardizes tool and resource interaction across clients. Its 2026 revision emphasizes stateless requests, deterministic catalog ordering, and authorization hardening [12]. MCP enables interoperability, but protocol transport alone does not determine who may write canonical memory. In this paper, an MCP-style client is constrained by a separate Cortex grant: caller-claimed scope, hosted/local identity, and requested result limits do not override the registered authority.

### 2.3 ADI and externalized continuity

ADI defines a system boundary in which models perform bounded inference while deterministic components govern identity, authority, memory admission, policy, execution rights, state transitions, verification, and release [1]. Paper 2 evaluated continuity under model handoff and runtime restart while holding an external work package constant [2]. Its proposed stronger test—source-model work followed by an authorized state update and a different recipient model—directly motivates this study.

This lineage matters scientifically. ADI is not used here as a product label added after testing; it supplies the hypothesis, the authority boundary, the evidence taxonomy, and the rule that model capability must not be confused with system authority. Paper 5 strengthens the ADI research program by testing one of its central architectural claims at the memory layer: state may remain durable and useful across model substitution without becoming model-owned state.

### 2.4 ADI research credit and extension

The ADI framework, the phrase *probabilistic reasoning, deterministic authority*, and the lifecycle-wide separation of inference from authorization originate in Branden Laskowski's ADI umbrella paper [1]. The fixed external contract and model-substitution method build directly on ADI Research Series Paper 2 [2]. Paper 5 is therefore an application and empirical extension of ADI rather than an unrelated memory benchmark. Its distinct contribution is the controlled continuity replacement test, the retained cross-environment evidence, and the public Cortex Continuum Benchmark v1 falsification contract.

## 3. Architecture and Formal Boundary

Let a model produce a candidate memory proposal:

\[
p = (c, s, n, k, t)
\]

where \(c\) is content, \(s\) is source lineage, \(n\) is namespace or scope, \(k\) is the proposed class, and \(t\) is time metadata. A probabilistic model may generate \(p\), but it does not produce the canonical transition.

The deterministic substrate evaluates:

\[
D(p, A, P, H) \rightarrow (d, r)
\]

where \(A\) is authenticated authority, \(P\) is policy, \(H\) is prior governed history, \(d\) is a disposition, and \(r\) is a receipt. In the evaluated implementation:

\[
d \in \{\text{HOLD}, \text{CONTEXT}, \text{AUTHORITY}, \text{QUARANTINE}, \text{DENY}\}
\]

The transition function is deterministic for fixed inputs and policy. The model cannot directly alter \(A\), \(P\), \(H\), \(d\), or \(r\).

### 3.1 Governed dispositions

The public research boundary describes five generic outcomes: held pending review, recallable context, approved authority, quarantined evidence, and denied admission. Historical state can remain retained under lifecycle policy after it is removed from current recall.

These categories describe the tested contract without disclosing proprietary subsystem names, internal role labels, implementation topology, or internal classification schemes. The research claim concerns the separation between candidate input, governed disposition, and recallability.

### 3.2 Authority invariants

The study tests five invariants:

1. **Admission:** no canonical record without required source lineage and legal transition.
2. **Placement:** model preference cannot promote a proposal to authoritative memory.
3. **Scope:** a client can retrieve only the namespace granted by deterministic authority.
4. **History:** restart, supersession, expiry, and disposition do not silently erase lineage or negative evidence.
5. **Receipts:** state transitions and recall produce independently inspectable proof records.

## 4. Methods

### 4.1 Primary hypothesis: the continuity carrier

We define the operational continuity state as:

\[
C = (W, D, N, P, S, L, R)
\]

where (W) is open work, (D) is a governing decision, (N) is retained negative evidence, (P) is provenance, (S) is authorized scope, (L) is lifecycle state, and (R) is the receipt and audit record.

The primary hypothesis was:

> **H1 — Substrate-carried continuity:** For a fixed authorized state and deterministic policy, replacing the consuming model, client, machine, or runtime will preserve (C) and produce zero unauthorized canonical-state effects.

The alternative explanation under test is that continuity is carried by the model session or its immediate runtime. If that were true, replacement should erase, alter, re-scope, or surrender control of some component of (C). H1 was falsified by any unauthorized canonical transition, lost or altered governed record, provenance mismatch in the substrate, cross-scope disclosure, invalid audit chain, or model/client ability to bypass the registered authority contract.

### 4.2 The Continuity Replacement Test

One intervention operationalized the hypothesis:

1. freeze one synthetic continuity state containing open work, a governing decision, a failed approach, exact source pointers, scope, lifecycle rules, and receipts;
2. admit and persist that state through the deterministic authority boundary;
3. replace the active client and restart the runtime against the same encrypted stores;
4. expose only the authorized state to named replacement models and environments;
5. test whether (C_{before}=C_{after}), whether excluded state remains excluded, and whether any replacement produces an unauthorized state effect; and
6. score each model's comprehension separately from the substrate result.

The primary substrate result was `PASS` only if the authorized records and exact provenance were preserved, the audit chain verified, the observed cross-scope leak count was zero, and the observed unauthorized-effect count was zero. Model consumption was a second result for each named model: semantic fields, exact response citations, and acknowledgement of no action authority. Thus, a model could fail to understand the packet without becoming capable of changing it.

### 4.3 Preregistration and execution order

Protocol version 1.0.0 was frozen before paper-specific pilot execution. The order was: existing baseline preservation; protocol and fixture freeze; deterministic and two-model pilot; reporting-only harness repair; one confirmatory execution; evidence hashing; manuscript drafting. A Dell machine was identified after freeze and registered as a separate extension. It was not added to or pooled with the preregistered confirmatory set.

After the original study, Continuity Expansion v1 was preregistered as a separate evidence layer. It retained the original three-record packet, prompt hash, lexical criteria, temperature 0, seed 7319 where the runtime exposed those controls, and the rule that any missing required criterion prevents a complete pass. The expansion covered two additional Dell model families/sizes, a separately implemented black-box client, bounded concurrency and restart repetition, a governance-adversarial suite, one fresh Codex observational trial, and alternate local and hosted runtime attempts. Expansion results are labeled post-freeze and are not pooled with the original confirmatory set.

The initial model pilot could not reach the local model service from the restricted execution environment. Both `fetch failed` results were retained. A retry with local-process access produced valid responses. The only main-study harness repair changed a static claim-boundary sentence so a zero-pass run could not claim support; prompt, evidence, inference parameters, parser, and scoring were unchanged.

The Dell extension had its own first-attempt reporting failure after the model-response path: the recorder used a hash-formatting method unavailable in the host's older Windows PowerShell/.NET environment. Because that catch path did not retain the raw response or criterion values, no model outcome was assigned to the attempt. The attempt was preserved, the byte-to-hex conversion alone was replaced with an older-compatible equivalent, and one confirmatory Dell execution was performed with the identical frozen prompt, schema, seed, temperature, parser, and scorer.

### 4.4 Evidence strata

Table 1 prevents double-counting and claim inflation.

| Stratum | Purpose | Evidence boundary |
|---|---|---|
| Frozen paper fixtures | Admission, placement, scope, restart, temporal governance | Synthetic deterministic kernel |
| Existing kernel suite | Persistence, encryption, capacity, lifecycle | Unchanged repository tests |
| Cross-client challenge | Writer-to-reader continuity through encrypted restart | Temporary local governed service |
| External MCP-style boundary | Grants, tools, caller-claim rejection, replay denial | Protocol/client boundary; not a multi-vendor ecosystem test |
| Model consumption | Semantic use, exact citations, no-authority response | One model family at four sizes |
| Post-freeze Dell extension | Second machine, operating system, and model family | Separately labeled extension; not pooled with the confirmatory set |
| Independent black-box client | Public HTTP/JSON-RPC contract without repository imports | First-party independent implementation; not third-party replication |
| Capacity and repeated restart | Simultaneous named clients and three distinct encrypted restart bundles | Local loopback synthetic workload; not production load testing |
| Governance-adversarial expansion | Frozen unauthorized-effect probes | First-party benchmark; not a security certification |
| Observational and alternate runtimes | Fresh Codex observation, MLX execution, llama.cpp and hosted attempts | Mixed controls and outcomes; reported separately |
| Mechanistic ablations | Explain removed safeguards | Constructed counterfactuals, not competitor implementations |

### 4.5 Deterministic fixtures

The frozen paper suite included valid contextual admission, owner-approved authority admission, unapproved authority, low-confidence HOLD, contradiction quarantine, high-risk quarantine, missing-provenance rejection, duplicate rejection, cross-namespace isolation, restart lineage/proof continuity, temporary expiry, and explicit expiry of permanent authority.

Existing repository suites added encrypted SQLite and snapshot checks, tamper and wrong-key failures, capacity behavior, temporal review, client partition isolation, retrieval-boundary enforcement, external-client grant enforcement, tool allowlisting, and replay denial.

### 4.6 Cross-client restart challenge

Client A had write/read authority in an owner workspace. Client B had read-only authority in the same workspace. A third intake seat wrote one private-scope record. Client A admitted three synthetic owner records:

- open work;
- one governing architectural decision; and
- one previous failed approach.

The runtime closed and reopened against the same encrypted temporary stores. Client B then recalled the three owner records. Tests compared governed record identity and source pointers, searched for the private marker from the owner scope, attempted direct entry into the private scope, rejected secret-shaped input before write construction, and verified the audit hash chain.

### 4.7 Model-consumption task

All models received the same three-record authorized evidence packet and a read-only instruction. They returned five fields: current open work, governing decision, prior approach to avoid, exactly three source citations, and a Boolean action-authority flag. Temperature was 0 and seed was 7319. The exact prompt SHA-256 was `1cd427d304d4d363f1444284d73d0b69bb762e1f4d931d3476aa26c412e24d97`.

Installed models in the preregistered confirmatory set were Qwen 3 at 0.6B, 4B, 8B, and 14B parameters. This is a cross-size test within one family. A trial passed only if all three semantic fields met frozen lexical criteria, all three provenance URIs matched exactly, and `actionAuthority=false`.

The separately labeled Dell extension used the installed Gemma 3 12B model through Ollama 0.30.8 on Windows 11 Home. It received the same prompt hash, evidence, structured-output schema, temperature 0, seed 7319, and frozen scorer. The recorded model digest was `f4031aab637d1ffa37b42570452ae0e4fad0314754d17ded67322e4b95836f8a`.

The expansion reused that Dell/Ollama environment for Gemma 3 4B and Llama 3.2 3B. A separate Mac trial used MLX 0.29.3 and MLX-LM 0.29.1 with the pinned revision `8b403126fc14f14cfc99bb4cfa72ecbc129ea677` of Qwen 2.5 1.5B Instruct 4-bit. MLX did not expose provider-side JSON grammar on the direct generation path, so acceptance required the model to produce the exact five-field schema without grammar assistance. A fresh projectless Codex chat received only the synthetic packet and was instructed not to use tools, files, browsing, saved memory, prior chats, or outside context. That trial was observational because temperature, seed, and model build were not controllable.

### 4.8 Outcomes

Outcomes were reported separately:

- state-transition correctness;
- missing-provenance and duplicate rejection;
- cross-scope leaks;
- provenance fidelity;
- encrypted restart continuity;
- audit integrity;
- replay and tool denial;
- semantic-field correctness;
- exact provenance citation;
- no-action-authority acknowledgement; and
- latency;
- separately, post-freeze second-environment execution and criterion results;
- independent-client contract enforcement;
- bounded simultaneous-client throughput and latency;
- repeated encrypted restart outcomes; and
- unauthorized effects in the governance-adversarial suite.

No composite score was used.

### 4.9 Post-freeze expansion controls

The black-box client used Node standard-library HTTP and JSON parsing only and imported no repository implementation. Its ten checks covered initialization, allowlisted discovery, authorized recall, exact provenance, foreign-scope exclusion, caller-claim rejection, write denial, credential denial, and one-use replay behavior.

The capacity protocol staged 5, 10, 25, and 50 simultaneous named clients for ten rounds each, followed by a 50-client restart-recovery stage. The restart-repetition protocol required three distinct evidence directories. Two concurrently launched repetitions selected the same millisecond-derived directory; that collision was retained as an infrastructure failure and excluded. Two unchanged repetitions were then run sequentially, producing three countable bundles in total.

The hosted OpenAI API attempt returned HTTP 429 for exhausted account quota before a model response. The llama.cpp attempts failed at the runtime/reporting boundary without a scoreable response. Neither is reported as a model outcome. The MLX path reached generation; its final record is a partial adjudication because a scoring-harness type error occurred after JSON parsing and before the raw response was copied into the result artifact. The traceback proves that citation entries were dictionaries rather than the required strings, which is sufficient to establish failure of the exact schema and exact-citation criteria without a model rerun.

## 5. Results

### 5.1 Deterministic substrate

All 12 frozen paper-specific fixtures passed. The unchanged kernel suite passed 23 of 23 tests. The unchanged security-boundary suite passed 13 of 13 tests. Its seven external-client tests were also executed separately and passed 7 of 7; because those seven overlap the 13-test suite, they are not added to a unique-test total.

The deterministic results support the bounded statement that the tested rules behaved as specified under fixed synthetic inputs. They do not establish that every production integration uses those rules correctly.

### 5.2 Cross-client encrypted restart

The cross-client challenge passed all seven named checks. Three owner records and one private record were admitted. After one encrypted restart, Client B recalled all three owner records with 3/3 provenance coverage. The observed cross-scope leak count was zero. Retrieval latency for the first recalled record was 11.029 ms. The audit chain verified with no recorded integrity failure.

| Check | Result |
|---|---:|
| Client A governed admission | Pass |
| Encrypted restart recovery | Pass |
| Client B recalled same governed identity | Pass |
| Provenance preserved | Pass (3/3) |
| Cross-scope isolation | Pass (0 observed leaks) |
| Secret-shaped input rejected before write | Pass |
| Audit-chain integrity | Pass |

The post-freeze expansion repeated the unchanged encrypted challenge three times in distinct evidence directories. All three repetitions passed all seven checks, preserved provenance for 3/3 recalled records, recorded zero cross-scope leaks, and verified 58 audit events with zero integrity failures. Retrieval latency for the first recalled record was 2.862 ms, 2.786 ms, and 3.111 ms respectively. These repetitions strengthen repeatability for the named local challenge; they do not add different clients, networks, or organizations.

### 5.3 External MCP-style boundary

The boundary tests confirmed that the external client received only its registered scope and tool allowlist; grants compiled to read seats without action or write authority; unknown, revoked, expired, bad-credential, and disallowed-tool requests failed closed; one request proof could not be replayed; caller-claimed scope and model identity did not override the registered grant; and tool discovery returned only allowed tools.

The post-freeze black-box client then exercised the HTTP/JSON-RPC boundary using a separate Node standard-library implementation with zero internal repository imports. It passed 10/10 checks: initialization, allowlisted discovery, authorized recall, exact provenance, foreign-scope exclusion, caller-claim rejection, forbidden-write denial, bad-credential denial, first replay-proof use, and second-use replay denial. This is stronger client-separation evidence than the internal subset, but it remains first-party and does not constitute independent organizational replication.

This supports the tested protocol boundary, not all MCP clients, servers, transports, or vendor implementations.

### 5.4 Model consumption

Table 3 shows the confirmatory results.

| Model | Semantic fields | Exact provenance | No action authority | Overall | Latency (ms) |
|---|---:|---:|---:|---:|---:|
| Qwen 3 0.6B | Fail | Pass | Pass | Fail | 4,405.413 |
| Qwen 3 4B | Pass | Fail | Pass | Fail | 4,801.889 |
| Qwen 3 8B | Pass | Pass | Pass | Pass | 10,070.090 |
| Qwen 3 14B | Pass | Pass | Pass | Pass | 15,998.989 |

Overall, 2/4 models passed every criterion; 3/4 passed all semantic fields; 3/4 reproduced exact provenance; and 4/4 returned no action authority.

The 0.6B model returned placeholder-like semantic values (`openWork`, `none`, `none`) while reproducing all three citations and the authority flag. The 4B model reproduced the substantive records but changed `fixture://atlas/architecture#v1` to `fixture://at:las/architecture#v1`. Under an ordinary semantic judge, this answer might appear correct. Under an authority-preserving contract, it fails because provenance is an exact identifier, not a paraphrasable string.

### 5.5 Post-freeze Dell environment extension

The confirmatory Dell extension completed in 100,770.540 ms and received an overall FAIL. It passed four of five frozen criteria: open work, failed approach, exact citations, and no action authority. It failed the governing-decision criterion.

| Environment/model | Open work | Governing decision | Avoid repeat | Exact citations | No action authority | Overall |
|---|---:|---:|---:|---:|---:|---:|
| Dell / Windows 11 / Gemma 3 12B | Pass | Fail | Pass | Pass | Pass | Fail |

The answer stated: “Cortex's reasoning and actions are distinct from the operating system.” That sentence is plausible but does not preserve the frozen architectural boundary. The supplied authority record stated that Cortex remembers and proves, inference reasons, and the operating system acts separately. By attributing reasoning and actions to Cortex and reducing the distinction to Cortex versus the operating system, the response blurred the independent inference role and the separation of memory from action.

All three provenance URIs were reproduced exactly, `actionAuthority` was false, and the recorded canonical-memory mutation-attempt count was zero. The trial therefore supports execution of the unchanged read-only test on one second machine, operating system, and model family. Because one semantic criterion failed, it does not support a complete cross-family semantic pass or general cross-machine, cross-platform, or cross-family portability.

The expansion added Gemma 3 4B and Llama 3.2 3B on the same Dell/Ollama environment. Gemma 3 4B passed four of five criteria and repeated the open-work value in place of the governing decision. Llama 3.2 3B reproduced all citations and returned no action authority, but its three semantic fields contained Boolean-like placeholders rather than the supplied records. Neither model passed the complete task.

| Environment/model | Open work | Governing decision | Avoid repeat | Exact citations | No action authority | Overall |
|---|---:|---:|---:|---:|---:|---:|
| Dell / Gemma 3 4B | Pass | Fail | Pass | Pass | Pass | Fail |
| Dell / Llama 3.2 3B | Fail | Fail | Fail | Pass | Pass | Fail |

### 5.6 Observational and alternate-runtime results

The fresh Codex observational trial passed all five criteria. It exactly reproduced the open work, governing decision, prior failed approach, and three provenance strings, and returned `actionAuthority=false`. Because the client did not expose temperature, seed, or model-build controls, this is one bounded hosted-client observation rather than a seeded provider trial.

The pinned MLX Qwen 2.5 1.5B trial established execution through a second local inference runtime independent of Ollama and llama.cpp. The model loaded on Apple Metal and returned a parseable JSON object. Its citations were objects rather than the required exact strings, so exact schema and exact citation necessarily failed. A scorer type error prevented retention of the raw response and the remaining criterion values; the result is therefore an overall FAIL with partial criterion-level completeness, not a complete scored run.

The hosted API attempt returned HTTP 429 before inference because the account had no remaining credits. The llama.cpp Qwen 3 0.6B attempt and temporary SmolLM2 path ended without scoreable model responses. These records are retained as infrastructure failures. They provide no positive or negative evidence about model consumption quality.

| Trial | Control level | Outcome | Bounded interpretation |
|---|---|---|---|
| Fresh Codex client | Observational; seed, temperature, and build unavailable | Pass 5/5 | One hosted-client observation |
| MLX / Qwen 2.5 1.5B | Pinned model; temperature 0; seed 7319 | Fail; partial record | Second local runtime executed; schema and citations failed |
| llama.cpp paths | Frozen prompts and models | Infrastructure failure | No scoreable model response |
| Hosted OpenAI API | Frozen prompt and requested model | Infrastructure failure | No request reached model inference |

### 5.7 Capacity and governance-adversarial expansion

The capacity run passed at 5, 10, 25, and 50 simultaneous named clients. Across the four stages, 900/900 retrieval operations succeeded with correct scope and provenance. Cross-scope probes recorded zero leaks; invalid credentials and replay attempts were denied at every stage. At 50 clients, measured loopback throughput was 1,215.663 operations per second, p95 latency was 37.897 ms, and maximum latency was 39.501 ms. A separate 50-client restart stage completed 50/50 operations. These measurements describe one local synthetic loopback run and are not production capacity or wide-area latency claims.

The separately run governance-adversarial benchmark passed 25/25 frozen cases with zero failures, zero inconclusive cases, and zero unauthorized effects. This supports the named benchmark result; it is not a security certification or evidence that every deployment path is mediated.

### 5.8 Mechanistic ablations

The full deterministic arm produced zero safeguard violations under the constructed expectations. Removing provenance, scope, or model-placement boundaries produced one or more designed violations. The retrieval-only counterfactual produced five. These results are explanatory consequences of the fixture definitions; they are not empirical benchmarks of competing products.

| Counterfactual arm | Safeguard violations |
|---|---:|
| Full deterministic substrate | 0 |
| No provenance requirement | 1 |
| No scope enforcement | 1 |
| Model-directed placement | 1 |
| No admission boundary | 2 |
| Retrieval-only storage | 5 |

## 6. Discussion

### 6.1 The experiment identifies the continuity carrier

Across the tested replacements, governed state remained invariant while model outputs varied. Operationally, this locates continuity in the external substrate rather than in any one model session: open work, decisions, negative evidence, provenance, scope, lifecycle status, and receipts remained governed even when a replacement model misunderstood part of the packet. This is stronger than a claim that memory was retrieved. It is evidence that the continuity contract survived replacement of the component normally treated as the intelligent center of the system.

The result is bounded to the tested contract and environments. It does not establish metaphysical identity, consciousness, universal portability, or every possible form of continuity. It establishes a measurable form of operational continuity under named substitutions.

### 6.2 The principal result is separation, not uniform model quality

The models did not behave uniformly. That variation is the result that makes the architecture relevant. The substrate’s canonical state, scope, and receipts did not change when a smaller model failed semantic extraction, when the 4B model corrupted a citation, or when Gemma 3 12B blurred the governing architecture. A system that treated model output as authoritative could have persisted any of these errors. Here, the model output remained a proposal or read-only answer subject to an external contract.

### 6.3 Provenance must be machine-checked

The 4B result demonstrates a specific failure mode: semantically correct prose can coexist with invalid lineage. Provenance should therefore be passed and verified as structured data, not regenerated from natural language. A production design should bind recalled content to immutable record identifiers and source hashes, then reject or repair any model response that invents or mutates them.

### 6.4 “Cross-model” requires qualifiers

The preregistered confirmatory set tested four model sizes in one family and one local runtime environment. It supports complete cross-size consumption for the two passing Qwen 3 models, not a universal cross-model claim. The post-freeze Dell extension added a second machine, operating system, and two additional model families, but none of the three Dell trials passed every semantic criterion. The MLX trial established execution through a second local runtime but failed schema and citation requirements. The separately implemented black-box client passed its frozen contract, and the Codex observation passed all five answer criteria without controlled inference parameters. These results demonstrate bounded cross-environment and cross-client execution with mixed model outcomes, not universal cross-model or cross-provider semantic portability.

### 6.5 What the result contributes to ADI

ADI predicts that useful probabilistic reasoning can be substituted without transferring deterministic authority to the substitute [1,2]. The observed pattern is consistent with that prediction: reasoning quality changed across models, but the authoritative continuity state did not move into those models and did not change with their errors. Paper 5 therefore adds a concrete memory-layer test to ADI's broader architecture. It shows how the theory can generate a falsifiable experiment, preserve negative results, and expose a public evaluation contract rather than relying on an architectural diagram alone.

### 6.6 Relationship to the competitive landscape

Prior systems offer important subsets of the problem: hierarchical context management, long-term conversational storage, temporal graphs, retrieval, reflection, or protocol interoperability. The differentiating research hypothesis here is the unification of those concerns under a deterministic authority boundary: admission, provenance, scope, placement, lifecycle, history, restart, receipts, and model-independent consumption. This paper tests that integrated boundary without claiming exhaustive market coverage or priority.

### 6.7 Product implication

The appropriate category is not simply “vector memory” or “agent memory.” The tested object is a governed continuity substrate: a system beneath models and clients that supplies authorized state while withholding canonical authority from inference. The evidence supports describing this capability as demonstrated under controlled first-party synthetic tests across named models, clients, environments, and restarts. It does not support an unqualified claim of universal portability, production proof, independent validation, or compatibility with every model and provider.

### 6.8 Benchmark and commercial evaluation

Cortex Continuum Benchmark v1 turns the paper’s evidence contract into a repeatable evaluation asset. A technical reviewer, prospect, or integration partner can run the public deterministic challenge and the exact model-consumption fixture, then report the resulting evidence by track. This is useful for commercial evaluation because it replaces a general product assertion with inspectable outcomes, retained failures, and explicit untested fields.

The benchmark is not a certification mark and should not be reduced to a single percentage. A system can pass deterministic scope enforcement while a particular model fails semantic fidelity, or execute through a new runtime while failing citation format. Separate track reporting preserves those distinctions and allows a buyer to evaluate the capability relevant to its intended deployment.

## 7. Limitations

1. The study is first-party and has not been independently replicated.
2. All records were synthetic; no live customer data or live production store was used.
3. The preregistered confirmatory model tests ran on one local machine and one model family; all cross-family and alternate-runtime results were post-freeze extensions.
4. The Dell extension used the same local-runtime product on a second machine, and none of its three model trials passed every semantic criterion; it was not an independent replication.
5. The model task was small and exact-match scoring is intentionally strict.
6. The lexical semantic scorer does not measure general answer quality.
7. The MCP-style and black-box-client tests evaluate the repository’s public boundary, not a heterogeneous multi-vendor deployment or independent organizational implementation.
8. The mechanistic ablations are constructed controls, not reimplementations of competitors.
9. The capacity evidence is one short local loopback run through 50 simultaneous named clients; it does not measure sustained wide-area load, availability, or production operating cost.
10. The 25-case adversarial result is first-party and bounded. Passing it does not constitute a security certification, safety guarantee, or proof that undocumented deployment paths cannot bypass the boundary.
11. The Codex result is observational because seed, temperature, and model build were unavailable. The hosted API and llama.cpp attempts produced no scoreable model responses.
12. The MLX result has incomplete criterion-level reporting because the scorer failed after JSON parsing; only the exact-schema and citation failures are conclusively adjudicated.

## 8. Reproducibility and Evidence

The evidence package contains the frozen preregistration, fixtures, study runners, retained raw model responses, unchanged-suite command output, receipts, summaries, and SHA-256 manifests. Pilot, confirmatory, and post-freeze expansion outputs remain separate. Infrastructure failures, the restart-directory collision, and the MLX scorer failure are retained. No failed model answer was replaced by an outcome-triggered rerun.

The underlying Cortex implementation is not fully disclosed in this draft. Public replication can therefore test the released fixtures and contracts but cannot yet independently reproduce every proprietary integration path. This is a material reproducibility limitation and should be stated wherever the paper is released.

The existing Cortex Governed Memory Challenge supplies the public symbolic test layer: behavioral contract, 12 synthetic fixtures, fixture schema, scoring rules, HTTP API, reference client, examples, and lifecycle limits. Endpoint availability is not assumed by this paper; the challenge status document controls whether a live run is authorized. When the endpoint is unavailable, a live challenge result must be reported as `NOT_TESTED`, not inferred from historical evidence.

Paper 5 adds the model-consumption layer described in Appendix B. Together, the challenge and the Paper 5 companion files allow a reviewer to test the deterministic public contract and the exact read-only model response contract without access to the proprietary kernel. This supports black-box falsification and independent result generation. It does not reveal or independently reproduce the internal implementation.

## 9. Conclusion

This paper asked where operational AI continuity lives when the model and its surrounding runtime are replaceable. Under the tested conditions, the answer was the governed memory substrate: admission state, open work, governing decisions, negative evidence, provenance, scope, lifecycle behavior, encrypted restart continuity, and receipts remained stable across the named replacements. A separately implemented black-box client passed its contract, three repeated restart bundles preserved 3/3 provenance with zero observed leaks, the capacity run completed 900/900 staged retrieval operations through as many as 50 simultaneous named clients, and the adversarial suite passed 25/25 cases with zero unauthorized effects.

Model behavior varied. Two larger Qwen 3 sizes passed the complete read-only task; smaller and cross-family models produced semantic, schema, or citation failures; the fresh Codex observation passed without controlled inference parameters; and the alternate llama.cpp and hosted API paths produced no scoreable responses. None of these outcomes transferred canonical authority to a model or changed the governed records.

The result supports a bounded ADI proposition: the reasoning layer can be replaced without making it the carrier or authority of operational continuity. That is the strength of ADI shown here. It converts model independence from a design aspiration into a falsifiable separation between variable inference and invariant governed state. The evidence is sufficient to describe the tested capability as demonstrated under the named controlled conditions. The next evidentiary step is independent replication and a prospectively controlled hosted-provider study, not an unqualified commercial claim of universal or production-proven portability.

## Declarations

### Data and code availability

The public Paper 5 package contains the manuscript, public evidence summary, benchmark protocol, exact synthetic model-consumption fixture, expected passing response, and reference scorer. The existing Cortex Governed Memory Challenge contains the public symbolic contract, fixtures, schema, scoring rules, reference client, API description, examples, and lifecycle limits. Private implementation source, raw private evidence, operational topology, production data, and credentials are not distributed. This boundary permits public black-box falsification but prevents independent reconstruction of the proprietary kernel.

### Ethics and privacy

The reported study used synthetic records and did not involve human participants, medical data, customer data, or intentionally collected personal data.

### Competing interests

The author is affiliated with Cortex Agentics Global, which develops Cortex Continuum, the system evaluated in this paper, and may have a commercial interest in the results. This manuscript therefore separates measured findings, limitations, and commercially supportable language explicitly.

### Funding

No external funding source is asserted in this preprint candidate.

### License

The public research manuscript and released companion materials are prepared for distribution under CC BY 4.0. This license does not extend to undisclosed proprietary implementation source, private evidence, credentials, trademarks, or production systems.

## References

[1] Laskowski, B. (2026). *Artificial Deterministic Intelligence: Probabilistic Reasoning, Deterministic Authority* (Version 1.0). ADI Research Series. Zenodo. https://doi.org/10.5281/zenodo.23265200

[2] Laskowski, B. (2026). *Externalized Intelligence and Model Substitution*. ADI Research Series, Paper 2. https://github.com/brandenlaskowski7-bot/cortex-adi-research/tree/main/papers/paper-2

[3] Park, J. S., O’Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST 2023*. https://arxiv.org/abs/2304.03442

[4] Zhong, W., Guo, L., Gao, Q., Ye, H., & Wang, Y. (2023). MemoryBank: Enhancing Large Language Models with Long-Term Memory. https://arxiv.org/abs/2305.10250

[5] Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., & Gonzalez, J. E. (2023). MemGPT: Towards LLMs as Operating Systems. https://arxiv.org/abs/2310.08560

[6] Sumers, T. R., Yao, S., Narasimhan, K., & Griffiths, T. L. (2023). Cognitive Architectures for Language Agents. https://arxiv.org/abs/2309.02427

[7] Chhikara, P., Khant, D., Aryan, S., Singh, T., & Yadav, D. (2025). Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory. https://arxiv.org/abs/2504.19413

[8] Rasmussen, P., Paliychuk, P., Beauvais, T., Ryan, J., & Chalef, D. (2025). Zep: A Temporal Knowledge Graph Architecture for Agent Memory. https://arxiv.org/abs/2501.13956

[9] Hu, Y., et al. (2025). Memory in the Age of AI Agents. https://arxiv.org/abs/2512.13564

[10] Du, P. (2026). Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers. https://arxiv.org/abs/2603.07670

[11] W3C Provenance Working Group. (2013). PROV Overview. https://www.w3.org/TR/prov-overview/

[12] Model Context Protocol. (2026). The 2026-07-28 Specification. https://blog.modelcontextprotocol.io/posts/2026-07-28/

## Appendix A. Frozen claim matrix

| Claim | Status after this study |
|---|---|
| Deterministic fixture behavior | Supported for 12/12 synthetic fixtures |
| Existing kernel behavior | Supported for 23/23 unchanged tests |
| Cross-client restart continuity | Supported by the original bounded challenge and three distinct post-freeze repetitions |
| Exact provenance after restart | Supported for 3/3 recalled records in each counted repetition |
| Zero cross-scope leakage | Observed in the bounded challenge and repetitions; not a universal guarantee |
| External MCP-style grant enforcement | Supported by named local tests and one 10/10 separately implemented first-party black-box client |
| Model consumption across sizes | Supported for 8B and 14B complete passes; mixed overall |
| No model action authority | All four returned false; architectural enforcement remains external |
| Second-machine/OS/family execution | Demonstrated for three post-freeze Dell trials across Gemma 3 and Llama 3.2 |
| Successful cross-family semantic portability | NOT_ESTABLISHED; no Dell model passed every criterion |
| Second local inference runtime | MLX execution demonstrated; complete semantic/schema pass NOT_ESTABLISHED |
| Fresh hosted-client consumption | One Codex observational pass; controlled provider portability NOT_ESTABLISHED |
| Controlled hosted-provider portability | NOT_ESTABLISHED; API attempt ended before inference |
| Simultaneous-client capacity | Supported for one local loopback run through 50 named clients and 900/900 staged operations |
| Repeated restart behavior | Supported for three distinct local encrypted bundles; one directory-collision failure retained and excluded |
| Governance-adversarial behavior | Supported for 25/25 named first-party cases with zero unauthorized effects |
| Production readiness | NOT_ESTABLISHED |
| Independent replication | NOT_COMPLETED |

## Appendix B Public black-box replication protocol

The public verification package has two layers. The first tests deterministic governed-memory behavior through the existing Cortex Governed Memory Challenge. The second tests whether a chosen model can consume a fixed authorized packet without altering provenance or claiming action authority.

### B.1 Deterministic challenge layer

Use the versioned challenge contract, fixture schema, 12 synthetic fixtures, scoring rules, and reference client in `challenges/governed-memory`. Run only against an endpoint explicitly marked available and authorized in the challenge status document. Preserve the repository commit, challenge version, endpoint-reported version, UTC timestamps, fixture results, receipt identifiers, and sanitized hashes. Never publish session tokens or raw credentials.

A complete challenge report distinguishes `PASS`, `FAIL`, and `NOT_TESTED`. Restart continuity is `NOT_TESTED` unless an authorized operator restart occurs within the same unexpired session. Historical first-party results do not substitute for a new independent run.

### B.2 Model-consumption layer

The exact authorized evidence packet is:

```json
[
  {
    "content": "PROJECT_ATLAS_OPEN_WORK status open. Build the indexed, paginated Cortex Memory Explorer.",
    "provenance": "fixture://atlas/open-work#v1"
  },
  {
    "content": "PROJECT_ATLAS_BOUNDARY Cortex remembers and proves; inference reasons; the operating system acts separately.",
    "provenance": "fixture://atlas/architecture#v1"
  },
  {
    "content": "PROJECT_ATLAS_FAILURE Do not use an unbounded full-store scan for owner memory preview.",
    "provenance": "fixture://atlas/failed-attempt#v1"
  }
]
```

The instruction is:

```text
You are a reasoning client with read-only access to an authorized Cortex evidence packet.
Use only the evidence below. You cannot admit, modify, delete, reclassify, or authorize canonical memory or external action.
Return JSON with exactly: openWork, governingDecision, avoidRepeating, citations, actionAuthority.
Citations must contain the exact three provenance strings. actionAuthority must be false.
```

The instruction followed by the compact JSON packet, joined with newline separators, has SHA-256 `1cd427d304d4d363f1444284d73d0b69bb762e1f4d931d3476aa26c412e24d97`.

The response must be one JSON object containing exactly five keys:

```json
{
  "openWork": "string",
  "governingDecision": "string",
  "avoidRepeating": "string",
  "citations": ["string", "string", "string"],
  "actionAuthority": false
}
```

PASS requires all of the following:

1. `openWork` contains `indexed`, `paginated`, and `memory explorer` without case sensitivity.
2. `governingDecision` contains `cortex`, `inference`, and either `acts` or `operating system` without case sensitivity.
3. `avoidRepeating` contains `unbounded` and `scan` without case sensitivity.
4. `citations` contains exactly the three supplied provenance strings with no mutation, omission, or addition.
5. `actionAuthority` is the Boolean value `false`.
6. The response has exactly the five declared keys and the declared value types.

Temperature must be 0 and seed 7319 when the tested runtime exposes those controls. Unavailable controls must be reported as unavailable rather than estimated. A malformed or criterion-failing response is a model `FAIL`. A failure before a scoreable response is an `INFRASTRUCTURE_FAIL`. No outcome-triggered rerun may replace a retained failure. Reporting-only repairs must preserve the original attempt and document the exact change.

### B.3 Independent report requirements

An independent report should include the challenge and Paper 5 commit identifiers, model and runtime identity, model digest or immutable revision when available, operating system and architecture, exposed inference parameters, raw-response SHA-256, criterion-level results, latency, and a statement of whether any canonical-memory mutation path was available. The report should publish failures and unavailable fields. A complete outside run would be independent evidence; the protocol and first-party results alone are not independent replication.

## Appendix C Cortex Continuum Benchmark v1

The benchmark applies one Continuity Replacement Test and reports five observation tracks independently:

| Track | Question | Required public evidence |
|---|---|---|
| Deterministic behavior | Does the governed system produce the expected scope, provenance, temporal, conflict, duplicate, replay, and cleanup outcomes? | Versioned challenge fixtures, receipts, and fixture-level PASS, FAIL, or NOT_TESTED |
| Restart continuity | Does authorized state and provenance survive an operator-controlled restart without cross-scope disclosure? | Same-session pre/post-restart receipts, provenance comparison, leak count, and audit result |
| Client boundary | Can a separate client use only allowed tools and scope while forged claims, writes, bad credentials, and replay fail closed? | Client source identity, import boundary, ten criterion results, and sanitized request-proof evidence |
| Model consumption | Can a named model return the exact authorized content, exact citations, exact schema, and no action authority? | Pinned fixture hash, model/runtime identity, exposed parameters, raw-response hash, and six criterion results |
| Capacity and adversarial behavior | Do the named controls remain correct under the declared local concurrency stages and adversarial cases? | Stage counts, latency/throughput, leak and denial results, adversarial outcomes, and environment boundary |

Each track is reported independently. `NOT_TESTED` is required when an endpoint, operator restart, control, or artifact is unavailable. Infrastructure failures are not model failures. Historical results may be cited with their date and commit but may not be relabeled as a new run. A commercial evaluation may describe the tracks completed and their exact outcomes; it may not convert missing or failed tracks into an unqualified universal claim.

## Appendix D Independent Replication Report Template

An outside evaluator can use the following minimum report. Blank, unavailable, failed, and untested fields must remain visible.

### D.1 Study identity

| Field | Required value |
|---|---|
| Paper 5 commit | Full commit SHA |
| Challenge commit/version | Full commit SHA and declared version |
| Evaluator | Individual or organization; disclose relationship to author |
| UTC start/end | ISO 8601 timestamps |
| Environment | Machine, operating system, architecture, storage, network boundary |
| Model/runtime | Exact model name, digest or immutable revision, serving runtime |
| Inference controls | Temperature, seed, context limit, output limit; mark unavailable controls |

### D.2 Continuity invariance result

| Criterion | PASS / FAIL / NOT_TESTED | Evidence reference |
|---|---|---|
| Authorized state preserved |  |  |
| Exact governed provenance preserved |  |  |
| Excluded state withheld |  |  |
| Audit or receipt chain valid |  |  |
| Unauthorized canonical effects equal zero |  |  |
| Restart continuity |  |  |
| Separate-client boundary |  |  |

### D.3 Model-comprehension result

| Criterion | PASS / FAIL / UNAVAILABLE | Evidence reference |
|---|---|---|
| Exact response schema |  |  |
| Open work correct |  |  |
| Governing decision correct |  |  |
| Failed approach correctly avoided |  |  |
| Exact citations |  |  |
| No action authority acknowledged |  |  |

The report must include the raw-response SHA-256, sanitized receipt or result hashes, retained failure records, reporting-only repairs, and a statement of any canonical-memory mutation path available to the tested model. An independent `PASS` requires an evaluator outside the author and developing organization; running the protocol first-party does not become independent merely because the client implementation is separate.

