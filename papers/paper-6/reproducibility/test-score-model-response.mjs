import assert from 'node:assert/strict'
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises'
import { createHash } from 'node:crypto'
import { tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const here = resolve(fileURLToPath(new URL('.', import.meta.url)))
const scorer = join(here, 'score-model-response.mjs')
const expected = join(here, 'expected-pass-response.json')
const work = await mkdtemp(join(tmpdir(), 'paper6-scorer-'))
function run(response, extra = []) {
  const result = spawnSync(process.execPath, [scorer, response, ...extra], { encoding: 'utf8' })
  return { code: result.status, output: JSON.parse(result.stdout) }
}
try {
  const pass = run(expected)
  assert.equal(pass.code, 0); assert.equal(pass.output.disposition, 'PASS')

  const badAnswerPath = join(work, 'criterion-fail.json')
  const badAnswer = JSON.parse(await readFile(expected, 'utf8'))
  badAnswer.openWork = 'Do something unrelated.'
  await writeFile(badAnswerPath, JSON.stringify(badAnswer))
  const failed = run(badAnswerPath)
  assert.equal(failed.code, 1); assert.equal(failed.output.disposition, 'FAIL')
  assert.equal(failed.output.criteria.openWork, false); assert.ok(failed.output.rawResponseSha256)

  const malformedPath = join(work, 'malformed.json')
  const malformed = '{not valid JSON\n'
  await writeFile(malformedPath, malformed)
  const malformedResult = run(malformedPath)
  assert.equal(malformedResult.code, 1); assert.equal(malformedResult.output.disposition, 'FAIL')
  assert.equal(malformedResult.output.error, 'malformed_response_json')
  assert.equal(malformedResult.output.rawResponseSha256, createHash('sha256').update(malformed).digest('hex'))

  const missing = run(join(work, 'missing.json'))
  assert.equal(missing.code, 2); assert.equal(missing.output.disposition, 'INFRASTRUCTURE_FAIL')
  assert.equal(missing.output.error, 'response_read_error'); assert.equal(missing.output.rawResponseSha256, undefined)

  const invalidFixture = join(work, 'invalid-fixture.json')
  await writeFile(invalidFixture, '{"schemaVersion":"invalid"}')
  const invalid = run(expected, ['--fixture', invalidFixture])
  assert.equal(invalid.code, 2); assert.equal(invalid.output.disposition, 'INFRASTRUCTURE_FAIL')
  assert.equal(invalid.output.error, 'invalid_fixture_structure')
  console.log('score-model-response regression tests: PASS')
} finally {
  await rm(work, { recursive: true, force: true })
}
