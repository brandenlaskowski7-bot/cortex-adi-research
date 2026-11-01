# ADI adversarial fixture v1

This is a synthetic, deterministic reference fixture. It does not call a model,
run an external tool, or demonstrate production behavior. Its only purpose is
to freeze the expected outcomes of a proposed cross-configuration experiment.

Run it with:

```sh
node run.js
```

The four configurations and five cases are fixed in `run.js`. A real comparison
must substitute real, independently implemented configurations and preserve the
same decision vocabulary: `execute`, `hold`, `ask_user`, and
`definition_repair`.

The cases cover model-to-user echo, supersession, operation substitution, a
missing provider requirement, and replay of a superseded memory record. The
fixture makes a falsifiable expectation explicit: first-origin tracking,
operation binding, separate ownership of provider requirements, and a
current-record check each address distinct failure modes. They must be tested
against independently implemented systems before drawing conclusions about a
real deployment.
