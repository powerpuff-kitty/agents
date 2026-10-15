export function port(value: unknown): number {
  if (typeof value === "number") {
    if (!Number.isInteger(value) || value < 1 || value > 65535) {
      throw new TypeError("port must be an integer between 1 and 65535");
    }
    return value;
  }

  if (typeof value === "string") {
    if (value.length === 0 || !isAsciiDecimalDigits(value)) {
      throw new TypeError(
        "port string must be non-empty ASCII decimal digits",
      );
    }
    const n = Number(value);
    if (n < 1 || n > 65535) {
      throw new TypeError("port must be between 1 and 65535");
    }
    return n;
  }

  throw new TypeError(
    "port must be an integer number or an ASCII decimal digit string",
  );
}

function isAsciiDecimalDigits(value: string): boolean {
  for (let i = 0; i < value.length; i++) {
    const c = value.charCodeAt(i);
    if (c < 48 || c > 57) {
      return false;
    }
  }
  return true;
}
