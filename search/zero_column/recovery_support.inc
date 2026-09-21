#define main former_search_main
#include "../../lib/search.cpp"
#undef main
#include <unordered_set>
#include <cstdint>
struct Task {string label,pattern,expectedc,expectedp;vector<int>values,masks;int n;};
struct Result {uint64_t nodes=0,solutions=0,memo=0;bool capped=false,expected=false,known_reject=false,unconstrained=false;int definite=0,longest_known=0;};
Task*task;const Cipher*alg;int filliv,language;string currentc,currentp;Result result;unordered_set<string>failed;uint64_t nodecap=50000000;
int transition(int state,unsigned char c,int pos){
 if(state==0){if(printable(c))return 0;if(!language)return -1;if(c==0xC2)return 1;if(c==0xE2)return 2;if(c==0xEF&&pos==0)return 4;return -1;}
 if(state==1)return c==0xA0?0:-1;
 if(state==2)return c==0x80?3:-1;
 if(state==3){for(int x:{0x93,0x94,0x98,0x99,0x9A,0x9B,0x9C,0x9D,0x9E,0x9F,0xA2,0xA6,0xAF})if(c==x)return 0;return -1;}
 if(state==4)return pos==1&&c==0xBB?5:-1;
 if(state==5)return pos==2&&c==0xBF?0:-1;
 return -1;
}
unsigned char streambyte(int pos){alignas(16)unsigned char b[32];int take=min(pos,alg->block);memset(b,filliv,alg->block-take);memcpy(b+alg->block-take,currentc.data()+pos-take,take);alg->encrypt(alg->key,b);return b[0];}
string memo_key(int pos,int state){string k;k+=(char)(pos&255);k+=(char)(pos>>8);k+=(char)state;int take=min(pos,alg->block);k.append(currentc.data()+pos-take,take);return k;}
bool dfs(int pos,int state){
 if(result.capped)return false;
 if(++result.nodes>nodecap){result.capped=true;return false;}
 if(pos==task->n){if(state)return false;result.solutions++;if(hex(currentc)==task->expectedc&&hex(currentp)==task->expectedp)result.expected=true;
  cout<<"CANDIDATE label="<<task->label<<" alg="<<alg->name<<" iv="<<filliv<<" language="<<language<<" cipher="<<hex(currentc)<<" plain="<<hex(currentp)<<endl;return true;
 }
 string mk=memo_key(pos,state);if(failed.find(mk)!=failed.end()){result.memo++;return false;}
 int stream=streambyte(pos);bool any=false;int known=task->values[pos],mask=task->masks[pos];
 for(int c=0;c<256;c++){if((c&mask)!=known)continue;int p=c^stream,next=transition(state,p,pos);if(next<0)continue;currentc[pos]=(char)c;currentp[pos]=(char)p;any=dfs(pos+1,next)||any;if(result.capped)break;}
 if(!any&&!result.capped)failed.insert(move(mk));return any;
}
bool knowncheck(){
 vector<bool>safe(task->n);string p(task->n,'\0');int longest=0,runlen=0;
 for(int i=0;i<task->n;i++){
  bool good=task->masks[i]==255;for(int j=max(0,i-alg->block);j<i&&good;j++)good=task->masks[j]==255;
  if(good){safe[i]=true;result.definite++;p[i]=streambyte(i)^(unsigned char)currentc[i];if(printable((unsigned char)p[i]))longest=max(longest,++runlen);else runlen=0;}else runlen=0;
 }
 result.longest_known=longest;
 if(longest>=48){string rendered;for(int i=0;i<task->n;i++)rendered+=safe[i]?hex(p.substr(i,1)):"??";
  cout<<"KNOWN_REGION label="<<task->label<<" alg="<<alg->name<<" iv="<<filliv<<" language="<<language<<" run="<<longest<<" plain="<<rendered<<endl;
 }
 int states=1;bool previous_safe=false;
 for(int i=0;i<task->n;i++){
  if(!safe[i]){previous_safe=false;continue;}
  if(!previous_safe){states=i==0?1:(language?15:1);if(language&&i==1)states|=1<<4;if(language&&i==2)states|=1<<5;}
  int next=0;for(int s=0;s<6;s++)if(states>>s&1){int t=transition(s,(unsigned char)p[i],i);if(t>=0)next|=1<<t;}
  if(!next)return false;states=next;previous_safe=true;
 }
 if(previous_safe&&!(states&1))return false;return true;
}
Result solve(Task&t,const Cipher&a,int iv,int lang){
 task=&t;alg=&a;filliv=iv;language=lang;result={};failed.clear();currentc.resize(t.n);currentp.resize(t.n);for(int i=0;i<t.n;i++)currentc[i]=(char)t.values[i];
 if(!knowncheck()){result.known_reject=true;return result;}
 int longest=0,rr=0;for(int m:t.masks){if(m!=255)longest=max(longest,++rr);else rr=0;}
 // A surviving long contiguous erased span is not enumerated as arbitrary prose.
 if(longest>4){result.unconstrained=true;return result;}
 dfs(0,0);return result;
}
Task parse(string label,string h,string ec="",string ep=""){
 Task t{label,h,ec,ep,{},{},(int)h.size()/2};if(h.size()%2)throw runtime_error("odd hex length");
 for(int i=0;i<(int)h.size();i+=2){int mask=0,value=0;for(int j=0;j<2;j++){mask<<=4;value<<=4;if(h[i+j]!='?'){mask|=15;value|=nib(h[i+j]);}}t.values.push_back(value);t.masks.push_back(mask);}return t;
}
