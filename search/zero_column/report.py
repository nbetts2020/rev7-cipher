from pathlib import Path
import json,re,gzip,hashlib
R=Path(__file__).resolve().parent;P=R.parent
summaries={}
for name,file in [('encode','encode_scan.log'),('decode_cfb','decode_cfb_scan.log')]:
 s=(R/file).read_text();line=next((x for x in s.splitlines()if x.startswith('DONE mode=scan ')),None)
 if line is None:raise RuntimeError(name+' incomplete')
 f=dict(x.split('=',1)for x in line.split()[1:]);assert f['candidates']=='0'and f['capped']=='0'and f['long_erasure']=='0'
 summaries[name]=f
cand_files=['encode_candidates.txt.gz','decode_cfb_candidates.txt.gz']
for f in cand_files:
 with gzip.open(R/f,'rt')as inp:assert not inp.read().strip()
s=(R/'decode_masked_modes.log').read_text();line=next(x for x in s.splitlines()if x.startswith('DONE masked_modes '));m=dict(x.split('=',1)for x in line.split()[2:]);assert m['candidates']=='0'and m['safe_regions']=='0'and int(m['maximum_safe_run'])<32;summaries['decode_modes']=m
controls=json.loads((R/'controls_results.json').read_text());assert controls['controls']==controls['exact_planted_cipher_and_plaintext_recoveries']==152
cs=(R/'controls.log').read_text();assert len(re.findall(' expected=1 capped=0',cs))==152
with gzip.open(R/'controls_candidates.jsonl.gz','rt')as inp:assert sum(1 for _ in inp)==controls['candidates_preserved']==66113
php=json.loads((R/'php_planted_results.json').read_text());php2=json.loads((R/'php_masked_results.json').read_text());assert php['cases']==php['exact_matches']==152 and php2['cases']==php2['exact_matches']==230 and php['source_sha256']==php2['source_sha256']
mc=json.loads((R/'masked_control_results.json').read_text());assert mc['complete_chains']==mc['exact_known_plaintext_regions']==230
manifest=json.loads((R/'input_manifest.json').read_text());assert len(manifest)==2160
keys={r['key']for r in manifest};assert len(keys)==45;assert sum(int(k)<=2147483647 for k in keys)==36
assert hashlib.sha256(''.join((P/'cipher.txt').read_text().split()).encode()).hexdigest()=='5c50001013a2dd862e13c38d314a0ba6d7303794287a05cc999018cf82cf4b1c'
summary={'keys':45,'portable_signed32_keys':36,'explicit_signed64_keys':9,'patterns':2160,'searches':summaries,'erasure_controls':controls,'masked_controls':mc,'original_PHP_planted_encode':php,'original_PHP_planted_decode':php2,'hashes':{}}
for p in[R/'recover.cpp',R/'work.py',R/'masked_modes.cpp',R/'input_manifest.json',R/'controls_candidates.jsonl.gz']:
 summary['hashes'][p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'RESULTS.json').write_text(json.dumps(summary,indent=2))
