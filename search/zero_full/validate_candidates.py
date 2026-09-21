from pathlib import Path
import hashlib,json,sys
root=Path(__file__).resolve().parents[1];here=Path(__file__).parent
sys.path.insert(0,str(root/'continuation_zero_column'))
from work import encrypted,ori
from literal_models import amsco_encode
records=json.loads((here/'candidates_decoded.json').read_text())
observed=''.join((root/'cipher.txt').read_text().split())
checks=[]
for index,r in enumerate(records):
    parts=dict(item.split('=',1) for item in r['label'].split('/')[1:])
    key=parts['key'];inner=int(parts['inner']);outer=int(parts['outer'])
    plain=bytes.fromhex(r['plain']);cipher=bytes.fromhex(r['cipher'])
    actual=encrypted(plain,r['alg'],int(r['iv']))
    assert actual==cipher,(index,'modern')
    assert ori(amsco_encode(ori(r['cipher'],inner),key),outer)==observed,(index,'outer model')
    checks.append({'index':index,'plaintext_bytes':len(plain),'ciphertext_bytes':len(cipher),'modern_reencryption_exact':True,'literal_outer_forward_exact':True,'ciphertext_sha256':hashlib.sha256(cipher).hexdigest(),'plaintext_sha256':hashlib.sha256(plain).hexdigest()})
selected=records[18]
assert 'but my cover was blown' in selected['text']
assert selected['text'].endswith('I better be careful.\n\n\n\n')
(here/'candidate18_plaintext_utf8.txt').write_bytes(bytes.fromhex(selected['plain']))
(here/'candidate18_reconstructed_cipher_hex.txt').write_text(selected['cipher']+'\n')
result={'records':len(records),'modern_reencryption_exact':len(checks),'literal_outer_forward_exact':len(checks),'selected_semantic_candidate_index':18,'selected_candidate_caveat':'The outer transform erases data; exact re-encryption alone does not make this plaintext mathematically unique. Candidate18 is the coherent reading among the recorded language-constrained completions.','observed_compact_sha256':hashlib.sha256(observed.encode()).hexdigest(),'checks':checks}
(here/'candidate_validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
