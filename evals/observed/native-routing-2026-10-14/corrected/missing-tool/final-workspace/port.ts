const MIN_PORT = 1;
const MAX_PORT = 65535;

// A non-empty run of ASCII decimal digits only (no sign, no decimal point,
// no exponent, no whitespace).
const ASCII_DECIMAL_DIGITS = /^[0-9]+$/;

/**
 * Validates and normalizes a TCP/UDP port value.
 *
 * Accepts:
 *   - an integer number in the inclusive range [1, 65535], or
 *   - an ASCII decimal digit string representing a value in [1, 65535].
 *
 * Rejects (throws TypeError): booleans, null/undefined, empty or whitespace
 * strings, fractional strings, signed or exponent-form strings, NaN/Infinity,
 * and out-of-range values.
 */
export function port(value: unknown): number {
  if (typeof value === "number") {
    if (!Number.isInteger(value) || value < MIN_PORT || value > MAX_PORT) {
      throw new TypeError(
        `port must be an integer between ${MIN_PORT} and ${MAX_PORT} inclusive`,
      );
    }
    return value;
  }

  if (typeof value === "string") {
    if (!ASCII_DECIMAL_DIGITS.test(value)) {
      throw new TypeError(
        `port must be an ASCII decimal digit string between ${MIN_PORT} and ${MAX_PORT} inclusive`,
      );
    }
    const parsed = Number(value);
    if (parsed < MIN_PORT || parsed > MAX_PORT) {
      throw new TypeError(
        `port must be an integer between ${MIN_PORT} and ${MAX_PORT} inclusive`,
      );
    }
    return parsed;
  }

  throw new TypeError(
    `port must be an integer or an ASCII decimal digit string between ${MIN_PORT} and ${MAX_PORT} inclusive`,
  );
}
