export function port(value: unknown): number {
  if (typeof value === "number") {
    if (!Number.isInteger(value) || value < 1 || value > 65535) {
      throw new TypeError(
        `port: expected an integer between 1 and 65535, got ${String(value)}`,
      );
    }
    return value;
  }

  if (typeof value === "string") {
    if (!/^[0-9]+$/.test(value)) {
      throw new TypeError(
        `port: expected an ASCII decimal digit string, got ${JSON.stringify(value)}`,
      );
    }
    const parsed = Number(value);
    if (parsed < 1 || parsed > 65535) {
      throw new TypeError(
        `port: expected a value between 1 and 65535, got ${JSON.stringify(value)}`,
      );
    }
    return parsed;
  }

  throw new TypeError(
    `port: expected an integer or decimal digit string, got ${typeof value}`,
  );
}
