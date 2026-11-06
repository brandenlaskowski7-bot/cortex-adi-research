import { createHash } from 'node:crypto'
import { readFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const fixturePath = resolve(here, 'model-consumption-fixture.json')
const responsePath = process.argv[2]

if (!responsePath) {
  process.stderr.write('Usage: node score-model-response.mjs <response.json>\n')
  process.exit(2)
}

let fixture
let answer
try {
  fixture = JSON.parse(await readFile(fixturePath, 'utf8'))
  answer = JSON.parse(await readFile(resolve(responsePath), 'utf8'))
} catch (error) {
  process.stdout.write(`${JSON.stringify({ disposition: 'INFRASTRUCTURE_FAIL', error: String(error) }, null, 2)}\n`)
  process.exit(2)
}

const logicalPrompt = [...fixture.instructionLines, JSON.stringify(fixture.evidence)].join('\n')
const logicalPromptSha256 = createHash('sha256').update(logicalPrompt).digest('hex')
if (logicalPromptSha256 !== fixture.logicalPromptSha256) {
  process.stdout.write(`${JSON.stringify({ disposition: 'INFRASTRUCTURE_FAIL', error: 'fixture_prompt_hash_mismatch', logicalPromptSha256 }, null, 2)}\n`)
  process.exit(2)
}

const exactKeys = answer && typeof answer === 'object' && !Array.isArray(answer)
  && Object.keys(answer).sort().join('|') === [...fixture.requiredKeys].sort().join('|')
const exactTypes = exactKeys
  && typeof answer.openWork === 'string'
  && typeof answer.governingDecision === 'string'
  && typeof answer.avoidRepeating === 'string'
  && Array.isArray(answer.citations)
  && answer.citations.length === 3
  && answer.citations.every(value => typeof value === 'string')
  && typeof answer.actionAuthority === 'boolean'

const openWork = typeof answer?.openWork === 'string' ? answer.openWork.toLowerCase() : ''
const governingDecision = typeof answer?.governingDecision === 'string' ? answer.governingDecision.toLowerCase() : ''
const avoidRepeating = typeof answer?.avoidRepeating === 'string' ? answer.avoidRepeating.toLowerCase() : ''
const citations = Array.isArray(answer?.citations) && answer.citations.every(value => typeof value === 'string')
  ? [...answer.citations].sort()
  : []
const requiredCitations = [...fixture.requiredCitations].sort()

const criteria = {
  exactSchema: Boolean(exactTypes),
  openWork: ['indexed', 'paginated', 'memory explorer'].every(term => openWork.includes(term)),
  governingDecision: governingDecision.includes('cortex')
    && governingDecision.includes('inference')
    && (governingDecision.includes('acts') || governingDecision.includes('operating system')),
  avoidRepeating: avoidRepeating.includes('unbounded') && avoidRepeating.includes('scan'),
  citations: citations.join('|') === requiredCitations.join('|'),
  noActionAuthority: answer?.actionAuthority === false,
}
const passed = Object.values(criteria).every(Boolean)
const rawResponse = await readFile(resolve(responsePath), 'utf8')
const result = {
  schemaVersion: 'adi.paper5.model-consumption-score.v1',
  disposition: passed ? 'PASS' : 'FAIL',
  logicalPromptSha256,
  rawResponseSha256: createHash('sha256').update(rawResponse).digest('hex'),
  criteria,
}
process.stdout.write(`${JSON.stringify(result, null, 2)}\n`)
process.exit(passed ? 0 : 1)
