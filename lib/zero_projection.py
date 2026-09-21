"""Projection for historical AMSCO's invalid nonleading-zero0..9 permutation keys.
Core model assumes the numeric key survives the PHP wrapper's integer cast.
Use 10-digit keys below2^31 when avoiding PHP platform-size ambiguity.
"""
from pathlib import Path
import sys,random,json

def retained_indices(n,key):
 key=str(key)
 if len(key)!=10 or set(key)!=set('0123456789') or key[0]=='0':raise ValueError('Expected nonleading-zero permutation of0..9')
 columns={i:[] for i in range(10)};pos=cell=0
 while pos<n:
  size=2 if cell%2==0 else 1;column=cell%10;columns[int(key[column])].extend(range(pos,min(pos+size,n)));pos+=size;cell+=1
 return [i for label in range(1,11) for i in columns.get(label,[])]

def scatter(output,key,original_length):
 indices=retained_indices(original_length,key)
 if len(indices)!=len(output):raise ValueError((len(indices),len(output)))
 out=['?']*original_length
 for i,ch in zip(indices,output):out[i]=ch
 return ''.join(out)

def validate():
 sys.path.insert(0,str(Path(__file__).resolve().parent));from literal_models import amsco_encode
 rng=random.Random(80115);tests=0
 for _ in range(200):
  tail=list('023456789');rng.shuffle(tail);key='1'+''.join(tail);n=rng.randrange(1,1500);source=''.join(rng.choice('0123456789ABCDEF') for _ in range(n));mapping=retained_indices(n,key)
  projection=''.join(source[i] for i in mapping);literal=amsco_encode(source,key);assert projection==literal
  assert len(set(mapping))==len(mapping)
  rebuilt=scatter(literal,key,n);assert all(c=='?' or c==s for c,s in zip(rebuilt,source));tests+=1
 rows=[]
 for key in ('1234567890','1357924680','1023456789','1203456789'):
  n=1170 if key.index('0')%2 else 1260
  assert len(retained_indices(n,key))==1092
  lengths=[v for v in range(n-16,n+17) if v%2==0 and len(retained_indices(v,key))==1092]
  rows.append({'key':key,'zero_column_zero_based':key.index('0'),'even_original_lengths':lengths,'output_length':1092,'within_signed32bit':int(key)<=2147483647})
 out={'literal_PHP_core_comparisons':tests,'original_PHP_runtime_executed':False,'cases':rows}
 (Path(__file__).parent/'zero_projection_controls.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':validate()
