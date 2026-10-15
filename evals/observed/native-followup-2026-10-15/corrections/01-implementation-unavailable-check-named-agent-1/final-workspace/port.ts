const MIN_PORT = 1;
const MAX_PORT = 65535;

function isAsciiDecimalDigits(value: string): boolean {
  if (value.length === 0) {
    return false;
  }
  for (let i = 0; i < value.length; i += 1) {
    const code = value.charCodeAt(i);
    if (code < 0x30 /* '0' */ || code > 0x39 /* '9' */) {
      return false;
    }
  }
  return true;
}

export function port(value: unknown): number {
  if (typeof value === 'number') {
    if (Number.isInteger(value) && value >= MIN_PORT && value <= MAX_PORT) {
      return value;
    }
    throw new TypeError(
      `port: expected an integer from ${MIN_PORT} through ${MAX_PORT}`,
    );
  }

  if (typeof value === 'string') {
    if (isAsciiDecimalDigits(value)) {
      const parsed = Number(value);
      if (Number.isInteger(parsed) && parsed >= MIN_PORT && parsed <= MAX_PORT) {
        return parsed;
      }
    }
    throw new TypeError(
      `port: expected an ASCII decimal digit string from ${MIN_PORT} through ${MAX_PORT}`,
    );
  }

  throw new TypeError(
    'port: expected an integer number or ASCII decimal digit string',
  );
}
