import { port } from "./port.ts";

let failures = 0;
function check(label, fn) {
  try {
    fn();
    console.log(`ok   ${label}`);
  } catch (e) {
    failures += 1;
    console.log(`FAIL ${label}: ${e.message}`);
  }
}
function accepts(value, expected) {
  check(`accept ${JSON.stringify(value)} -> ${expected}`, () => {
    const got = port(value);
    if (got !== expected || typeof got !== "number") {
      throw new Error(`expected number ${expected}, got ${typeof got} ${got}`);
    }
  });
}
function rejects(value) {
  check(`reject ${JSON.stringify(value)}`, () => {
    try {
      port(value);
      throw new Error("did not throw");
    } catch (e) {
      if (!(e instanceof TypeError)) {
        throw new Error(`expected TypeError, got ${e.constructor.name}`);
      }
    }
  });
}

// Accepted integer numbers
accepts(1, 1);
accepts(80, 80);
accepts(65535, 65535);
accepts(1.0, 1);
accepts(1000, 1000);
accepts(1e2, 100); // exponent number literal is an integer, in range

// Accepted ASCII decimal digit strings
accepts("1", 1);
accepts("80", 80);
accepts("65535", 65535);
accepts("00080", 80);

// Rejected: booleans
rejects(true);
rejects(false);

// Rejected: null/undefined
rejects(null);
rejects(undefined);

// Rejected: empty/whitespace strings
rejects("");
rejects(" ");
rejects("\t");
rejects("\n");
rejects("  80");

// Rejected: fractional
rejects(1.5);
rejects("1.5");
rejects("1.0");
rejects("0.5");
rejects(".5");

// Rejected: signed strings
rejects("+1");
rejects("-1");
rejects("+80");

// Rejected: exponent-form strings
rejects("1e3");
rejects("1E3");
rejects("1.5e2");
rejects("8e0");

// Rejected: NaN/Infinity
rejects(NaN);
rejects(Infinity);
rejects(-Infinity);

// Rejected: out-of-range
rejects(0);
rejects(-1);
rejects(65536);
rejects("0");
rejects("65536");
rejects("999999999999999999999");

// Rejected: other types
rejects({});
rejects([]);
rejects(Symbol("p"));
rejects(() => {});
rejects(1n);

console.log(failures === 0 ? "ALL PASS" : `${failures} FAILURES`);
if (failures !== 0) process.exit(1);
