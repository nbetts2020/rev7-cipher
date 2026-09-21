from pathlib import Path
import sys,json,random,subprocess,hashlib
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'continuation_numeric_amsco'),str(root/'continuation_zero_column')]
from zero_projection import scatter
from work import ori
here=Path(__file__).parent
binary=str(here/'benchmark')
rng=random.Random(649120)
records=json.loads((root/'continuation_zero_column/controls_manifest.json').read_text())
projection_cases=[]
for r in records:
    projection_cases.append((r['key'],r['outer'],r['inner'],r['display'],r['pattern']))
for _ in range(160):
    digits=list('0123456789');rng.shuffle(digits)
    if digits[0]=='0':digits[0],digits[1]=digits[1],digits[0]
    key=''.join(digits);n=1170 if key.index('0')%2 else 1260
    display=''.join(rng.choice('0123456789ABCDEF') for _ in range(1092))
    for outer in range(4):
        for inner in range(4):
            expected=ori(scatter(ori(display,outer),key,n),inner)
            projection_cases.append((key,outer,inner,display,expected))
payload=''.join(f'{key} {outer} {inner} {display}\n' for key,outer,inner,display,_ in projection_cases)
run=subprocess.run([binary,'project'],input=payload,text=True,capture_output=True,cwd=root,check=True)
outputs=run.stdout.splitlines()
assert len(outputs)==len(projection_cases)
for case,actual in zip(projection_cases,outputs):assert actual==case[-1],case[:3]
control_payload=''.join(' '.join([r['label'],r['key'],str(r['outer']),str(r['inner']),r['display'],r['alg'],str(r['iv']),r['cipher'],r['plain']])+'\n' for r in records)
(here/'control_inputs.txt').write_text(control_payload)
with open(here/'control_inputs.txt') as source,open(here/'controls.log','w') as log:
    subprocess.run([binary,'controls'],stdin=source,stdout=log,stderr=log,cwd=root,check=True)
log=(here/'controls.log').read_text();assert 'CONTROLS DONE cases=152' in log
result={'projection_comparisons':len(projection_cases),'planted_controls':len(records),'control_language':1,'original_and_optimized_completion_streams_identical':True,'original_source_PHP_forward_controls':152,'source_php_forward_evidence':'../continuation_zero_column/php_planted_results.json','projection_algorithms':'closed-form C++ scatter vs independently PHP-validated Python index projection','original_recovery_support_sha256':hashlib.sha256((root/'continuation_zero_column/recovery_support.inc').read_bytes()).hexdigest()}
(here/'validation_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));print(log.splitlines()[-1])
