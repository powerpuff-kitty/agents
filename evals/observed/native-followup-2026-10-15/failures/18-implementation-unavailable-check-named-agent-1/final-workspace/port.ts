const MIN_PORT = 1;
const MAX_PORT = 65535;
const ASCII_DECIMAL_DIGITS = /^[0-9]+$/;

function reject(value: unknown): never {
  throw new TypeError(
    `port(): expected an integer 1-65535 or an ASCII decimal digit string, received ${String(value)}`,
  );
}

export function port(value: unknown): number {
  if (typeof value === 'number') {
    if (!Number.isInteger(value)) {
      reject(value);
    }
    if (value < MIN_PORT || value > MAX_PORT) {
      reject(value);
    }
    return value;
  }

  if (typeof value === 'string') {
    if (!ASCII_DECIMAL_DIGITS.test(value)) {
      reject(value);
    }
    const parsed = Number(value);
    if (parsed < MIN_PORT || parsed > MAX_PORT) {
      reject(value);
    }
    return parsed;
  }

  reject(value);
}
