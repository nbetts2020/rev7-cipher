from pathlib import Path
import urllib.request,urllib.error,json,hashlib,re,concurrent.futures,datetime

ROOT=Path(__file__).resolve().parent/'deployment_audit_20260913'
ROOT.mkdir(exist_ok=True)
HEAD={'User-Agent':'Rev7-public-source-audit/1.0'}
def fetch(url):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers=HEAD),timeout=25)as r:
   body=r.read(2500000);encoding='latin-1' if url.endswith('.php') else 'utf-8';return dict(url=url,final_url=r.url,status=r.status,headers=dict(r.headers),raw_sha256=hashlib.sha256(body).hexdigest(),encoding=encoding,body=body.decode(encoding,'replace'))
 except urllib.error.HTTPError as e:return dict(url=url,status=e.code,final_url=e.url,error=str(e))
 except Exception as e:return dict(url=url,error=str(e))
def run():
 forks_result=fetch('https://api.github.com/repos/cryptool-org/cto/forks?per_page=100&sort=newest')
 forks=json.loads(forks_result['body']);(ROOT/'fork_metadata.json').write_text(json.dumps(forks,indent=2))
 sites=[
  'https://www.cryptool.org/en/cto/',
  'https://www.cryptool.org/en/cto/amsco/',
  'https://legacy.cryptool.org/en/cto/',
  'https://legacy.cryptool.org/en/cto/amsco',
  'https://legacy.cryptool.org/en/cto/amsco.html',
  'https://www.cryptool-online.org/',
  'https://www.cryptool-online.org/index.php?option=com_cto&view=tool&Itemid=64&lang=en',
  'https://www.cryptool-online.org/index.php?option=com_cto&view=tool&Itemid=125&lang=en',
 ]
 historical=ROOT.parent/'continuation_historical_tools/_ctoLegacy__tools__amsco__class.amsco.php'
 historic_hash=hashlib.sha256(historical.read_bytes()).hexdigest()
 jobs=[('site',u)for u in sites]+[('fork',f'https://raw.githubusercontent.com/{f["full_name"]}/{f["default_branch"]}/_ctoLegacy/tools/amsco/class.amsco.php')for f in forks]
 rows=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
  for (kind,url),r in zip(jobs,pool.map(lambda x:fetch(x[1]),jobs)):
   body=r.pop('body','');r['kind']=kind
   if body:
    r['sha256']=r['raw_sha256'];r['historical_source_identical']=r['sha256']==historic_hash if kind=='fork'else None
    r['title']=re.findall(r'<title[^>]*>(.*?)</title>',body,re.S|re.I)[:1]
    r['amsco_mentions']=[body[max(0,m.start()-120):m.end()+220]for m in list(re.finditer('amsco',body,re.I))[:12]]
    r['github_links']=sorted(set(re.findall(r'https://github.com/[^\s<>"\x27]+',body)))[:30]
    filename=f'{len(rows):02d}_'+('source.php'if kind=='fork'else'page.html');(ROOT/filename).write_bytes(body.encode(r['encoding']));r['saved_body']=filename
   rows.append(r);print(json.dumps({k:r.get(k)for k in ['kind','url','status','final_url','historical_source_identical','title','error']}),flush=True)
 (ROOT/'results.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_source_sha256':historic_hash,'fork_count':len(forks),'forks_pushed_since_sep7':[f['full_name']for f in forks if f['pushed_at']>='2026-09-07'],'requests':rows},indent=2))
if __name__=='__main__':run()