text='''# Historical AMSCO zero-column recovery — focused search

**No complete message or reliable readable region was recovered.** The focused source-derived encode and decode constructions completed without node caps or unresolved long-erasure cases.

The key set contains45 decimal permutations: insert0 at every nonleading position of `123456789`, `198346572`, `135624789`, `987654321`, and `135792468`. Thirty-six survive a signed32-bit integer conversion; nine descending-base cases explicitly assume64-bit PHP. Each construction includes four observed-text orientations and four orientations between modern encryption and AMSCO.

| Construction | Reconstructed hex lengths | Patterns | Completed checks | Result |
|---|---|---:|---:|---|
| Historical encode used as forward transform | 1170 or1260 | 720 | 54,720 CFB8 algorithm/IV/language cases;609,352 DFS nodes | No compatible complete plaintext |
| Historical decode used as forward transform | 1260 or1262 | 1,440 | 109,440 CFB8 cases | Every case contradicted a provably unaffected plaintext byte/sequence |
| Decode, other modern modes and masked readable regions | 1260 or1262 | 1,440 | 331,200 mode configurations | No compatible known-region message; maximum safe ASCII run18 bytes |

Counts overlap across modern families; they are executed instances, not a fraction of the entire construction space.

## The actual loss mechanism

The recovered2016 AMSCO instructions require consecutive, unrepeated digits but do not explicitly say to start at1. A nonleading-zero permutation of0–9 survives the controller's numeric conversion. The encoder labels columns using those digits, but its output loop visits1 through the width, omitting column0. Continuous2/1 cells and width10 give a sparse loss of78 nibbles from1170, or168 from1260, leaving the observed1092. Only those source-identified missing slots were treated as unknown. [Original class](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/class.amsco.php), [instructions](https://github.com/cryptool-org/cto/blob/887e095c586f7dbae805ae40a29e82ce0d565a6f/_ctoLegacy/tools/amsco/infobox.template).

The decode button behaves differently with those keys: missing label10 makes `getPos` return null; `null+1` selects column1 and overwrites its earlier assignment. Its matching even input lengths are1260 and1262, with a contiguous source chunk erased. Both operation roles were modeled separately. Even lengths were enumerated against the exact projection; missing characters were not arbitrary padding.

## Recovery and validation

Sparse encode holes were solved under CFB8, password `Zombies`, nineteen block primitives and both ASCII-zero/binary-zero IV fills. DFS enumerates missing nibble values and checks plaintext bytes. Failed-state memoization retains position, UTF-8 state and the preceding ciphertext feedback block. Every target case completed below the50-million-node guard.

Language0 permits ASCII32–126 plus tab, CR and LF. Language1 additionally permits UTF-8 NBSP; en/em dashes, specified curly quotes, bullet, ellipsis and narrow NBSP; and a UTF-8 BOM only at the beginning. This is a curated repertoire, not arbitrary Unicode. Every compatible ending is preserved; no missing punctuation was guessed.

All152 planted585/630-byte controls recovered the exact original message **and every missing cipher digit among the candidates**. The66,113 compatible completions are retained in compressed JSONL; each was independently re-encrypted and passed the legacy forward transformation. Printable constraints do not guarantee a unique natural-language answer.

The unchanged historical PHP source was also executed through PHP-WASM8.4.25 with64-bit integers: all152 planted encode forwards and230 planted decode forwards matched exactly, with the original source hash preserved. This verifies source behavior in that runtime, not the historical deployment environment.

For contiguous decode loss, dependency masks identify exactly which plaintext bytes are independent of unknown ciphertext. The mode pass covers CFB8/NCFB/ECB/CBC over19 primitives and97 cached OFB8/OFB/CTR/RC4 configurations, including both IV fills where relevant. Incomplete ECB/CBC tails are not decrypted or invented. All230 independent masked-mode controls recovered exact known plaintext regions, and a negative filler-artifact control passed.

The preliminary unmasked zero-fill run produced4380 artificial hits inside erased spans. The strict masked pass found no safe ASCII run of32 bytes anywhere; its maximum was18. Those filler artifacts are not partial solutions.

An independent review found no false-negative defect in the recurrence, memo key or known-region UTF-8 pruning;66,844 grammar-oracle cases,760 actual-cipher recurrence/pruning cases and102 exhaustive memo comparisons passed. See [independent review](../continuation_audit/zero_column_review/REVIEW.md).

## Limits and artifacts

The negative applies to these45 keys, the stated orientations, `Zombies`, and the accepted text classes. Other keys, additional layers, other IV/key conventions, arbitrary Unicode, binary intermediates and trailing NUL padding remain outside it. This focused DFS is CFB8; other feedback/block modes were checked only where erasure-independent bytes could be determined. Broader key enumeration and NCFB erasure recovery are separate tasks.

`RESULTS.json` records exact counts and hashes. `work.py` generates projections and control chains; `recover.cpp` performs sparse recovery; `masked_modes.cpp` checks dependency-safe regions. The compressed control archive preserves all endings and recovered ciphertexts. The original Rev-7 transcription was not changed.
'''
for a,b in [('contains45','contains 45'),('insert0','insert 0'),('signed32','signed 32'),('assume64','assume 64'),('or1260','or 1260'),('or1262','or 1262'),('cases;609','cases; 609'),('run18','run 18'),('recovered2016','recovered 2016'),('at1','at 1'),('of0','of 0'),('visits1','visits 1'),('column0','column 0'),('Continuous2/1','Continuous 2/1'),('width10','width 10'),('of78','of 78'),('from1170','from 1170'),('or168','or 168'),('from1260','from 1260'),('observed1092','observed 1092'),('label10','label 10'),('column1','column 1'),('are1260','are 1260'),('and1262','and 1262'),('the50','the 50'),('Language0','Language 0'),('ASCII32','ASCII 32'),('Language1','Language 1'),('All152','All 152'),('planted585','planted 585'),('The66,113','The 66,113'),('PHP-WASM8','PHP-WASM 8'),('with64','with 64'),('all152','all 152'),('and230','and 230'),('over19','over 19'),('and97','and 97'),('All230','All 230'),('produced4380','produced 4380'),('of32','of 32'),('was18','was 18'),(';66,844','; 66,844'),(',760',', 760'),('and102','and 102'),('these45','these 45')]:text=text.replace(a,b)
(R/'RESULTS.md').write_text(text)
print('PASS focused zero-column audit:45 keys,2160 patterns,382 actual-PHP planted forwards,152 full erasure recoveries,230 masked-mode controls; no target message')
