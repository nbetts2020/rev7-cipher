#include <mcrypt.h>
#include <algorithm>
#include <array>
#include <chrono>
#include <cstring>
#include <dlfcn.h>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
struct Internal {struct {void* h;char name[64];} ah,mh;void *key,*buf,*given,*me,*md,*ae,*ad,*abs;};
struct Cipher {string name;MCRYPT td;int block;void *key;void (*encrypt)(void*,void*);void (*decrypt)(void*,void*);};
vector<Cipher> cs;
bool ecbfast=getenv("ECB_FAST")!=nullptr;
unsigned long long candidates=0,windows=0,hits=0;
auto began=chrono::steady_clock::now();
bool printable(unsigned char c){return (c>=32&&c<=126)||c==10||c==13||c==9;}
int nib(char c){return c<='9'?c-'0':c-'A'+10;}
string hex(const string &s){const char*h="0123456789ABCDEF";string out;for(unsigned char c:s){out+=h[c>>4];out+=h[c&15];}return out;}
string unhex(const string &s,int phase=0){string out;for(int i=phase;i+1<(int)s.size();i+=2)out+=(char)(nib(s[i])*16+nib(s[i+1]));return out;}
int run(const string &s){int b=0,c=0;for(unsigned char x:s){c=printable(x)?c+1:0;b=max(b,c);}return b;}
unsigned char cfbbyte(const string&c,int pos,const Cipher &a){alignas(16) unsigned char b[32];if(pos>=a.block)memcpy(b,c.data()+pos-a.block,a.block);else {memset(b,'0',a.block-pos);memcpy(b+a.block-pos,c.data(),pos);}a.encrypt(a.key,b);return b[0]^(unsigned char)c[pos];}
void found(const string&c,const Cipher&a,const string&label,const string&mode,int offset=0){
 string p(c.size(),'\0');
 if(mode=="cfb")for(int i=0;i<(int)c.size();i++)p[i]=cfbbyte(c,i,a);
 else {p=c;for(int i=offset;i+a.block<=(int)c.size();i+=a.block){alignas(16) unsigned char b[32];memcpy(b,c.data()+i,a.block);a.decrypt(a.key,b);if(mode=="cbc")for(int k=0;k<a.block;k++)b[k]^=i>=a.block?(unsigned char)c[i-a.block+k]:'0';memcpy(&p[i],b,a.block);}}
 if(run(p)<32)return;
 hits++;cout<<"HIT "<<label<<" "<<a.name<<" "<<mode<<" offset="<<offset<<" run="<<run(p)<<" cipher="<<hex(c)<<" plain="<<hex(p)<<endl;
}
void scanbytes(const string &c,const string&label,bool ecb=false){
 candidates++;
 for(auto&a:cs){
  if(!ecbfast)for(int pos: {0,48,112,208,304,400,496}){
   if(pos+24>(int)c.size())continue;windows++;
   bool good=true;
   for(int i=0;i<16;i++)if(!printable(cfbbyte(c,pos+i,a))){good=false;break;}
   if(good)found(c,a,label,"cfb");
  }
  if(ecb||ecbfast){if(ecbfast&&c.size()%a.block)continue;for(int offset=0;offset<(ecbfast?1:a.block);offset++)for(int base:{0,192,384})for(int cbc=0;cbc<(ecbfast?2:1);cbc++){
   int pos=base+offset;if(pos+2*a.block>(int)c.size())continue;windows++;
   alignas(16) unsigned char b[32];memcpy(b,c.data()+pos,a.block);a.decrypt(a.key,b);
   if(cbc)for(int i=0;i<a.block;i++)b[i]^=pos>=a.block?(unsigned char)c[pos-a.block+i]:'0';
   bool good=true;for(int i=0;i<a.block;i++)if(!printable(b[i])){good=false;break;}
   if(!good)continue;memcpy(b,c.data()+pos+a.block,a.block);a.decrypt(a.key,b);
   if(cbc)for(int i=0;i<a.block;i++)b[i]^=(unsigned char)c[pos+i];
   for(int i=0;i<a.block;i++)if(!printable(b[i])){good=false;break;}
   if(good)found(c,a,label,cbc?"cbc":"ecb",offset);
  }}
 }
}
void scan(const string &s,const string&label,bool ecb=false,bool phase=false){scanbytes(unhex(s),label,ecb);if(phase)scanbytes(unhex(s,1),label+"/phase1",ecb);}
void init(const string &key){
 if(getenv("EXTRA_ONLY")){
  void* dl=dlopen("./extras.dylib",RTLD_NOW);if(!dl){cerr<<dlerror()<<endl;exit(2);}
  for(string name:{"threeway","safer_sk64","safer_sk128"}){
   string prefix=name+"_LTX__mcrypt_";
   auto get=[&](string x){void*p=dlsym(dl,(prefix+x).c_str());if(!p){cerr<<"symbol error"<<endl;exit(2);}return p;};
   auto val=[&](string x){return ((int(*)())get(x))();};
   if(val("self_test")){cerr<<"EXTRA SELFTEST FAILED "<<name<<endl;exit(2);}
   void* expanded=calloc(1,val("get_size"));int ks=val("get_key_size");string k=key;k.resize(ks,'\0');
   ((int(*)(void*,void*,int))get("set_key"))(expanded,k.data(),ks);
   cs.push_back({name,nullptr,val("get_block_size"),expanded,(void(*)(void*,void*))get("encrypt"),(void(*)(void*,void*))get("decrypt")});
  }cerr<<"Extra algorithms "<<cs.size()<<" self-tests PASS key="<<key<<endl;return;
 }
 int n;char**as=mcrypt_list_algorithms(nullptr,&n);for(int i=0;i<n;i++){
 string name=as[i];MCRYPT t=mcrypt_module_open(as[i],nullptr,(char*)"ecb",nullptr);if(!t)continue;
 if(mcrypt_enc_self_test(t)!=0){cerr<<"FAIL "<<name<<endl;exit(2);}
 char iv[32];memset(iv,'0',32);if(mcrypt_generic_init(t,(void*)key.data(),key.size(),iv)){mcrypt_module_close(t);continue;}
 Internal *p=(Internal*)t;
 cs.push_back({name,t,mcrypt_enc_get_block_size(t),p->key,(void(*)(void*,void*))p->ae,(void(*)(void*,void*))p->ad});
 }mcrypt_free_p(as,n);cerr<<"Algorithms "<<cs.size()<<" key="<<key<<endl;}
