from pathlib import Path
import sys,json,hashlib,concurrent.futures
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from deployment_audit_20260913 import fetch,ROOT

def main():
 response=fetch('https://api.github.com/repos/fschell/cryptool-online/forks?per_page=100')
 forks=json.loads(response['body']);(ROOT/'old_family_forks.json').write_text(json.dumps(forks,indent=2))
 names=['fschell/cryptool-online']+[x['full_name']for x in forks]
 urls=[f'https://raw.githubusercontent.com/{n}/master/_ctoLegacy/tools/amsco/class.amsco.php'for n in names]
 extra=['http://www.cryptool-online.org/','http://www.cryptool-online.org/index.php?option=com_cto&view=tool&Itemid=64&lang=en','https://cryptool-online.org/']
 original=(ROOT.parent/'continuation_historical_tools/_ctoLegacy__tools__amsco__class.amsco.php').read_bytes();digest=hashlib.sha256(original).hexdigest();rows=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
  for i,r in enumerate(pool.map(fetch,urls+extra)):
   body=r.pop('body','')
   if i<len(names):r['repo']=names[i];r['identical_to_2016_source']=r.get('raw_sha256')==digest
   if body:
    name=f'old_family_{i}.php'if i<len(names)else f'old_hostname_{i}.html';(ROOT/name).write_bytes(body.encode(r['encoding']));r['saved_body']=name
   rows.append(r);print(json.dumps({k:r.get(k)for k in ['repo','url','status','final_url','identical_to_2016_source','error']}),flush=True)
 result={'historical_sha256':digest,'fork_count':len(forks),'forks_pushed_since_sep7':[x['full_name']for x in forks if x['pushed_at']>='2026-09-07'],'requests':rows}
 (ROOT/'old_family_results.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
