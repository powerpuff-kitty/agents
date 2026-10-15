const MIN_PORT = 1;
const MAX_PORT = 65535;
const ASCII_DIGITS = /^[0-9]+$/;

export function port(value: unknown): number {
  if (typeof value === "number") {
    if (Number.isInteger(value) && value >= MIN_PORT && value <= MAX_PORT) {
      return value;
    }
    throw new TypeError(`port: expected an integer 1..65535, got ${value}`);
  }

  if (typeof value === "string") {
    if (ASCII_DIGITS.test(value)) {
      const parsed = Number(value);
      if (parsed >= MIN_PORT && parsed <= MAX_PORT) {
        return parsed;
      }
    }
    throw new TypeError(`port: expected an ASCII decimal digit string for 1..65535, got ${JSON.stringify(value)}`);
  }

  throw new TypeError(`port: expected a number or string, got ${typeof value}`);
}
