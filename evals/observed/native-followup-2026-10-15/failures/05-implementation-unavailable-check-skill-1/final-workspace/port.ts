export function port(value: unknown): number {
  if (typeof value === 'number') {
    if (!Number.isInteger(value) || value < 1 || value > 65535) {
      throw new TypeError(`port: expected an integer 1..65535, received ${value}`);
    }
    return value;
  }

  if (typeof value === 'string') {
    // ASCII decimal digits only (no sign, fraction, exponent, hex, whitespace, or
    // fullwidth digits), and must represent a value in [1, 65535]. Leading zeros
    // are allowed ('00042' -> 42), but '0' / '00' map to 0 and are rejected.
    if (!/^[0-9]+$/.test(value)) {
      throw new TypeError(`port: expected an ASCII decimal digit string, received ${JSON.stringify(value)}`);
    }
    const n = Number(value);
    if (!Number.isInteger(n) || n < 1 || n > 65535) {
      throw new TypeError(`port: value out of range, received ${JSON.stringify(value)}`);
    }
    return n;
  }

  throw new TypeError(`port: expected an integer or decimal digit string, received ${typeof value}`);
}
