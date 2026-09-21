from pathlib import Path
import sys,ast,json,subprocess,re,ctypes as C,random
R=Path(__file__).resolve().parent;P=R.parent;sys.path.insert(0,str(R));sys.path.insert(0,str(P))
from work import plaintext,ori,dec_scatter,literal_decode
from crypto import crypt,ALGS,STREAM,op,bs,lib,ptr
lib.mcrypt_module_close.argtypes=[ptr]
source=(P/'continuation_byte_keys/controls.py').read_text();tree=ast.parse(source);node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='extra_encrypt');helper=ast.get_source_segment(source,node).replace('def extra_encrypt(name,plaintext,mode):','def extra_encrypt(name,plaintext,mode,iv=48):').replace("reg=b'0'*block","reg=bytes([iv])*block");exec(helper)
records=[]
def add(alg,mode,iv,block,extra=False):
 i=len(records);n=630+i%2;rawp=plaintext(n,i%3==1);p=rawp[:n//block*block]if mode in('ecb','cbc')else rawp
 c=(extra_encrypt(alg,p,mode,iv)[0]if extra else crypt(p,alg,mode,b'Zombies',bytes([iv]),encrypt=True))
 c+=(b'\xa5\x81\xfe\xc7'*8)[:n-len(c)];assert len(c)==n
 key=['1234567890','1203456789','1983465720','9876543210'][i%4];inner=(i//4)%4;outer=i%4;h=c.hex().upper();display=ori(literal_decode(ori(h,inner),key),outer);assert len(display)==1092
 pattern=ori(dec_scatter(ori(display,outer),key,2*n),inner);assert all(a=='?'or a==b for a,b in zip(pattern,h))
 records.append(dict(label='masked_control'+str(i),alg=alg,mode=mode,iv=iv,key=key,inner=inner,outer=outer,cipher=h,plain=p.hex().upper(),display=display,pattern=pattern,model='decode'))
for alg in ALGS:
 if alg in STREAM:continue
 t=op(alg.encode(),None,b'ecb',None);block=bs(t);lib.mcrypt_module_close(t)
 for mode in('cfb','ncfb','ecb','cbc','ofb','nofb','ctr'):
  for iv in([48]if mode=='ecb'else[48,0]):add(alg,mode,iv,block)
for alg in('threeway','safer_sk64','safer_sk128'):
 for mode in('cfb','ncfb','ecb','cbc'):
  for iv in([48]if mode=='ecb'else[48,0]):add(alg,mode,iv,12 if alg=='threeway'else 8,True)
add('arcfour','stream',0,1)
(R/'masked_controls_manifest.json').write_text(json.dumps(records,indent=2))
payload=''.join(r['label']+'\t'+r['pattern']+'\n'for r in records);(R/'masked_control_inputs.tsv').write_text(payload)
process=subprocess.run([str(R/'masked_modes')],cwd=P,input=payload,text=True,capture_output=True,check=True);(R/'masked_controls.log').write_text(process.stdout+process.stderr)
found={}
for line in process.stdout.splitlines():
 if not line.startswith('MASK_CANDIDATE '):continue
 f=dict(x.split('=',1)for x in line.split()[1:]);found.setdefault(f['label'],[]).append(f)
for r in records:
 identifier=f"{r['alg']}/{r['mode']}/iv{r['iv']}";matching=[x for x in found.get(r['label'],[])if x['algorithm']==identifier];assert matching,(r['label'],identifier)
 for f in matching:
  h=f['plaintext_mask'];assert len(h)==len(r['pattern'])
  for i in range(0,len(h),2):
   if h[i:i+2]!='??':assert i+2<=len(r['plain'])and h[i:i+2]==r['plain'][i:i+2],(r['label'],i)
  assert int(f['definite'])>=80
# A random known suffix must reject despite the printable constant generated inside a zero-filled gap.
rng=random.Random(849310);raw=''.join(rng.choice('0123456789ABCDEF')for _ in range(1260));p=dec_scatter(literal_decode(raw,'1234567890'),'1234567890',1260)
negative=subprocess.run([str(R/'masked_modes')],cwd=P,input='random_gap_negative\t'+p+'\n',text=True,capture_output=True,check=True);assert not negative.stdout.strip();(R/'masked_negative.log').write_text(negative.stderr)
summary={'complete_chains':len(records),'exact_known_plaintext_regions':len(records),'negative_filler_artifact_controls':1,'original_PHP_verified_separately':True}
(R/'masked_control_results.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))
