const MIN_PORT = 1;
const MAX_PORT = 65535;

export function port(value: unknown): number {
  if (typeof value === "number") {
    if (!Number.isInteger(value) || value < MIN_PORT || value > MAX_PORT) {
      throw new TypeError(
        `port must be an integer between ${MIN_PORT} and ${MAX_PORT}`,
      );
    }
    return value;
  }

  if (typeof value === "string") {
    // Accept only ASCII decimal digit strings: no sign, decimal point,
    // exponent marker, or surrounding/interior whitespace.
    if (!/^[0-9]+$/.test(value)) {
      throw new TypeError("port must be an ASCII decimal digit string");
    }
    const n = Number(value);
    if (n < MIN_PORT || n > MAX_PORT) {
      throw new TypeError(
        `port must be an integer between ${MIN_PORT} and ${MAX_PORT}`,
      );
    }
    return n;
  }

  throw new TypeError("port must be an integer number or a decimal digit string");
}
