from pathlib import Path
import sys,subprocess,json,re,random,itertools,hashlib
root=Path(__file__).resolve().parents[2];out=Path(__file__).resolve().parent;sys.path.insert(0,str(root));sys.path.insert(0,str(root/'continuation_zero_column'))
from work import encrypted
from crypto import ALGS,STREAM,op,bs,end
rng=random.Random(498120);exe=out/'harness'
allowed=lambda c:c in '\t\r\n' or ' '<=c<='~' or c in '\u00a0\u2013\u2014\u2018\u2019\u201a\u201b\u201c\u201d\u201e\u201f\u2022\u2026\u202f'
def valid(b,lang=1):
 try:s=b.decode('utf-8') if lang else b.decode('ascii')
 except UnicodeError:return False
 if lang and s.startswith('\ufeff'):s=s[1:]
 return all(allowed(c) if lang else c in '\t\r\n' or ' '<=c<='~' for c in s)
def call(mode,lines,tag):
 inp='\n'.join(lines)+'\n';(out/(tag+'.txt')).write_text(inp);r=subprocess.run([str(exe),mode],input=inp,text=True,cwd=root,capture_output=True,check=True);(out/(tag+'.log')).write_text(r.stdout+r.stderr);return r.stdout.splitlines()
# Exhaust every pair of bytes; target multi-byte punctuation/BOM boundaries separately.
grammar=[bytes([x]) for x in range(256)]+[bytes([a,b]) for a in range(256) for b in range(256)]
grammar.extend(bytes(prefix+[x]) for prefix in [[0xE2,0x80],[0xEF,0xBB],[0xE2,0x81],[0xEF,0xBA]] for x in range(256))
for token in ['\ufeff','\u00a0','\u2014','\u2019','\u2022','\u2026','\u202f']:
 b=token.encode();grammar.extend([b+b'A',b'A'+b,b'A'+b+b'B',b'\xef\xbb\xbf'+b+b'X'])
rows=call('grammar',[b.hex().upper() for b in grammar],'grammar');assert len(rows)==len(grammar)
for b,line in zip(grammar,rows):assert bool(int(line))==valid(b),(b.hex(),line,valid(b))
# Known-region pruning with its first safe byte in the middle of a permitted UTF-8 token.
known=[];expect={};counter=0
for alg in [x for x in ALGS if x not in STREAM]+['threeway','safer_sk64','safer_sk128']:
 if alg=='threeway':block=12
 elif alg.startswith('safer_'):block=8
 else:td=op(alg.encode(),None,b'cfb',None);block=bs(td);end(td)
 for iv in [0,48]:
  for gap in [0,1,2,17]:
   for token,offset in [(b'\xc2\xa0',1),(b'\xe2\x80\x94',1),(b'\xe2\x80\x94',2)]:
    first_safe=gap+block+1;p=b'A'*(first_safe-offset)+token+b' ending with allowed text.\n';c=encrypted(p,alg,iv);h=c.hex().upper();pattern=h[:2*gap]+'??'+h[2*gap+2:];label='known'+str(counter);counter+=1
    known.append(f'{label} {pattern} {alg} {iv} 1 {c.hex().upper()} {p.hex().upper()}');expect[label]=True
  for p in [b'\xef\xbb\xbfAllowed BOM.',b'\xef\xbb',b'\xc2',b'ASCII then \xef\xbb\xbf forbidden BOM.',b'\xe2\x80\x94',b'\xe2\x80',b'\xa0',b'final ascii']:
   c=encrypted(p,alg,iv);label='known'+str(counter);counter+=1;known.append(f'{label} {c.hex().upper()} {alg} {iv} 1 {c.hex().upper()} {p.hex().upper()}');expect[label]=valid(p)
rows=call('known',known,'known_boundaries');records=[x for x in rows if x.startswith('KNOWN ')];assert len(records)==len(known)
for row in records:
 fields=row.split();label=fields[1];d=dict(x.split('=') for x in fields[2:]);assert bool(int(d['accepted']))==expect[label],row;assert d['recurrence']=='1',row
# Independent finite exhaustive oracle for the state graph, using a bijective one-byte identity block.
def oracle(pattern,lang,iv):
 choices=[[int(ch,16)] if ch!='?' else range(16) for ch in pattern];solutions=0
 for digits in itertools.product(*choices):
  c=bytes((digits[i]<<4)|digits[i+1] for i in range(0,len(digits),2));p=bytes(x^previous for x,previous in zip(c,bytes([iv])+c[:-1]));solutions+=valid(p,lang)
 return solutions
cases=[('??0065FF',0,0,1),('??004161',0,0,1)]
for i in range(100):
 lang=i%2;iv=48 if i%3 else 0
 p=(b'\xef\xbb\xbf' if lang and i%4==1 else b'')+bytes(rng.choice(b'ABCDE 123.\n') for _ in range(rng.randrange(3,9)));c=bytearray();prev=iv
 for byte in p:y=prev^byte;c.append(y);prev=y
 pattern=list(c.hex().upper());unknown=rng.sample(range(len(pattern)),2 if i%7 else 3)
 for at in unknown:pattern[at]='?'
 if i%3==2:
  at=rng.choice([j for j in range(len(pattern)) if j not in unknown]);pattern[at]=rng.choice('0123456789ABCDEF')
 cases.append((''.join(pattern),lang,iv,0))
rows=call('toy',['%s %d %d %d'%x for x in cases],'memo_comparison');assert len(rows)==2*len(cases)
summary=[]
for i,(pattern,lang,iv,direct) in enumerate(cases):
 count=oracle(pattern,lang,iv);pair=[]
 for row in rows[2*i:2*i+2]:
  d={k:int(v) for k,v in (x.split('=') for x in row.split()[1:])};assert not d['cap'] and not d['long'];assert d['solutions']==count,(pattern,lang,iv,row,count);pair.append(d)
 summary.append({'pattern':pattern,'lang':lang,'iv':iv,'bypass_known_for_memo_unit_test':bool(direct),'oracle_solutions':count,'runs':pair})
assert summary[0]['runs'][0]['memo']>0 and summary[0]['runs'][0]['nodes']<summary[0]['runs'][1]['nodes']
result={'grammar_oracle_cases':len(grammar),'known_region_and_recurrence_cases':len(known),'independent_memo_oracle_cases':len(cases),'memo_examples':summary[:2],'all_passed':True,'source_sha256':hashlib.sha256((root/'continuation_zero_column/recover.cpp').read_bytes()).hexdigest()};(out/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');(out/'memo_cases.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(result))
