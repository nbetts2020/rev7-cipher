import fs from 'node:fs';
import crypto from 'node:crypto';
import { PHP, loadPHPRuntime } from '@php-wasm/universal';
import { getPHPLoaderModule } from '@php-wasm/node-8-4';

/** Execute actual original source. Cases: {id,mode:'encode'|'decode',text,key}.
 * Returns {php_version,php_int_size,source_sha256,warning_counts,
 * warning_examples,results:[{id,key_after_integer_cast,grouped,compact}]}.
 * No filesystem mounts, network setup, expected outputs, or source edits.
 */
export async function executeAmscoCases(cases) {
  for (const c of cases) if (!['encode','decode'].includes(c.mode)) throw Error('Invalid method');
  const source=fs.readFileSync(new URL('../continuation_historical_tools/_ctoLegacy__tools__amsco__class.amsco.php',import.meta.url));
  const php=new PHP(await loadPHPRuntime(await getPHPLoaderModule()));
  php.writeFile('/class.amsco.php',source);
  php.writeFile('/cases.json',JSON.stringify(cases.map(({id,mode,text,key})=>({id,mode,text,key:String(key)}))));
  php.writeFile('/verify.php',`<?php
define('_JEXEC',true);
class JURI { public static function base($relative=false) { return ''; } }
$CTOPluginName='verification';
$warning_counts=[];
$warning_examples=[];
set_error_handler(function($severity,$message,$file,$line) use (&$warning_counts,&$warning_examples) {
    $signature=$severity.':'.$message;
    $warning_counts[$signature]=($warning_counts[$signature]??0)+1;
    if(count($warning_examples)<15) $warning_examples[]=['severity'=>$severity,'message'=>$message,'line'=>$line];
    return true;
});
require '/class.amsco.php';
$cases=json_decode(file_get_contents('/cases.json'),true);
$results=[];
foreach($cases as $case) {
    $coder=new amsco_cipher();
    $key=$case['key'];
    if(is_numeric($key)) $key=(int)$key;
    $coder->setKey($key);
    $coder->setText($case['text']);
    $coder->{$case['mode']}();
    $grouped=$coder->getText();
    $results[]=['id'=>$case['id'],'key_after_integer_cast'=>(string)$key,'grouped'=>$grouped,'compact'=>str_replace(' ','',$grouped)];
}
echo json_encode(['php_version'=>PHP_VERSION,'php_int_size'=>PHP_INT_SIZE,'source_sha256'=>hash_file('sha256','/class.amsco.php'),'warning_counts'=>$warning_counts,'warning_examples'=>$warning_examples,'results'=>$results]);
`);
  try {
    const response=await php.run({scriptPath:'/verify.php'});
    if(response.exitCode!==0)throw Error(`PHP exit ${response.exitCode}: ${response.errors}`);
    const actual=JSON.parse(response.text);
    if(actual.source_sha256!==crypto.createHash('sha256').update(source).digest('hex'))throw Error('Source bytes changed');
    if(actual.results.length!==cases.length)throw Error('Case count mismatch');
    return actual;
  } finally { php.exit(); }
}
