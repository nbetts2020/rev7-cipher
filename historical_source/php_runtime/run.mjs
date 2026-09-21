import fs from 'node:fs';
import crypto from 'node:crypto';
import { PHP, loadPHPRuntime } from '@php-wasm/universal';
import { getPHPLoaderModule } from '@php-wasm/node-8-4';

const source=fs.readFileSync('../continuation_historical_tools/_ctoLegacy__tools__amsco__class.amsco.php');
const cases=JSON.parse(fs.readFileSync('cases.json','utf8'));
const php=new PHP(await loadPHPRuntime(await getPHPLoaderModule()));
php.writeFile('/class.amsco.php',source);
php.writeFile('/cases.json',JSON.stringify(cases.map(({expected,...rest})=>rest)));
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
const response=await php.run({scriptPath:'/verify.php'});
if(response.errors)fs.writeFileSync('runtime_stderr.log',response.errors);
if(response.exitCode!==0)throw Error(`PHP exit ${response.exitCode}: ${response.errors}`);
fs.writeFileSync('actual_outputs.json',response.text+'\n');
const actual=JSON.parse(response.text);
const sourceHash=crypto.createHash('sha256').update(source).digest('hex');
if(sourceHash!==actual.source_sha256)throw Error('Original PHP bytes changed entering runtime');
const mismatches=[];
if(actual.results.length!==cases.length)throw Error('Case count mismatch');
for(const observed of actual.results){
    const expected=cases[observed.id];
    if(observed.compact!==expected.expected||observed.key_after_integer_cast!==expected.key)mismatches.push({expected,observed});
}
const summary={
    php_version:actual.php_version,php_int_size:actual.php_int_size,
    runtime_packages:{'@php-wasm/universal':'3.1.53','@php-wasm/node-8-4':'3.1.53'},
    source_sha256:sourceHash,source_bytes_preserved:true,
    cases:cases.length,mismatches:mismatches.length,
    category_counts:Object.fromEntries([...new Set(cases.map(c=>c.category))].map(category=>[category,cases.filter(c=>c.category===category).length])),
    warning_total:Object.values(actual.warning_counts).reduce((a,b)=>a+b,0),
    warning_examples:actual.warning_examples,
    fixture:actual.results[0],
};
fs.writeFileSync('RESULTS.json',JSON.stringify(summary,null,2)+'\n');
if(mismatches.length)fs.writeFileSync('mismatches.json',JSON.stringify(mismatches,null,2)+'\n');
console.log(JSON.stringify(summary,null,2));
if(mismatches.length)process.exitCode=1;
php.exit();
