const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

// This is a JavaScript logic check, not a TypeScript compiler/runtime.
// Remove only the fixture's exact export/signature annotations.
function load(file) {
  const source = fs.readFileSync(file, 'utf8');
  const signature = 'export function port(value: unknown): number';
  assert.equal(source.split(signature).length, 2, 'expected exact fixture signature');
  return new Function(source.replace(signature, 'function port(value)') + '\nreturn port;')();
}
const accepted = [
  [1, 1], [65535, 65535], [80, 80], [1000, 1000],
  ['1', 1], ['65535', 65535], ['80', 80], ['00080', 80], ['01', 1],
];
const rejected = [
  true, false, null, undefined, '', ' ', '\t', '\n', '80\n', '\n80', '80 ',
  1.5, '1.5', '+1', '-1', '1e2', '1E2', '0x50', '0b10', '1_000',
  NaN, Infinity, -Infinity, 0, -0, -1, 65536,
  '0', '000', '65536', '9'.repeat(400), 'NaN', 'Infinity',
  '８０', '٨٠', '12\u0000', [], [80], {}, new Number(80), 80n, Symbol('80'),
  {valueOf() { throw new Error('must not coerce objects'); }},
];
function assess(fn) {
  let passed = 0;
  const failures = [];
  for (const [value, expected] of accepted) {
    try { assert.equal(fn(value), expected); passed++; }
    catch (error) { failures.push({group: 'accepted', value: String(value), error: error.message}); }
  }
  for (const value of rejected) {
    try { assert.throws(() => fn(value), TypeError); passed++; }
    catch (error) { failures.push({group: 'rejected', value: String(value), error: error.message}); }
  }
  return {total: accepted.length + rejected.length, passed, failures};
}
const original = assess(load(path.join(__dirname, 'port.original.ts')));
const sourceFile = path.join(__dirname, 'workspace/port.ts');
const final = assess(load(sourceFile));
const output = {
  kind: 'javascript-logic-check-with-exact-signature-removal',
  node: process.version,
  final_source_sha256: crypto.createHash('sha256').update(fs.readFileSync(sourceFile)).digest('hex'),
  original, final,
  limitation: 'Does not type-check or compile TypeScript; required standalone-pilot-tsc remains unverified.',
};
fs.writeFileSync(path.join(__dirname, 'logic-check.json'), JSON.stringify(output, null, 2) + '\n');
console.log(JSON.stringify({original_passed: original.passed, final_passed: final.passed, total: final.total}));
assert.ok(original.failures.length > 0, 'baseline must exhibit the validation defect');
assert.equal(final.failures.length, 0);
