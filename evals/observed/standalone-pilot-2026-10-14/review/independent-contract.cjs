const fs=require('node:fs');
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const source=fs.readFileSync('implementation-copy/workspace/port.ts','utf8');
const signature='export function port(value: unknown): number';
assert.equal(source.split(signature).length,2);
const port=new Function(source.replace(signature,'function port(value)')+'\nreturn port;')();
let accepted=0,rejected=0;
for(let n=1;n<=65535;n++) {
 for(const input of [n,String(n),'000'+n]) {assert.equal(port(input),n);accepted++;}
}
for(const x of [-1,0,65536,1.01,Number.MIN_VALUE,Number.MAX_VALUE,NaN,Infinity,-Infinity,true,false,null,undefined,[],{},new String('1'),Object(1),1n,Symbol('1')]) {assert.throws(()=>port(x),TypeError);rejected++;}
for(let code=0;code<=65535;code++) {
 if(code>=48 && code<=57)continue;
 for(const input of [String.fromCharCode(code)+'80','80'+String.fromCharCode(code)]) {assert.throws(()=>port(input),TypeError);rejected++;}
}
for(const s of ['', '0','00000','65536','9999999999999999999999999999999999','+80','-80','8e1','0x50','80.0']){assert.throws(()=>port(s),TypeError);rejected++;}
let coerced=false;
assert.throws(()=>port({valueOf(){coerced=true;return 80;},toString(){coerced=true;return '80';}}),TypeError);rejected++;
assert.equal(coerced,false);
const result={kind:'independent-JavaScript-logic-check-after-exact-signature-removal',node:process.version,accepted,rejected,total:accepted+rejected,failures:0,source_sha256:crypto.createHash('sha256').update(source).digest('hex'),limitations:'No TypeScript parsing, type-checking or compilation. Finite contract coverage; no browser/integration claim.'};
fs.writeFileSync('independent-contract.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
