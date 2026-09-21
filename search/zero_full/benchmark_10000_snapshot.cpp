#include "../zero_column/recovery_support.inc"
#include <map>
#include <stdexcept>

// Original recovery implementation remains included and unchanged for controls.
// This scanner changes enumeration/caching overhead, not the accepted language.
struct Layout {
 int zero,inner,n;
 vector<int> masks;
 map<int,vector<int>> definitely_known;
 int longest_erasure=0;
};
map<pair<int,int>,Layout> layouts;
string orient(string s,int k){
 if(k==1)reverse(s.begin(),s.end());
 else if(k==2){string r;for(int i=(int)s.size()-2;i>=0;i-=2)r+=s.substr(i,2);s=move(r);}
 else if(k==3)for(int i=0;i<(int)s.size();i+=2)swap(s[i],s[i+1]);
 return s;
}
int zero_position(const string&key){
 if(key.size()!=10||key[0]=='0')throw runtime_error("invalid zero permutation");
 string sorted=key;sort(sorted.begin(),sorted.end());if(sorted!="0123456789")throw runtime_error("invalid key labels");
 return key.find('0');
}
const Layout& getlayout(int zero,int inner){
 auto index=make_pair(zero,inner);auto old=layouts.find(index);if(old!=layouts.end())return old->second;
 int n=zero%2?1170:1260;string pattern(n,'0');
 int start=3*(zero/2)+(zero%2?2:0),size=zero%2?1:2;
 for(int row=0;row<n/15;row++)for(int j=0;j<size;j++)pattern[row*15+start+j]='?';
 pattern=orient(pattern,inner);auto t=parse("layout",pattern);
 Layout l{zero,inner,n/2,t.masks,{}};int erasure=0;
 for(int mask:l.masks)if(mask!=255)l.longest_erasure=max(l.longest_erasure,++erasure);else erasure=0;
 for(int block:{8,12,16,24,32}){
  auto& positions=l.definitely_known[block];
  for(int pos=0;pos<l.n;pos++){
   bool safe=l.masks[pos]==255;
   for(int j=max(0,pos-block);j<pos&&safe;j++)safe=l.masks[j]==255;
   if(safe)positions.push_back(pos);
  }
 }
 return layouts.emplace(index,move(l)).first->second;
}
Task projected(const string&display,const string&key,int outer,int inner,const string&label){
 int zero=zero_position(key),n=zero%2?1170:1260,rows=n/15;
 if(display.size()!=1092)throw runtime_error("expected1092 display chars");
 string source=orient(display,outer),pattern(n,'?');int column_for_label[10],starts[10],cursor=0;
 for(int j=0;j<10;j++)column_for_label[key[j]-'0']=j;
 for(int labelnum=1;labelnum<=9;labelnum++){
  starts[labelnum]=cursor;int col=column_for_label[labelnum];cursor+=rows*(col%2?1:2);
 }
 if(cursor!=1092)throw runtime_error("projection length mismatch");
 for(int col=0;col<10;col++){
  int labelnum=key[col]-'0';if(!labelnum)continue;
  int size=col%2?1:2,start=3*(col/2)+(col%2?2:0);
  for(int row=0;row<rows;row++)for(int j=0;j<size;j++)pattern[row*15+start+j]=source[starts[labelnum]+row*size+j];
 }
 pattern=orient(pattern,inner);auto t=parse(label,pattern);
 if(t.masks!=getlayout(zero,inner).masks)throw runtime_error("layout mismatch");
 return t;
}

