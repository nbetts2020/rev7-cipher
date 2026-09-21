from pathlib import Path
import hashlib,json,random,sys
root=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(root/'continuation_historical_tools'),str(root/'continuation_numeric_amsco')]
from literal_models import amsco_encode,amsco_decode,prep_amsco
from zero_projection import retained_indices as encode_indices
from zero_decode_projection import retained_indices as decode_indices
rng=random.Random(88017)
cases=[]
def add(text,key,category):
    clean=prep_amsco(text)
    for mode,func in [('encode',amsco_encode),('decode',amsco_decode)]:
        expected=func(clean,key)
        if category=='zero-permutation':
            indices=(encode_indices if mode=='encode' else decode_indices)(len(clean),key)
            assert expected==''.join(clean[i] for i in indices)
        cases.append({'id':len(cases),'mode':mode,'text':text,'key':str(key),'category':category,'expected':expected})
add('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789','135624','valid-fixture')
for width in range(2,10):
    for _ in range(12):
        key=list(str(i) for i in range(1,width+1));rng.shuffle(key);key=''.join(key)
        n=rng.choice([1,2,3,14,15,16,36,99,100,101,1091,1092,1093])
        add(''.join(rng.choice('0123456789ABCDEF') for _ in range(n)),key,'valid-permutation')
keys=['1234567890','1357924680','1023456789','1203456789']
for _ in range(36):
    tail=list('023456789');rng.shuffle(tail);keys.append('1'+''.join(tail))
for key in keys:
    for n in [1,2,3,14,15,16,36,1092,1170,1260,1262,1263]:
        add(''.join(rng.choice('0123456789ABCDEF') for _ in range(n)),key,'zero-permutation')
for key in ('115','935','101','1230','1123','9999'):
    for n in (36,1092):
        add(''.join(rng.choice('0123456789ABCDEF') for _ in range(n)),key,'other-invalid')
add(' abcd 0123\tEF\n4567\r89\x00\x0b','135624','preprocessing')
out=Path(__file__).parent/'cases.json';out.write_text(json.dumps(cases,separators=(',',':'))+'\n')
print(json.dumps({'cases':len(cases),'cases_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'categories':{c:sum(v['category']==c for v in cases) for c in sorted({v['category'] for v in cases})}},indent=2))
