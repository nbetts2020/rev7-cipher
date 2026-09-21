"""Recover the 64 completions for the discovered pipeline, without a plaintext crib.

Run from any working directory:
    python3 -B /path/to/rev7-cipher/search/zero_full/targeted_reproduce.py

Requires the native recovery binary; build it first (see lib/BUILD.md):
    clang++ -O3 -std=c++17 -I mcrypt/include search/zero_column/recover.cpp \
        -L mcrypt/lib -lmcrypt -o search/zero_column/recover

The original recovery executable tries its19algorithms,2IVs,2languages on one
masked input. Candidate18 is selected only AFTER enumeration, as the coherent
reading identified by inspection. This semantic choice is not a uniqueness proof.
"""
from pathlib import Path
import gzip,hashlib,json,subprocess,sys
here=Path(__file__).resolve().parent;root=here.parents[1]
sys.path.insert(0,str(root/'lib'))
from zero_projection import scatter
observed=''.join((root/'cipher.txt').read_text().split())
assert hashlib.sha256(observed.encode()).hexdigest()=='5c50001013a2dd862e13c38d314a0ba6d7303794287a05cc999018cf82cf4b1c'
pattern=scatter(observed[::-1],'1947038265',1260)
(here/'targeted_input.tsv').write_text('discovered1947038265\t'+pattern+'\n')
with open(here/'targeted_original_recover.log','w') as log:
    result=subprocess.run([str(root/'search/zero_column/recover')],input='discovered1947038265\t'+pattern+'\n',stdout=subprocess.PIPE,stderr=log,text=True,cwd=root,check=True)
records=[]
for line in result.stdout.splitlines():
    if not line.startswith('CANDIDATE '):raise AssertionError(line)
    record=dict(field.split('=',1) for field in line.split()[1:])
    record['text']=bytes.fromhex(record['plain']).decode('utf-8');records.append(record)
assert len(records)==64
assert {(r['alg'],r['iv'],r['language']) for r in records}=={('blowfish-compat','48','1')}
with gzip.open(here/'targeted_all64_candidates.txt.gz','wt') as out:out.write(result.stdout)
prior=json.loads((here/'candidates_decoded.json').read_text())
assert [(r['cipher'],r['plain'])for r in records]==[(r['cipher'],r['plain'])for r in prior]
selected_index=18  # Explicit post-search semantic selection, not a solver constraint.
selected=records[selected_index]
(here/'targeted_selected_plaintext_utf8.txt').write_bytes(bytes.fromhex(selected['plain']))
summary={'candidates':len(records),'matches_original_broad_search':True,'plaintext_crib_supplied_to_search':False,'selected_candidate_index_zero_based':selected_index,'selection_basis':'Post-search reading: candidate18 has coherent prose in all four erasure-affected regions.','mathematically_unique':False,'key':'1947038265','algorithm':'blowfish-compat','mode':'CFB8','inner_key':'Zombies','IV_hex':'3030303030303030','outer_operation':'Historical AMSCO encode followed by full hex-character reversal','original_hex_characters':1260,'observed_hex_characters':1092,'omitted_hex_characters':168}
(here/'targeted_results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2));print(selected['text'])
