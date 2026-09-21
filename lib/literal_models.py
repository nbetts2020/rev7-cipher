"""Literal translations of the recovered PHP algorithms; not a PHP-runtime execution.
Source: official cto commit 887e095c586f7dbae805ae40a29e82ce0d565a6f, _ctoLegacy/tools/.
"""
from pathlib import Path
from math import ceil
PHP_TRIM=' \t\n\r\x00\x0b'
def prep_amsco(s):return ''.join(c for c in s.upper() if c not in PHP_TRIM)
def group5(s):return ' '.join(s[i:i+5] for i in range(0,len(s),5))
def cells(s,k):
 matrix={};col=row=n=1
 while s:
  take=1+n%2;part,s=s[:take],s[take:];matrix.setdefault(row,{})[col]=part
  if col==k:col=1;row+=1
  else:col+=1
  n+=1
 return matrix,row
def amsco_encode(s,key):
 key=str(key);matrix,lastrow=cells(s,len(key));sorted_rows={}
 for r,row in matrix.items():
  sorted_rows[r]={}
  for c,value in row.items():sorted_rows[r][int(key[c-1])]=value
 return ''.join(sorted_rows.get(r,{}).get(c,'') for c in range(1,len(key)+1) for r in range(1,lastrow+1))
def amsco_decode(s,key):
 key=str(key);matrix,lastrow=cells(s,len(key));rows=len(matrix);new={};cypher=s
 for c in range(1,len(key)+1):
  # PHP getPos compares each individual numeric character; absent label => null + 1 == 1.
  # This helper models nonnegative numeric keys; valid-key controls use permutations 1..width.
  pos=next((i+1 for i,ch in enumerate(key) if ch in "0123456789" and int(ch)==c),1)
  for r in range(1,rows+1):
   n=len(matrix.get(r,{}).get(pos,''));new.setdefault(r,{})[pos]=cypher[:n];cypher=cypher[n:]
 return ''.join(new.get(r,{}).get(c,'') for r in range(1,lastrow+1) for c in range(1,len(key)+1))
def php_substr(s,start,length):
 if start<0:start=max(len(s)+start,0)
 return s[start:start+length]
def skytale_core(text,key,fill):
 n=len(text)
 if not n:return ''
 other=ceil(n/key)
 if fill:
  holes=abs(n-key*other);tmp=''
  for t in range(1,holes+1):tmp=php_substr(text,n-t*(key-1),key-1)+' '+tmp
  for i in range(other-holes-1,-1,-1):tmp=php_substr(text,i*key,key)+tmp
  text=tmp
 rows=[text[t:t+key] for t in range(0,n,key)]
 return ''.join(rows[t][j:j+1] for j in range(key) for t in range(other))
def skytale_check_ascii_hex(s):
 # Restricted to ASCII hex/whitespace; eregi's metacharacter quirks are outside this helper.
 return ''.join(c for c in s.upper() if c in 'ABCDEF')
def skytale_decode(s,userkey):return skytale_core(s,ceil(len(s)/userkey),1)