bool precheck(const Task&t,const Cipher&a,int iv,const Layout&layout){
 const auto& positions=layout.definitely_known.at(a.block);
 int states=1,previous=-2;
 for(int pos:positions){
  if(pos!=previous+1){states=pos==0?1:15;if(pos==1)states|=1<<4;if(pos==2)states|=1<<5;}
  alignas(16) unsigned char block[32];int take=min(pos,a.block);
  memset(block,iv,a.block-take);for(int j=0;j<take;j++)block[a.block-take+j]=t.values[pos-take+j];
  a.encrypt(a.key,block);unsigned char plain=block[0]^t.values[pos];
  int next=0;for(int state=0;state<6;state++)if(states>>state&1){int value=transition(state,plain,pos);if(value>=0)next|=1<<value;}
  if(!next)return false;states=next;previous=pos;
 }
 return previous!=t.n-1||(states&1);
}
bool fastdfs(int pos,int state){
 if(result.capped)return false;
 if(++result.nodes>nodecap){result.capped=true;return false;}
 if(pos==task->n){
  if(state)return false;result.solutions++;
  if(hex(currentc)==task->expectedc&&hex(currentp)==task->expectedp)result.expected=true;
  cout<<"CANDIDATE label="<<task->label<<" alg="<<alg->name<<" iv="<<filliv<<" language="<<language<<" cipher="<<hex(currentc)<<" plain="<<hex(currentp)<<endl;
  return true;
 }
 string key=memo_key(pos,state);if(failed.find(key)!=failed.end()){result.memo++;return false;}
 int stream=streambyte(pos),known=task->values[pos],freebits=(~task->masks[pos])&255,subset=0;bool any=false;
 do{
  int cipher=known|subset,plain=cipher^stream,next=transition(state,plain,pos);
  if(next>=0){currentc[pos]=(char)cipher;currentp[pos]=(char)plain;any=fastdfs(pos+1,next)||any;if(result.capped)break;}
  subset=(subset-freebits)&freebits;
 }while(subset);
 if(!any&&!result.capped)failed.insert(move(key));return any;
}
Result fastsolve(Task&t,const Cipher&a,int iv,const Layout&layout){
 task=&t;alg=&a;filliv=iv;language=1;result={};
 if(!precheck(t,a,iv,layout)){result.known_reject=true;return result;}
 if(layout.longest_erasure>4){result.unconstrained=true;return result;}
 failed.clear();currentc.resize(t.n);currentp.resize(t.n);for(int i=0;i<t.n;i++)currentc[i]=(char)t.values[i];
 fastdfs(0,0);return result;
}

