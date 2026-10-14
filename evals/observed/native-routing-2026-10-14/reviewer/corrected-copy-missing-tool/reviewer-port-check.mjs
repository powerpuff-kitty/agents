import assert from "node:assert/strict";
import { port } from "./port.ts";
const accepted = [[1,1],[65535,65535],[443,443],["1",1],["65535",65535],["443",443],["00001",1],["0".repeat(400)+"443",443]];
const rejected = [true,false,null,undefined,""," ","\t","1\n","1\r","1\r\n","1\u2028","1\u2029"," 1","1 ","1.5","-1","+1","1e3","1E3","0x10","１","١","0","65536",0,-0,-1,65536,1.5,NaN,Infinity,-Infinity,{},[],[1],1n,Symbol("1"),"9".repeat(400)];
let checks=0;for (const [value,expected] of accepted){assert.equal(port(value),expected);checks++;}for(const value of rejected){assert.throws(()=>port(value),TypeError);checks++;}console.log(JSON.stringify({accepted:accepted.length,rejected:rejected.length,checks,passed:true}));
