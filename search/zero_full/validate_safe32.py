from pathlib import Path
from itertools import permutations
import json,re,sys,subprocess
root=Path(__file__).resolve().parents[1];here=Path(__file__).parent
sys.path[:0]=[str(root/'continuation_zero_column'),str(root/'continuation_historical_tools')]
from work import ori
from literal_models import amsco_encode
totals=[{'keys':0,'numeric_key_sum':0,'ordinal_sum':0,'zero_counts':{str(i):0 for i in range(1,10)}} for _ in range(2)]
ordinal=0;members={};wanted=['1023456789','1203456789','1234567890','1234567908','1357924680']
for digits in permutations('0123456789'):
    if digits[0]=='0':continue
    key=''.join(digits)
    if int(key)>2147483647:break
    part=ordinal%2;row=totals[part];row['keys']+=1;row['numeric_key_sum']+=int(key);row['ordinal_sum']+=ordinal;row['zero_counts'][str(key.index('0'))]+=1
    if key in wanted:members[key]={'ordinal':ordinal,'partition':part}
    ordinal+=1
assert ordinal==416400 and {v['partition'] for v in members.values()}=={0,1}
log=(here/'shard_counts.log').read_text()
for part,keys,keysum,ord_sum in re.findall(r'SHARD partition=(\d+) partitions=2 keys=(\d+) numeric_key_sum=(\d+) ordinal_sum=(\d+)',log):
    row=totals[int(part)];assert [row['keys'],row['numeric_key_sum'],row['ordinal_sum']]==list(map(int,[keys,keysum,ord_sum]))
for part,zero,keys in re.findall(r'SHARD_ZERO partition=(\d+) zero=(\d+) keys=(\d+)',log):assert totals[int(part)]['zero_counts'][zero]==int(keys)
records=json.loads((root/'continuation_zero_column/controls_manifest.json').read_text());controls=[]
for i,key in enumerate(wanted):
    n=1170 if key.index('0')%2 else 1260
    available=[r for r in records if len(r['cipher'])==n];r=available[i*13%len(available)]
    inner=i%4;outer=(i//2)%4;text=ori(r['cipher'],inner);compact=amsco_encode(text,key);display=ori(compact,outer)
    controls.append({'label':f'safe_shard_control{i}','key':key,'outer':outer,'inner':inner,'display':display,'alg':r['alg'],'iv':r['iv'],'cipher':r['cipher'],'plain':r['plain'],'php_input':text,'php_output':compact,**members[key]})
payload=''.join(' '.join(str(r[k]) for k in ['label','key','outer','inner','display','alg','iv','cipher','plain'])+'\n' for r in controls)
(here/'safe32_control_inputs.txt').write_text(payload)
(here/'safe32_control_manifest.json').write_text(json.dumps(controls,indent=2)+'\n')
with open(here/'safe32_control_inputs.txt') as inp,open(here/'safe32_controls.log','w') as out:
    subprocess.run([str(here/'benchmark'),'controls'],cwd=root,stdin=inp,stdout=out,stderr=out,check=True)
assert 'CONTROLS DONE cases=5' in (here/'safe32_controls.log').read_text()
result={'independent_key_enumeration':'Python itertools.permutations vs C++ next_permutation','total_keys':ordinal,'partition_counts':totals,'planted_keys':members,'planted_recoveries':5,'both_partitions_exercised':True}
(here/'safe32_validation_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
