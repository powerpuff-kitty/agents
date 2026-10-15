function isAsciiDecimalDigits(value: string): boolean {
  for (let i = 0; i < value.length; i++) {
    const code = value.charCodeAt(i);
    if (code < 0x30 || code > 0x39) {
      return false;
    }
  }
  return true;
}

export function port(value: unknown): number {
  if (typeof value === 'number') {
    if (Number.isInteger(value) && value >= 1 && value <= 65535) {
      return value;
    }
    throw new TypeError(
      'port: expected an integer or ASCII decimal string in 1..65535',
    );
  }

  if (typeof value === 'string') {
    if (value.length > 0 && isAsciiDecimalDigits(value)) {
      const parsed = Number(value);
      if (parsed >= 1 && parsed <= 65535) {
        return parsed;
      }
    }
    throw new TypeError(
      'port: expected an integer or ASCII decimal string in 1..65535',
    );
  }

  throw new TypeError(
    'port: expected an integer or ASCII decimal string in 1..65535',
  );
}
