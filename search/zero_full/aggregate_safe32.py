from pathlib import Path
import gzip,hashlib,json,re
here=Path(__file__).parent
validation=json.loads((here/'safe32_validation_results.json').read_text())
shards=[];candidate_records=0;candidate_cases=set()
for part in range(2):
    log=(here/f'safe32_part{part}_stats.log').read_text()
    done=[line for line in log.splitlines() if line.startswith('DONE SAFE32 ')]
    assert len(done)==1,f'shard{part} has not completed'
    values={k:float(v) if '.' in v else int(v) for k,v in re.findall(r'(\w+)=([0-9.]+)',done[0])}
    expected=validation['partition_counts'][part]
    assert values['partition']==part and values['partitions']==2
    for field in ['keys','numeric_key_sum','ordinal_sum']:assert values[field]==expected[field],(part,field)
    assert values['cases']==values['keys']*16*19*2
    zeros={str(z):int(count) for p,z,count in re.findall(r'SAFE32_ZERO_POSITION partition=(\d+) zero=(\d+) keys=(\d+)',log) if int(p)==part}
    assert zeros==expected['zero_counts']
    incomplete=[line for line in log.splitlines() if line.startswith('INCOMPLETE ')]
    assert len(incomplete)==values['capped']+values['long_erasure']
    stream_records=0
    with gzip.open(here/f'safe32_part{part}_candidates.txt.gz','rt') as stream:
        for line in stream:
            if not line.startswith('CANDIDATE '):raise AssertionError(line[:80])
            record=dict(field.split('=',1) for field in line.split()[1:])
            assert record['language']=='1'
            stream_records+=1
            candidate_cases.add((record['label'],record['alg'],record['iv']))
    assert stream_records==values['candidates']
    candidate_records+=stream_records
    shards.append({**values,'zero_position_key_counts':zeros,'incomplete_case_records':len(incomplete)})
totals={field:sum(row[field] for row in shards) for field in ['keys','cases','rejected_known','nodes','candidates','capped','long_erasure','numeric_key_sum','ordinal_sum']}
assert totals['keys']==416400 and totals['cases']==253171200
out={
 'rev7_solved':False,
 'search_complete':True,
 'conditional_negative':candidate_records==0 and totals['capped']==0 and totals['long_erasure']==0,
 'scope':'All signed32-safe nonleading-zero permutations of0..9; historical AMSCO encode erasure only; Zombies key;19CFB8 primitives; IV0/48;16input/output orientations; ASCII plus recorded UTF8 typography language',
 'totals':totals,
 'candidate_records_preserved':candidate_records,
 'distinct_candidate_cases':len(candidate_cases),
 'shards':shards,
 'parallel_wall_seconds_approx':max(row['seconds'] for row in shards),
 'summed_worker_seconds':sum(row['seconds'] for row in shards),
 'unsearched_nonleading_zero_keys_above_signed32_limit':3265920-416400,
 'controls':{'partition_and_planted':validation,'actual_original_PHP':json.loads((here/'safe32_php_controls.json').read_text())},
 'source_hashes':{str(p.relative_to(here.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [here/'benchmark.cpp',here.parent/'continuation_zero_column/recovery_support.inc',here.parent/'cipher.txt']},
 'limitations':['This does not establish that Rev7 used the malformed key or this cipher family.','The language is a specific subset of UTF8, not all text encodings or binary data.','Keys outside signed32 range, other inner keys/modes, data errors, and decode-as-forward erasure models are not covered by this pass.']
}
(here/'SAFE32_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'totals':totals,'parallel_wall_seconds_approx':out['parallel_wall_seconds_approx'],'conditional_negative':out['conditional_negative']},indent=2))
