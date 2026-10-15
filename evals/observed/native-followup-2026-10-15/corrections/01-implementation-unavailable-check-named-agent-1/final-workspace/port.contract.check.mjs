import assert from 'node:assert/strict';
import { port } from './port.ts';
for (const [value, expected] of [[1, 1], [65535, 65535], ['1', 1], ['00042', 42], ['65535', 65535]]) {
  assert.equal(port(value), expected);
}
for (const value of [true, false, null, undefined, '', ' ', '1.2', '+1', '-1', '1e2', '0x10', '１２', '1\n', NaN, Infinity, -Infinity, 0, -1, 65536, 1.5, '0', '65536', [], {}, 1n, Object.create(null), {toString() {throw new Error('conversion hook');}}, {[Symbol.toPrimitive]() {throw new Error('conversion hook');}}, Symbol('invalid')]) {
  assert.throws(() => port(value), TypeError);
}
console.log('34 local port-contract cases passed; required compiler remains separate.');
