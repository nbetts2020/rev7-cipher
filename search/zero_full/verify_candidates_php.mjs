import fs from 'node:fs';
import { executeAmscoCases } from '../continuation_php_runtime/original_amsco.mjs';
const here=new URL('./',import.meta.url);
const records=JSON.parse(fs.readFileSync(new URL('candidates_decoded.json',here),'utf8'));
const observed=fs.readFileSync(new URL('../cipher.txt',here),'utf8').replace(/\s+/g,'');
const cases=records.map((r,id)=>{
  if(r.label!=='zeroencode/key=1947038265/outer=1/inner=0')throw Error('Unexpected pipeline');
  return{id,mode:'encode',key:'1947038265',text:r.cipher};
});
const actual=await executeAmscoCases(cases);
for(const r of actual.results)if([...r.compact].reverse().join('')!==observed)throw Error(`Original PHP mismatch${r.id}`);
const result={cases:cases.length,original_PHP_exact_observed_ciphertext_matches:actual.results.length,php_version:actual.php_version,source_sha256:actual.source_sha256,original_hex_characters:records[0].cipher.length,observed_hex_characters:observed.length,omitted_hex_characters:records[0].cipher.length-observed.length,key:'1947038265',operation:'Original PHP AMSCO encode, remove grouping spaces, reverse all hex characters'};
fs.writeFileSync(new URL('candidate_php_validation.json',here),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
