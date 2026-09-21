from pathlib import Path
import sys,json,subprocess,gzip,re,hashlib,ctypes as C
R=Path(__file__).resolve().parent;P=R.parent
sys.path.insert(0,str(P));sys.path.insert(0,str(P/'continuation_numeric_amsco'));sys.path.insert(0,str(P/'continuation_historical_tools'))
from crypto import ALGS,STREAM,crypt
from literal_models import amsco_encode
from zero_projection import retained_indices as enc_indices,scatter as enc_scatter
from zero_decode_projection import retained_indices as dec_indices,scatter as dec_scatter,literal_decode

BASES=['123456789','198346572','135624789','987654321','135792468']
KEYS=sorted({b[:i]+'0'+b[i:]for b in BASES for i in range(1,10)})
assert len(KEYS)==45 and all(len(k)==10 and len(set(k))==10 and k[0]!='0'for k in KEYS)

def ori(s,k):
 if k==0:return s
 if k==1:return s[::-1]
 if k==2:return ''.join(s[i:i+2]for i in range(len(s)-2,-1,-2))
 return ''.join(s[i:i+2][::-1]for i in range(0,len(s),2))

def encrypted(p,alg,iv):
 if alg not in ['threeway','safer_sk64','safer_sk128']:return crypt(p,alg,'cfb',b'Zombies',bytes([iv]),encrypt=True)
 ex=C.CDLL(str(P/'extras.dylib'));prefix=alg+'_LTX__mcrypt_'
 def integer(s):f=getattr(ex,prefix+s);f.restype=C.c_int;return f()
 size=integer('get_size');block=integer('get_block_size');ks=integer('get_key_size');state=C.create_string_buffer(size)
 setkey=getattr(ex,prefix+'set_key');setkey.argtypes=[C.c_void_p,C.c_void_p,C.c_int];encrypt=getattr(ex,prefix+'encrypt');encrypt.argtypes=[C.c_void_p,C.c_void_p]
 assert setkey(state,b'Zombies'.ljust(ks,b'\0'),ks)==0
 register=bytes([iv])*block;out=bytearray()
 for byte in p:
  buf=C.create_string_buffer(register,block);encrypt(state,buf);c=byte^buf.raw[0];out.append(c);register=register[1:]+bytes([c])
 return bytes(out)

def plaintext(n,typography):
 base=('An “independent” message… tests zero-column recovery — without guessing an ending.\u00a0'if typography else 'An independent message tests zero column recovery without guessing any missing ciphertext. ').encode()
 p=(b'\xef\xbb\xbf'if typography else b'')+base*20;p=p[:n-1]
 while True:
  try:p.decode('utf-8');break
  except UnicodeDecodeError:p=p[:-1]
 return p+b' '*(n-1-len(p))+b'\n'

def make_control(alg,iv,n,typography,index):
 key='1234567890'if n==585 else '1203456789';p=plaintext(n,typography);c=encrypted(p,alg,iv).hex().upper();inner=(index//4)%4;outer=index%4
 displayed=ori(amsco_encode(ori(c,inner),key),outer);assert len(displayed)==1092
 pattern=ori(enc_scatter(ori(displayed,outer),key,2*n),inner);assert all(x=='?'or x==y for x,y in zip(pattern,c))
 return dict(label=f'control{index}',pattern=pattern,alg=alg,iv=iv,language=int(typography),cipher=c,plain=p.hex().upper(),key=key,model='encode',inner=inner,outer=outer,display=displayed)

def controls(pilot=False):
 algs=['rc2','serpent']if pilot else[a for a in ALGS if a not in STREAM]+['threeway','safer_sk64','safer_sk128']
 records=[]
 for alg in algs:
  for iv in ([48]if pilot else[48,0]):
   for n in [585,630]:
    for typography in [False,True]:records.append(make_control(alg,iv,n,typography,len(records)))
 tag='pilot'if pilot else'controls';(R/(tag+'_manifest.json')).write_text(json.dumps(records,indent=2));payload='\n'.join(' '.join([r['label'],r['pattern'],r['alg'],str(r['iv']),str(r['language']),r['cipher'],r['plain']])for r in records)+'\n';(R/(tag+'_inputs.txt')).write_text(payload)
 bylabel={r['label']:r for r in records};expected=set();candidates=0
 # Start with file-backed stdin for deterministic streaming of every completion.
 with open(R/(tag+'_inputs.txt'))as inp,open(R/(tag+'.log'),'w')as err,gzip.open(R/(tag+'_candidates.jsonl.gz'),'wt')as out:
  process=subprocess.Popen([str(R/'recover'),'controls'],cwd=P,stdin=inp,stdout=subprocess.PIPE,stderr=err,text=True)
  for line in process.stdout:
   if not line.startswith('CANDIDATE '):continue
   fields=dict(x.split('=',1)for x in line.split()[1:]);r=bylabel[fields['label']];c=fields['cipher'];p=fields['plain'];candidates+=1
   assert len(c)==len(r['pattern'])and all(a=='?'or a==b for a,b in zip(r['pattern'],c))
   assert ori(amsco_encode(ori(c,r['inner']),r['key']),r['outer'])==r['display']
   # Independent modern re-encryption verifies every recovered missing digit.
   assert encrypted(bytes.fromhex(p),r['alg'],r['iv']).hex().upper()==c
   if c==r['cipher']and p==r['plain']:expected.add(r['label'])
   out.write(json.dumps(fields)+'\n')
  code=process.wait()
 assert code==0,(code,(R/(tag+'.log')).read_text()[-2000:])
 assert expected==set(bylabel),(set(bylabel)-expected)
 result={'controls':len(records),'candidates_preserved':candidates,'exact_planted_cipher_and_plaintext_recoveries':len(expected),'forward_legacy_and_modern_checks':'all candidates','original_PHP_runtime_executed':False}
 (R/(tag+'_results.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result))

def inputs():
 source=''.join((P/'cipher.txt').read_text().split());seen=set();records=[];summary=[]
 for model,indices,scatter in [('encode',enc_indices,enc_scatter),('decode',dec_indices,dec_scatter)]:
  for key in KEYS:
   lengths=[n for n in range(len(source),1501,2)if len(indices(n,key))==len(source)]
   for n in lengths:
    mapping=indices(n,key);assert len(mapping)==len(set(mapping))==1092
    for outer in range(4):
     scattered=scatter(ori(source,outer),key,n)
     for inner in range(4):
      pattern=ori(scattered,inner);digest=hashlib.sha256(pattern.encode()).digest()
      if digest in seen:continue
      seen.add(digest);label=f'{model}_key{key}_n{n}_outer{outer}_inner{inner}';record=dict(label=label,model=model,key=key,n=n,outer=outer,inner=inner,integer_model='signed32'if int(key)<=2147483647 else'signed64',pattern=pattern)
      records.append(record)
    summary.append({'model':model,'key':key,'length':n,'erased_nibbles':n-1092})
 (R/'input_manifest.json').write_text(json.dumps(records,indent=2));(R/'input_shapes.json').write_text(json.dumps(summary,indent=2))
 for model in ['encode','decode']:
  selected=[r for r in records if r['model']==model];(R/(model+'_inputs.tsv')).write_text(''.join(r['label']+'\t'+r['pattern']+'\n'for r in selected));print(model,'patterns',len(selected))
 print('TOTAL',len(records),'keys',len(KEYS))
if __name__=='__main__':
 if len(sys.argv)>1 and sys.argv[1]=='inputs':inputs()
 else:controls(len(sys.argv)>1 and sys.argv[1]=='pilot')
