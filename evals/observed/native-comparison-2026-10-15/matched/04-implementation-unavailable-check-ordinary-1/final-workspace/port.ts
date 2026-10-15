export function port(value: unknown): number {
  let n: number;

  if (typeof value === "number") {
    n = value;
  } else if (typeof value === "string" && /^[0-9]+$/.test(value)) {
    n = Number(value);
  } else {
    throw new TypeError("port: expected an integer or ASCII decimal digit string");
  }

  if (!Number.isInteger(n) || n < 1 || n > 65535) {
    throw new TypeError("port: expected an integer from 1 through 65535");
  }

  return n;
}
