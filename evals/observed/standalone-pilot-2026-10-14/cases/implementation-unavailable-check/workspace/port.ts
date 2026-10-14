export function port(value: unknown): number {
  if (typeof value === "string") {
    if (value.length === 0 || /[^0-9]/.test(value)) {
      throw new TypeError("Invalid port");
    }
  } else if (typeof value !== "number") {
    throw new TypeError("Invalid port");
  }

  const result = Number(value);
  if (!Number.isInteger(result) || result < 1 || result > 65535) {
    throw new TypeError("Invalid port");
  }
  return result;
}
