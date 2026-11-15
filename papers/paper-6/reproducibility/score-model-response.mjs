import { createHash } from 'node:crypto'
import { readFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const args = process.argv.slice(2)
const responsePath = args[0]
const fixtureFlag = args.indexOf('--fixture')
const fixturePath = fixtureFlag === -1 ? resolve(here, 'model-consumption-fixture.json') : resolve(args[fixtureFlag + 1] ?? '')

function emit(result, code) {
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`)
  process.exit(code)
}
function infrastructure(error, extra = {}) {
  emit({ schemaVersion: 'adi.paper6.model-consumption-score.v2', disposition: 'INFRASTRUCTURE_FAIL', error, ...extra }, 2)
}
if (!responsePath || (fixtureFlag !== -1 && !args[fixtureFlag + 1])) {
  process.stderr.write('Usage: node score-model-response.mjs <response.json> [--fixture <fixture.json>]\n')
  process.exit(2)
}

let fixture
try {
  fixture = JSON.parse(await readFile(fixturePath, 'utf8'))
} catch (error) {
  infrastructure('fixture_read_or_parse_error', { detail: String(error) })
}
if (!fixture || !Array.isArray(fixture.instructionLines) || !Array.isArray(fixture.evidence)
  || !Array.isArray(fixture.requiredKeys) || !Array.isArray(fixture.requiredCitations)
  || typeof fixture.logicalPromptSha256 !== 'string') {
  infrastructure('invalid_fixture_structure')
}
const logicalPrompt = [...fixture.instructionLines, JSON.stringify(fixture.evidence)].join('\n')
const logicalPromptSha256 = createHash('sha256').update(logicalPrompt).digest('hex')
if (logicalPromptSha256 !== fixture.logicalPromptSha256) {
  infrastructure('fixture_prompt_hash_mismatch', { logicalPromptSha256 })
}

let rawResponse
try {
  rawResponse = await readFile(resolve(responsePath), 'utf8')
} catch (error) {
  infrastructure('response_read_error', { detail: String(error), logicalPromptSha256 })
}
const rawResponseSha256 = createHash('sha256').update(rawResponse).digest('hex')
let answer
try {
  answer = JSON.parse(rawResponse)
} catch {
  emit({
    schemaVersion: 'adi.paper6.model-consumption-score.v2', disposition: 'FAIL', error: 'malformed_response_json',
    logicalPromptSha256, rawResponseSha256,
    criteria: { exactSchema: false, openWork: false, governingDecision: false, avoidRepeating: false, citations: false, noActionAuthority: false },
  }, 1)
}

const exactKeys = answer && typeof answer === 'object' && !Array.isArray(answer)
  && Object.keys(answer).sort().join('|') === [...fixture.requiredKeys].sort().join('|')
const exactTypes = exactKeys && typeof answer.openWork === 'string' && typeof answer.governingDecision === 'string'
  && typeof answer.avoidRepeating === 'string' && Array.isArray(answer.citations) && answer.citations.length === 3
  && answer.citations.every(value => typeof value === 'string') && typeof answer.actionAuthority === 'boolean'
const openWork = typeof answer?.openWork === 'string' ? answer.openWork.toLowerCase() : ''
const governingDecision = typeof answer?.governingDecision === 'string' ? answer.governingDecision.toLowerCase() : ''
const avoidRepeating = typeof answer?.avoidRepeating === 'string' ? answer.avoidRepeating.toLowerCase() : ''
const citations = Array.isArray(answer?.citations) && answer.citations.every(value => typeof value === 'string') ? [...answer.citations].sort() : []
const requiredCitations = [...fixture.requiredCitations].sort()
const criteria = {
  exactSchema: Boolean(exactTypes),
  openWork: ['indexed', 'paginated', 'memory explorer'].every(term => openWork.includes(term)),
  governingDecision: governingDecision.includes('cortex') && governingDecision.includes('inference')
    && (governingDecision.includes('acts') || governingDecision.includes('operating system')),
  avoidRepeating: avoidRepeating.includes('unbounded') && avoidRepeating.includes('scan'),
  citations: citations.join('|') === requiredCitations.join('|'),
  noActionAuthority: answer?.actionAuthority === false,
}
const passed = Object.values(criteria).every(Boolean)
emit({ schemaVersion: 'adi.paper6.model-consumption-score.v2', disposition: passed ? 'PASS' : 'FAIL', logicalPromptSha256, rawResponseSha256, criteria }, passed ? 0 : 1)
