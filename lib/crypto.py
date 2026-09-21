import ctypes as C
import pathlib,base64
ROOT=pathlib.Path(__file__).resolve().parent
lib=C.CDLL(str(ROOT/'mcrypt/lib/libmcrypt.dylib'))
def bind(name,rest,args):
 f=getattr(lib,name);f.restype=rest;f.argtypes=args;return f
ptr=C.c_void_p; integer=C.c_int; string=C.c_char_p
op=bind('mcrypt_module_open',ptr,[string,string,string,string])
init=bind('mcrypt_generic_init',integer,[ptr,ptr,integer,ptr])
dec=bind('mdecrypt_generic',integer,[ptr,ptr,integer])
enc=bind('mcrypt_generic',integer,[ptr,ptr,integer])
end=bind('mcrypt_generic_end',integer,[ptr])
bs=bind('mcrypt_enc_get_block_size',integer,[ptr])
ivsize=bind('mcrypt_enc_get_iv_size',integer,[ptr])
test=bind('mcrypt_module_self_test',integer,[string,string])
lst=bind('mcrypt_list_algorithms',C.POINTER(string),[string,C.POINTER(integer)])
count=integer(); algs_ptr=lst(None,C.byref(count));ALGS=[algs_ptr[i].decode() for i in range(count.value)]
STREAM={'arcfour','wake','enigma'}
def crypt(data,alg,mode='cfb',key=b'Zombies',iv=b'0',encrypt=False):
 td=op(alg.encode(),None,mode.encode(),None)
 if not td:raise ValueError((alg,mode))
 vs=ivsize(td);vec=(iv*vs)[:vs] if iv else bytes(vs)
 if init(td,key,len(key),vec):raise ValueError((alg,mode,key))
 buf=C.create_string_buffer(data)
 result=(enc if encrypt else dec)(td,buf,len(data));end(td)
 if result:raise ValueError(result)
 return buf.raw[:len(data)]

def validate():
 for alg in ALGS:
  assert test(alg.encode(),None)==0,alg
 s=base64.b64decode('LeIXjxfrjSpfgR1RnFDIZr0t2JDCRjgueCZqdIiZwvNXC0/yTS76kfRMb/sTi7p3')
 p=crypt(s,'rc2','ecb').rstrip(b'\0')
 assert p==b'=cSr+4oEQ6IObJJ8nRTt7+opLqDeJDJOunfLG2DTAHwc\n',repr(p)
 p=crypt(base64.b64decode(p[::-1]),'rijndael-256','ecb').rstrip(b'\0')
 assert p==b'The many worlds are now one.\n',repr(p)
 c=bytes.fromhex('d865ecd86169a6ccfe60eb53a106aee3e2521ff9ff9eff881fd3246fc64918d68193cdf01ae4d7f5cd64d832dcabef9e6e96c2583daa26a5330c34bec8996cdb03a002d0b93b9a51462a40d62a24443ea1aab2bb5b450bd6482a2cae6bf46404643fec918f9eb421d93d1bd81a79e94868e2ab4cdea2226aee3fdc92202fad')
 expected=b'ka ykhociq vazr vcgg vi bk vaij xktp skji gcei vcraktr xkt vcgg oi btgg otr cr cq rchi rk sk qkhivaipi jiv zjb qcjs z jiv qkjs'
 expected+=b'\n'
 assert crypt(c,'serpent')==expected
 assert crypt(expected,'serpent',encrypt=True)==c
 print('PASS: all',len(ALGS),'algorithm self-tests; published Rev-1 RC2/Rijndael ECB layers; Rev-6 Serpent CFB decrypt and exact re-encryption')
if __name__=='__main__':validate();print(ALGS)
