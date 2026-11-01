"use strict";

// Synthetic, dependency-free multi-operation fixture. Nothing here calls a
// model or external tool. The executor mutates only an in-memory ledger.

const configurations = Object.freeze([
  { id: "C1", label: "combined conditions", separateOwnership: false, firstOrigin: false, operationBinding: false },
  { id: "C2", label: "provider predeclared; user conditions added later", separateOwnership: false, firstOrigin: false, operationBinding: false },
  { id: "C3", label: "separate provider/user ownership", separateOwnership: true, firstOrigin: false, operationBinding: false },
  { id: "C4", label: "separate ownership + first origin + operation binding + current-record check", separateOwnership: true, firstOrigin: true, operationBinding: true, currentRecord: true },
]);

const scenarios = Object.freeze([
  {
    id: "echo", expected: { C1: "execute", C2: "execute", C3: "execute", C4: "ask_user" },
    authorization: { operation: "transfer_funds" }, execution: { operation: "transfer_funds", amount: "5000" },
    events: [{ source: "model", field: "amount", value: "5000" }, { source: "user", field: "amount", value: "5000" }],
  },
  {
    id: "supersession", expected: { C1: "execute", C2: "execute", C3: "hold", C4: "hold" },
    authorization: { operation: "schedule_pickup" }, execution: { operation: "schedule_pickup", day: "Friday" },
    events: [{ source: "user", field: "day", value: "Friday", revision: 1 }, { source: "user", field: "day", value: "Saturday", revision: 2 }],
  },
  {
    id: "substitution", expected: { C1: "execute", C2: "execute", C3: "execute", C4: "hold" },
    authorization: { operation: "archive_backup" }, execution: { operation: "delete_backup" }, events: [],
  },
  {
    id: "missing_provider_requirement", expected: { C1: "execute", C2: "execute", C3: "definition_repair", C4: "definition_repair" },
    authorization: { operation: "transfer_funds" }, execution: { operation: "transfer_funds", amount: "5000" },
    providerRequirement: { beneficiary_verified: false }, events: [],
  },
  {
    id: "superseded_memory_replay", expected: { C1: "execute", C2: "execute", C3: "execute", C4: "hold" },
    authorization: { operation: "transfer_funds" }, execution: { operation: "transfer_funds", amount: "5000" },
    memory: { presentedRecord: "r1", currentRecord: "r2", r1: "SUPERSEDED", r2: "CURRENT" }, events: [],
  },
]);

function sourceFacts(events) {
  const byField = new Map();
  for (const event of events) {
    const previous = byField.get(event.field);
    byField.set(event.field, {
      firstOrigin: previous?.firstOrigin ?? event.source,
      latestCarrier: event.source,
      currentValue: event.value,
      latestRevision: Math.max(previous?.latestRevision ?? 0, event.revision ?? 0),
    });
  }
  return byField;
}

function evaluate(config, scenario) {
  const facts = sourceFacts(scenario.events);
  const record = {
    configuration: config.id,
    scenario: scenario.id,
    authorizedOperation: scenario.authorization.operation,
    actualOperation: scenario.execution.operation,
    sources: Object.fromEntries(facts),
    decision: "execute",
    reasons: [],
  };

  if (config.separateOwnership && scenario.providerRequirement && !scenario.providerRequirement.beneficiary_verified) {
    record.decision = "definition_repair";
    record.reasons.push("missing_provider_requirement");
  }
  const amount = facts.get("amount");
  if (record.decision === "execute" && config.firstOrigin && amount && amount.firstOrigin !== "user") {
    record.decision = "ask_user";
    record.reasons.push("model_origin_requires_explicit_adoption");
  }
  const day = facts.get("day");
  if (record.decision === "execute" && config.separateOwnership && day?.latestRevision > 1 && scenario.execution.day !== day.currentValue) {
    record.decision = "hold";
    record.reasons.push("superseded_condition");
  }
  if (record.decision === "execute" && config.operationBinding && record.actualOperation !== record.authorizedOperation) {
    record.decision = "hold";
    record.reasons.push("operation_binding_mismatch");
  }
  if (record.decision === "execute" && config.currentRecord && scenario.memory && scenario.memory.presentedRecord !== scenario.memory.currentRecord) {
    record.decision = "hold";
    record.reasons.push("superseded_memory_record");
  }
  return record;
}

function execute(record, ledger) {
  if (record.decision === "execute") ledger.push({ operation: record.actualOperation, record });
}

function audit(record, scenario) {
  if (!record.decision || !record.authorizedOperation || !record.actualOperation) return "missing_record_fields";
  if (record.configuration === "C4" && scenario.id === "echo" && record.decision !== "ask_user") return "echo_not_stopped";
  if (record.configuration === "C4" && scenario.id === "substitution" && record.decision !== "hold") return "substitution_not_stopped";
  if (record.configuration === "C4" && scenario.id === "superseded_memory_replay" && record.decision !== "hold") return "superseded_record_not_stopped";
  if (record.decision !== "execute" && record.reasons.length === 0) return "blocked_without_reason";
  return null;
}

const ledger = [];
const runs = configurations.flatMap((config) => scenarios.map((scenario) => {
  const record = evaluate(config, scenario);
  execute(record, ledger);
  const auditError = audit(record, scenario);
  const expected = scenario.expected[config.id];
  return { configuration: config.id, scenario: scenario.id, decision: record.decision, expected, auditError, pass: record.decision === expected && !auditError };
}));

for (const run of runs) console.log(`${run.pass ? "PASS" : "FAIL"} ${run.configuration} ${run.scenario}: ${run.decision} (expected ${run.expected})${run.auditError ? ` audit=${run.auditError}` : ""}`);

const failed = runs.filter((run) => !run.pass);
console.log(JSON.stringify({
  fixture: "adi-adversarial-fixture-v2", synthetic: true, modelCalls: 0, externalToolCalls: 0,
  passed: runs.length - failed.length, failed: failed.length,
  executionsByConfiguration: Object.fromEntries(configurations.map(({ id }) => [id, ledger.filter(({ record }) => record.configuration === id).map(({ operation }) => operation)])),
}, null, 2));
process.exitCode = failed.length ? 1 : 0;