void progress(const string&phase){cerr<<phase<<" candidates="<<candidates<<" windows="<<windows<<" hits="<<hits<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-began).count()<<endl;}
vector<int> columnmap(int n,int width,const vector<int>&order,int amsco=-1,int pattern=0){
 vector<vector<int>>cols(width);int pos=0,row=0;
 while(pos<n){for(int j=0;j<width&&pos<n;j++){
  int take=amsco<0?1:1+((j+(pattern==0?row:pattern==1?row*width:0)+amsco)%2);
  while(take--&&pos<n)cols[j].push_back(pos++);
 }row++;}
 vector<int> out;out.reserve(n);for(int j:order)for(int x:cols[j])out.push_back(x);return out;
}
string transform(const string&s,const vector<int>&p,bool inverse){string out(s.size(),'0');for(int i=0;i<(int)s.size();i++)if(inverse)out[p[i]]=s[i];else out[i]=s[p[i]];return out;}
void altered(const string&s,const string&label,bool ecb=false,bool phase=false){scan(s,label,ecb,phase);string r=s;reverse(r.begin(),r.end());scan(r,label+"/outrev",ecb,phase);}
unsigned long long nodes=0,limitnodes=0;
int subst[16],used=0;
bool capped=false;
vector<int> cmasks;
int assigned=0;
bool compatible(const string&s,const Cipher&a,int changed){
 if(__builtin_popcount((unsigned)assigned)<9)return true;
 for(int j=0;j<(int)cmasks.size();j++)if((cmasks[j]&changed)&&!(cmasks[j]&~assigned)){
  alignas(16) unsigned char b[32];
  for(int k=0;k<a.block;k++){
   int q=j-a.block+k;
   b[k]=q<0?'0':(subst[nib(s[2*q])]<<4)|subst[nib(s[2*q+1])];
  }
  a.encrypt(a.key,b);int val=(subst[nib(s[2*j])]<<4)|subst[nib(s[2*j+1])];
  if(!printable(val^b[0]))return false;
 }return true;
}
void subdfs(const string&s,string&c,const Cipher&a,int pos,const string&label){
 if(capped)return;
 if(++nodes>limitnodes){capped=true;return;}
 if(pos==min(64,(int)s.size()/2)){
  string full=unhex(s);for(int i=0;i<(int)full.size();i++){int h=subst[nib(s[2*i])],l=subst[nib(s[2*i+1])];full[i]=(max(h,0)<<4)|max(l,0);}
  string mapping;for(int i=0;i<16;i++)mapping+="0123456789ABCDEF"[max(subst[i],0)];
  found(full,a,label+" subst="+mapping,"cfb");return;
 }
 alignas(16) unsigned char b[32];
 if(pos>=a.block)memcpy(b,c.data()+pos-a.block,a.block);else {memset(b,'0',a.block-pos);memcpy(b+a.block-pos,c.data(),pos);}
 a.encrypt(a.key,b);int stream=b[0],h=nib(s[2*pos]),l=nib(s[2*pos+1]);
 if(subst[h]>=0&&subst[l]>=0){int val=subst[h]*16+subst[l];if(printable(val^stream)){c[pos]=val;subdfs(s,c,a,pos+1,label);}return;}
 bool uh=subst[h]<0,ul=subst[l]<0;
 for(int x=0;x<16;x++){
  if(uh?(used>>x&1):(x!=subst[h]))continue;
  if(uh){subst[h]=x;used|=1<<x;assigned|=1<<h;}
  if(h==l){int val=x*17;if(printable(val^stream)&&compatible(s,a,1<<h)){c[pos]=val;subdfs(s,c,a,pos+1,label);}}
  else for(int y=0;y<16;y++){
   if(ul?(used>>y&1):(y!=subst[l]))continue;
   int val=x*16+y;if(!printable(val^stream))continue;
   if(ul){subst[l]=y;used|=1<<y;assigned|=1<<l;}
   c[pos]=val;if(compatible(s,a,(uh?(1<<h):0)|(ul?(1<<l):0)))subdfs(s,c,a,pos+1,label);
   if(ul){subst[l]=-1;used&=~(1<<y);assigned&=~(1<<l);}
  }
  if(uh){subst[h]=-1;used&=~(1<<x);assigned&=~(1<<h);}
 }
}
int main(int argc,char**argv){
 string task=argc>1?argv[1]:"basic",key=argc>2?argv[2]:"Zombies";init(key);
 if(task=="stdin"){string line;while(getline(cin,line)){auto t=line.find('\t');if(t!=string::npos)scan(line.substr(t+1),line.substr(0,t),true,true);}progress("DONE");return 0;}
 ifstream f("cipher.txt");string s,w;while(f>>w)s+=w;
 if(task=="substitution"){
  limitnodes=argc>3?stoull(argv[3]):200000000;
  for(int orientation=0;orientation<4;orientation++){
   string v=s;if(orientation&1)reverse(v.begin(),v.end());if(orientation&2)for(int i=0;i<(int)v.size();i+=2)swap(v[i],v[i+1]);
   for(auto&a:cs){
    cmasks.assign(v.size()/2,0);for(int j=0;j<(int)cmasks.size();j++)for(int k=max(0,j-a.block);k<=j;k++)cmasks[j]|=(1<<nib(v[2*k]))|(1<<nib(v[2*k+1]));
    fill(subst,subst+16,-1);used=assigned=0;nodes=0;capped=false;string c(v.size()/2,'\0');subdfs(v,c,a,0,"orientation="+to_string(orientation));cerr<<"substitution orientation="<<orientation<<" algorithm="<<a.name<<" nodes="<<nodes<<" capped="<<capped<<" hits="<<hits<<endl;}
  }progress("DONE");return 0;
 }
 if(task=="selftest"){
  string p="This is a validation message containing enough printable text to test the entire cipher scanner.\n";
  for(auto&a:cs){string c=p;MCRYPT t=mcrypt_module_open((char*)a.name.c_str(),nullptr,(char*)"cfb",nullptr);string iv(a.block,'0');mcrypt_generic_init(t,(void*)key.data(),key.size(),(void*)iv.data());mcrypt_generic(t,c.data(),c.size());mcrypt_generic_end(t);for(int i=0;i<(int)p.size();i++)if(cfbbyte(c,i,a)!=(unsigned char)p[i]){cerr<<"SELFTEST FAIL "<<a.name<<endl;return 2;}scanbytes(c,"synthetic "+a.name);}
  progress("SELFTEST PASS");return hits>=cs.size()?0:3;
 }
 if(task=="basic"||task=="missing"){
  int maxgap=task=="missing"?(argc>3?stoi(argv[3]):8):0;
  for(int gap=0;gap<=maxgap;gap++){
   if(ecbfast&&gap!=12&&gap!=28&&gap!=60)continue;
   if(task=="missing"&&gap==0)continue;
   int n=s.size()+gap;
   vector<int>positions;
   if(!gap)positions={0};else { // Every visible group boundary, plus each physical line boundary.
    for(int j=0;j<=(int)s.size();j++)if(j==0||j==2||j%5==2||j==(int)s.size())positions.push_back(j);
   }
   for(int width=2;width<=n/2;width++){
    vector<int>order(width);iota(order.begin(),order.end(),0);auto map=columnmap(n,width,order);
    for(int pos:positions)for(int rev=0;rev<2;rev++){
     string v=s;if(rev)reverse(v.begin(),v.end());v.insert(pos,gap,'0');
     for(bool inverse:{true,false}){
      string t=transform(v,map,inverse);
      string label="gap="+to_string(gap)+" pos="+to_string(pos)+" width="+to_string(width)+" rev="+to_string(rev)+" inv="+to_string(inverse);
      altered(t,label,false,gap%2);
     }
    }
   }
   progress("scytale gap="+to_string(gap));
  }
 }
 if(task=="keyedmissing"){
  vector<string>keys={"ZOMBIES","ZOMBIE","REVELATIONS","ORIGINS","TRENCH","THEGIANT","RICHTOFEN","SAMANTHA","MAXIS","MONTY","PRIMIS","KRONORIUM","APOTHICON","AGARTHA","AETHER","SHADOWMAN","115","935","1234567","7654321","BLACKOPS","BLACKOPS3"};
  if(argc>3)keys={argv[3]};
  for(string kw:keys){vector<int>order(kw.size());iota(order.begin(),order.end(),0);stable_sort(order.begin(),order.end(),[&](int a,int b){return kw[a]<kw[b];});
   for(int gap=0;gap<=(argc>4?stoi(argv[4]):16);gap++){
    if(ecbfast&&gap!=12&&gap!=28&&gap!=60)continue;
    int n=s.size()+gap;
    for(int am=-1;am<=1;am++)for(int pat=0;pat<(am<0?1:3);pat++){
     auto map=columnmap(n,kw.size(),order,am,pat);
     for(int pos=0;pos<=(int)s.size();pos++){
      if(!gap&&pos)break;
      for(int rev=0;rev<2;rev++){
       string v=s;if(rev)reverse(v.begin(),v.end());v.insert(pos,gap,'0');
       for(bool inv:{false,true})altered(transform(v,map,inv),"key="+kw+" gap="+to_string(gap)+" pos="+to_string(pos)+" am="+to_string(am)+" pat="+to_string(pat)+" rev="+to_string(rev)+" inv="+to_string(inv),false,gap%2);
      }
     }
    }
   }
   progress("keyed "+kw);
  }
 }
 progress("DONE");
 return 0;
}
