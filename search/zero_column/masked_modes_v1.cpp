#include "recovery_support.inc"
struct KeyStream{string name,bytes;};vector<KeyStream>kstreams;
uint64_t cfgs=0,maskhits=0;
bool spanvalid(const string&p,const vector<bool>&safe,int lang){
 language=lang;int states=1;bool previous=false;
 for(int i=0;i<(int)p.size();i++){
  if(!safe[i]){previous=false;continue;}
  if(!previous){states=i==0?1:(language?15:1);if(language&&i==1)states|=1<<4;if(language&&i==2)states|=1<<5;}
  int next=0;for(int state=0;state<6;state++)if(states>>state&1){int to=transition(state,(unsigned char)p[i],i);if(to>=0)next|=1<<to;}
  if(!next)return false;states=next;previous=true;
 }return !previous||(states&1);
}
void consider(const Task&t,const string&p,const vector<bool>&safe,const string&name){
 cfgs++;int definite=count(safe.begin(),safe.end(),true);if(definite<80)return;
 bool ascii=spanvalid(p,safe,0),utf=spanvalid(p,safe,1);if(!ascii&&!utf)return;
 maskhits++;string out;for(int i=0;i<t.n;i++)out+=safe[i]?hex(p.substr(i,1)):"??";
 cout<<"MASK_CANDIDATE label="<<t.label<<" algorithm="<<name<<" definite="<<definite<<" ascii="<<ascii<<" typography="<<utf<<" plaintext_mask="<<out<<endl;
}
void scanmask(Task&t){
 vector<bool>known(t.n);string c(t.n,'\0');for(int i=0;i<t.n;i++){known[i]=t.masks[i]==255;c[i]=(char)t.values[i];}
 auto complete=[&](int start,int count){if(start<0||start+count>t.n)return false;for(int i=start;i<start+count;i++)if(!known[i])return false;return true;};
 for(auto&a:cs)for(int iv:{48,0}){
  alg=&a;filliv=iv;currentc=c;
  {string p(t.n,'\0');vector<bool>safe(t.n);for(int i=0;i<t.n;i++)if(known[i]&&complete(max(0,i-a.block),min(i,a.block))){safe[i]=true;p[i]=streambyte(i)^(unsigned char)c[i];}consider(t,p,safe,a.name+"/cfb/iv"+to_string(iv));}
  {string p(t.n,'\0');vector<bool>safe(t.n);for(int start=0;start<t.n;start+=a.block){if(start>0&&!complete(start-a.block,a.block))continue;alignas(16)unsigned char b[32];if(start==0)memset(b,iv,a.block);else memcpy(b,c.data()+start-a.block,a.block);a.encrypt(a.key,b);for(int j=0;j<a.block&&start+j<t.n;j++)if(known[start+j]){safe[start+j]=true;p[start+j]=b[j]^(unsigned char)c[start+j];}}consider(t,p,safe,a.name+"/ncfb/iv"+to_string(iv));}
  for(string mode:{"ecb","cbc"}){
   if(mode=="ecb"&&iv==0)continue;string p(t.n,'\0');vector<bool>safe(t.n);
   for(int start=0;start+a.block<=t.n;start+=a.block){if(!complete(start,a.block))continue;alignas(16)unsigned char b[32];memcpy(b,c.data()+start,a.block);a.decrypt(a.key,b);
    for(int j=0;j<a.block;j++){int i=start+j;if(mode=="cbc"&&start&& !known[i-a.block])continue;safe[i]=true;p[i]=b[j]^(mode=="cbc"?(start?(unsigned char)c[i-a.block]:iv):0);}
   }consider(t,p,safe,a.name+"/"+mode+"/iv"+to_string(iv));
  }
 }
 for(auto&ks:kstreams){string p=c;for(int i=0;i<t.n;i++)p[i]^=ks.bytes[i];consider(t,p,known,ks.name);}
}
int main(){
 init("Zombies");setenv("EXTRA_ONLY","1",1);init("Zombies");unsetenv("EXTRA_ONLY");
 for(auto&a:cs)if(a.td)for(string mode:{"ofb","nofb","ctr"})for(int iv:{48,0}){
  MCRYPT td=mcrypt_module_open((char*)a.name.c_str(),nullptr,(char*)mode.c_str(),nullptr);string vec(a.block,(char)iv),z(2048,'\0');if(mcrypt_generic_init(td,(void*)"Zombies",7,vec.data()))return 2;mcrypt_generic(td,z.data(),z.size());mcrypt_generic_end(td);kstreams.push_back({a.name+"/"+mode+"/iv"+to_string(iv),z});
 }
 {MCRYPT td=mcrypt_module_open((char*)"arcfour",nullptr,(char*)"stream",nullptr);string z(2048,'\0');mcrypt_generic_init(td,(void*)"Zombies",7,nullptr);mcrypt_generic(td,z.data(),z.size());mcrypt_generic_end(td);kstreams.push_back({"arcfour/stream/iv0",z});}
 string row;int inputs=0;while(getline(cin,row)){istringstream in(row);string label,pattern;in>>label>>pattern;auto t=parse(label,pattern);scanmask(t);inputs++;}
 cerr<<"DONE masked_modes inputs="<<inputs<<" configurations="<<cfgs<<" candidates="<<maskhits<<" cached_streams="<<kstreams.size()<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-began).count()<<endl;
}
