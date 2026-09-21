import fs from 'node:fs';
import { executeAmscoCases } from '../continuation_php_runtime/original_amsco.mjs';
const dir=new URL('./',import.meta.url);
const controls=JSON.parse(fs.readFileSync(new URL('safe32_control_manifest.json',dir),'utf8'));
const actual=await executeAmscoCases(controls.map((r,id)=>({id,mode:'encode',text:r.php_input,key:r.key})));
for(const r of actual.results)if(r.compact!==controls[r.id].php_output)throw Error('PHP forward mismatch');
const result={cases:controls.length,matches:actual.results.length,php_version:actual.php_version,source_sha256:actual.source_sha256,keys:controls.map(r=>r.key)};
fs.writeFileSync(new URL('safe32_php_controls.json',dir),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
