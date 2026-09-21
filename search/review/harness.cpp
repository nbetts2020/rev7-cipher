#include "support.inc"
void identity(void*,void*){}
int main(int argc,char**argv){
 string mode=argc>1?argv[1]:"known";
 if(mode=="toy"){
  Cipher toy={"identity_block1",nullptr,1,nullptr,identity,identity};string pattern;int lang,iv,direct;
  while(cin>>pattern>>lang>>iv>>direct){
   for(bool disable:{false,true}){disable_memo=disable;auto t=parse("toy",pattern);Result r;auto saved=cout.rdstate();cout.setstate(ios_base::failbit);
    if(direct){task=&t;alg=&toy;filliv=iv;language=lang;result={};failed.clear();currentc.assign(t.n,0);currentp.assign(t.n,0);for(int i=0;i<t.n;i++)currentc[i]=(char)t.values[i];dfs(0,0);r=result;}
    else r=solve(t,toy,iv,lang);
    cout.clear(saved);cout<<"TOY disable="<<disable<<" nodes="<<r.nodes<<" solutions="<<r.solutions<<" memo="<<r.memo<<" cap="<<r.capped<<" known_reject="<<r.known_reject<<" long="<<r.unconstrained<<endl;
   }
  }return 0;
 }
 if(mode=="grammar"){language=1;string h;while(cin>>h){auto p=unhex(h);int s=0;for(int i=0;i<(int)p.size()&&s>=0;i++)s=transition(s,(unsigned char)p[i],i);cout<<(s==0)<<endl;}return 0;}
 init("Zombies");setenv("EXTRA_ONLY","1",1);init("Zombies");unsetenv("EXTRA_ONLY");
 string label,h,name,ec,ep;int iv,lang;
 while(cin>>label>>h>>name>>iv>>lang>>ec>>ep){
  auto a=find_if(cs.begin(),cs.end(),[&](const Cipher&x){return x.name==name;});if(a==cs.end())return 2;auto t=parse(label,h,ec,ep);
  task=&t;alg=&*a;filliv=iv;language=lang;result={};failed.clear();currentc.assign(t.n,0);currentp.assign(t.n,0);for(int i=0;i<t.n;i++)currentc[i]=(char)t.values[i];
  bool check=knowncheck();
  // Independently supplied full ciphertext also tests every CFB output byte before any DFS choices.
  currentc=unhex(ec);string full;for(int pos=0;pos<t.n;pos++)full+=(char)(streambyte(pos)^(unsigned char)currentc[pos]);
  cout<<"KNOWN "<<label<<" accepted="<<check<<" definite="<<result.definite<<" recurrence="<<(hex(full)==ep)<<endl;
 }
 return 0;
}
