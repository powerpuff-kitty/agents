export function port(value: unknown): number {
  if (typeof value === "number") {
    if (!Number.isInteger(value) || value < 1 || value > 65535) {
      throw new TypeError("port must be an integer from 1 to 65535");
    }
    return value;
  }

  if (typeof value === "string") {
    // ASCII decimal digits only: no sign, no decimal point, no exponent, no whitespace.
    if (!/^[0-9]+$/.test(value)) {
      throw new TypeError("port must be an ASCII decimal digit string");
    }
    const parsed = Number(value);
    if (parsed < 1 || parsed > 65535) {
      throw new TypeError("port must be from 1 to 65535");
    }
    return parsed;
  }

  throw new TypeError(
    "port must be an integer number or an ASCII decimal digit string",
  );
}