struct DigestBuf:std::streambuf{
 uint64_t hash1=1469598103934665603ULL,hash2=1099511628211ULL,bytes=0;
 void put(unsigned char c){hash1=(hash1^c)*1099511628211ULL;hash2=(hash2+c+0x9e3779b97f4a7c15ULL)*0xbf58476d1ce4e5b9ULL;bytes++;}
 int overflow(int ch)override{if(ch!=traits_type::eof())put(ch);return traits_type::not_eof(ch);}
 std::streamsize xsputn(const char*s,std::streamsize n)override{for(std::streamsize i=0;i<n;i++)put((unsigned char)s[i]);return n;}
 bool operator==(const DigestBuf&o)const{return hash1==o.hash1&&hash2==o.hash2&&bytes==o.bytes;}
};
void controls(){
 string row;uint64_t count=0,solutions=0,nodes=0,outputbytes=0;
 while(getline(cin,row)){
  istringstream in(row);string label,key,display,name,expectedc,expectedp;int outer,inner,iv;
  if(!(in>>label>>key>>outer>>inner>>display>>name>>iv>>expectedc>>expectedp))throw runtime_error("control parse");
  auto a=find_if(cs.begin(),cs.end(),[&](const Cipher&c){return c.name==name;});if(a==cs.end())throw runtime_error("algorithm");
  auto t=projected(display,key,outer,inner,label);t.expectedc=expectedc;t.expectedp=expectedp;
  DigestBuf oldbuf,newbuf;auto saved=cout.rdbuf(&oldbuf);auto original=solve(t,*a,iv,1);cout.rdbuf(&newbuf);
  auto updated=fastsolve(t,*a,iv,getlayout(zero_position(key),inner));cout.rdbuf(saved);
  if(!original.expected||!updated.expected||original.capped||updated.capped||original.unconstrained||updated.unconstrained||original.solutions!=updated.solutions||!(oldbuf==newbuf))throw runtime_error("control mismatch "+label);
  count++;solutions+=updated.solutions;nodes+=updated.nodes;outputbytes+=newbuf.bytes;
  cerr<<"CONTROL label="<<label<<" exact_expected=1 identical_completion_stream=1 candidates="<<updated.solutions<<" nodes="<<updated.nodes<<endl;
 }
 cerr<<"CONTROLS DONE cases="<<count<<" candidates="<<solutions<<" nodes="<<nodes<<" compared_output_bytes="<<outputbytes<<endl;
}
void countspace(){
 string key="0123456789";uint64_t total=0,safe=0;array<uint64_t,10>zero_counts{},safe_zero_counts{},leading{};
 do{if(key[0]=='0')continue;int zero=key.find('0');total++;zero_counts[zero]++;if(key<="2147483647"){safe++;safe_zero_counts[zero]++;leading[key[0]-'0']++;}}while(next_permutation(key.begin(),key.end()));
 cout<<"KEYSPACE total="<<total<<" safe32="<<safe<<" safe_leading1="<<leading[1]<<" safe_leading2="<<leading[2]<<endl;
 for(int zero=1;zero<=9;zero++)cout<<"ZERO_POSITION "<<zero<<" full="<<zero_counts[zero]<<" safe32="<<safe_zero_counts[zero]<<endl;
 if(total!=3265920||safe!=416400)throw runtime_error("key counts");
}
int main(int argc,char**argv){
 string mode=argc>1?argv[1]:"benchmark";
 if(mode=="count"){countspace();return 0;}
 if(mode=="project"){
  string line;while(getline(cin,line)){istringstream in(line);string key,display;int outer,inner;in>>key>>outer>>inner>>display;auto t=projected(display,key,outer,inner,"projection");cout<<t.pattern<<endl;}return 0;
 }
 init("Zombies");setenv("EXTRA_ONLY","1",1);init("Zombies");unsetenv("EXTRA_ONLY");
 if(mode=="controls"){controls();return 0;}
 if(mode!="benchmark")throw runtime_error("only bounded benchmark enabled");
 uint64_t wanted=argc>2?stoull(argv[2]):10000;if(wanted<1||wanted>10000)throw runtime_error("benchmark cap10000keys");
 string source,w;ifstream input("cipher.txt");while(input>>w)source+=w;
 uint64_t total=3265920,ordinal=0,selected=0,cases=0,rejected=0,caps=0,longerasure=0,nodes=0,solutions=0,safe=0;
 array<uint64_t,10>zero_counts{};auto start=chrono::steady_clock::now();
 string key="0123456789";
 do{
  if(key[0]=='0')continue;uint64_t target=selected*total/wanted;if(ordinal++!=target)continue;
  selected++;int zero=zero_position(key);zero_counts[zero]++;safe+=key<="2147483647";
  for(int outer=0;outer<4;outer++)for(int inner=0;inner<4;inner++){
   string label="zeroencode/key="+key+"/outer="+to_string(outer)+"/inner="+to_string(inner);
   auto t=projected(source,key,outer,inner,label);const auto& layout=getlayout(zero,inner);
   for(auto&a:cs)for(int iv:{48,0}){
    auto r=fastsolve(t,a,iv,layout);cases++;rejected+=r.known_reject;caps+=r.capped;longerasure+=r.unconstrained;nodes+=r.nodes;solutions+=r.solutions;
    if(r.capped||r.unconstrained)cerr<<"INCOMPLETE "<<label<<" alg="<<a.name<<" iv="<<iv<<" capped="<<r.capped<<" long_erasure="<<r.unconstrained<<endl;
   }
  }
  if(selected%1000==0)cerr<<"PROGRESS keys="<<selected<<" cases="<<cases<<" nodes="<<nodes<<" candidates="<<solutions<<" seconds="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<endl;
  if(selected==wanted)break;
 }while(next_permutation(key.begin(),key.end()));
 double seconds=chrono::duration<double>(chrono::steady_clock::now()-start).count();
 cerr<<"DONE BENCHMARK keys="<<selected<<" cases="<<cases<<" rejected_known="<<rejected<<" nodes="<<nodes<<" candidates="<<solutions<<" capped="<<caps<<" long_erasure="<<longerasure<<" safe32_keys="<<safe<<" seconds="<<seconds<<" extrapolated_full_seconds="<<seconds/selected*total<<" extrapolated_safe32_seconds="<<seconds/selected*416400<<endl;
 for(int zero=1;zero<=9;zero++)cerr<<"BENCHMARK_ZERO_POSITION "<<zero<<" keys="<<zero_counts[zero]<<endl;
 return selected==wanted?0:2;
}
