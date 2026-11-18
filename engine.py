import json,os,random,sys,urllib.request as u,urllib.error as e
P,N,B,R,Q,K=1,2,3,4,5,6
V=[0,100,320,330,500,900,0]
MATE=100000
INF=10**6
KN=(-33,-31,-18,-14,14,18,31,33)
KI=(-17,-16,-15,-1,1,15,16,17)
DG=(-17,-15,15,17)
OR=(-16,-1,1,16)
CR={0:2,7:1,112:8,119:4}
def _pst():
 t=[[0]*64 for _ in range(8)]
 a=[0,0,4,8,14,24,40,0];c=[0,0,0,10,15,10,5,0]
 for i in range(64):
  r,f=i//8,i%8;cc=min(f,7-f)+min(r,7-r)
  t[1][i]=a[r]+c[r]*(f in(3,4))
  t[2][i]=6*cc-20
  t[3][i]=4*cc-8
  t[4][i]=15*(r==6)+5*(r==0 and f in(3,4))
  t[5][i]=2*cc-6
  t[6][i]=[20,25,10,0,0,10,25,20][f]*(r==0)or max(-50,-15*r)
  t[7][i]=8*cc-24
 return t
T=_pst()
OM=6400
RW=[(_sq>>4)*8+(_sq&7) for _sq in range(128)]
RB=[(7-(_sq>>4))*8+(_sq&7) for _sq in range(128)]
_g=random.Random(0xC0FFEE)
ZH=[[_g.getrandbits(64) for _ in range(128)] for _ in range(13)]
ZS=_g.getrandbits(64)
ZC=[_g.getrandbits(64) for _ in range(16)]
ZE=[_g.getrandbits(64) for _ in range(8)]
def tm(pc,sq):
 t=abs(pc)
 return 0 if t==K else (V[t]+T[t][(RB[sq],RW[sq])[pc>0]])*(pc>0 or-1)
class Pos:
 def __init__(self):
  self.b=[0]*128;self.s=1;self.c=0;self.e=-1;self.h=0;self.z=0;self.u=[];self.k=[4,116];self.sc=0;self.np=0;self.bi=[0,0]
 def fen(self,f):
  p=f.split();self.b=[0]*128
  for r,row in enumerate(p[0].split('/')):
   rk=7-r;fl=0
   for ch in row:
    if ch.isdigit():fl+=int(ch)
    else:
     pc='PNBRQK'.index(ch.upper())+1
     if ch.islower():pc=-pc
     self.b[rk*16+fl]=pc;fl+=1
  self.s=1 if p[1]=='w' else -1
  self.c=0
  if len(p)>2:
   for ch in p[2]:self.c|={'K':1,'Q':2,'k':4,'q':8}.get(ch,0)
  self.e=-1
  if len(p)>3 and p[3]!='-':self.e=ord(p[3][0])-97+(int(p[3][1])-1)*16
  self.h=int(p[4]) if len(p)>4 else 0
  self.u=[];self.k=[4,116];self.sc=0;self.np=0;self.bi=[0,0]
  for sq in range(128):
   pc=self.b[sq]
   if not pc:continue
   t=abs(pc)
   if t==K:self.k[pc<0]=sq;continue
   self.sc+=tm(pc,sq)
   if t!=P:self.np+=V[t]
   if t==B:self.bi[pc<0]+=1
  h=0
  for sq in range(128):
   if sq&0x88:continue
   pc=self.b[sq]
   if pc:h^=ZH[pc+6][sq]
  if self.s<0:h^=ZS
  h^=ZC[self.c]
  if self.e>=0:h^=ZE[self.e&7]
  self.z=h
 def atk(self,sq,by):
  b=self.b
  for d in(-15,-17):
   t=sq+d*by
   if not t&0x88 and b[t]==by*P:return 1
  for d in KN:
   t=sq+d
   if not t&0x88 and b[t]==by*N:return 1
  for d in KI:
   t=sq+d
   if not t&0x88 and b[t]==by*K:return 1
  for d in DG:
   t=sq+d
   while not t&0x88:
    pc=b[t]
    if pc:
     if pc==by*B or pc==by*Q:return 1
     break
    t+=d
  for d in OR:
   t=sq+d
   while not t&0x88:
    pc=b[t]
    if pc:
     if pc==by*R or pc==by*Q:return 1
     break
    t+=d
  return 0
 def gen(self,cap=False):
  b=self.b;s=self.s;mv=[]
  for sq in range(128):
   if sq&0x88:continue
   pc=b[sq]
   if not pc or (pc>0)!=(s>0):continue
   t=abs(pc)
   if t==P:
    d=16*s;sr=(7-5*s)//2;pr=7*(s>0);rk=sq>>4
    o=sq+d
    if not cap and b[o]==0:
     if rk+s==pr:
      for q in(5,4,3,2):mv.append(sq|(o<<7)|(q<<14))
     else:
      mv.append(sq|(o<<7))
      if rk==sr and b[sq+2*d]==0:mv.append(sq|((sq+2*d)<<7))
    for dd in(d-1,d+1):
     to=sq+dd
     if to&0x88:continue
     tg=b[to]
     if tg and (tg>0)!=(s>0):
      if (to>>4)==pr:
       for q in(5,4,3,2):mv.append(sq|(to<<7)|(q<<14))
      else:mv.append(sq|(to<<7))
     elif to==self.e:mv.append(sq|(to<<7))
   elif t==N or t==K:
    for d in(KN if t==N else KI):
     to=sq+d
     if to&0x88:continue
     tg=b[to]
     if not tg:
      if not cap:mv.append(sq|(to<<7))
     elif (tg>0)!=(s>0):mv.append(sq|(to<<7))
    if t==K and not cap:self._cs(mv,sq,s)
   else:
    for d in(DG if t==B else OR if t==R else DG+OR):
     to=sq+d
     while not to&0x88:
      tg=b[to]
      if not tg:
       if not cap:mv.append(sq|(to<<7))
      else:
       if (tg>0)!=(s>0):mv.append(sq|(to<<7))
       break
      to+=d
  return mv
 def _cs(self,mv,ks,s):
  b=self.b;rp=4 if s>0 else -4
  for K,rs,es,ts,cb,tg in((4,7,(5,6),(4,5,6),1,6),(4,0,(3,2,1),(4,3,2),2,2),(116,119,(117,118),(116,117,118),4,118),(116,112,(115,114,113),(116,115,114),8,114)):
   if ks==K and self.c&cb and b[rs]==rp and all(not b[x] for x in es) and all(not self.atk(x,-s) for x in ts):mv.append(ks|(tg<<7))
 def make(self,m):
  b=self.b;f=m&127;t=(m>>7)&127;pr=(m>>14)&7;pc=b[f];s=self.s
  ep=abs(pc)==P and (t&7)!=(f&7) and b[t]==0
  cs=-1;cap=0
  if ep:
   cs=t-16 if s>0 else t+16;cap=b[cs];b[cs]=0
  else:cap=b[t]
  self.u.append((m,cap,cs,self.c,self.e,self.h,self.z,self.sc,self.np,self.bi[0],self.bi[1]))
  h=self.z
  h^=ZH[pc+6][f]
  if cap:h^=ZH[cap+6][cs if ep else t]
  h^=ZC[self.c]
  if self.e>=0:h^=ZE[self.e&7]
  self.sc-=tm(pc,f)
  if cap:
   self.sc-=tm(cap,cs if ep else t)
   ct=abs(cap)
   if ct!=P:self.np-=V[ct]
   if ct==B:self.bi[cap<0]-=1
  b[f]=0
  npc=s*pr if pr else pc
  b[t]=npc
  self.sc+=tm(npc,t)
  if pr:
   self.np+=V[pr]
   if pr==B:self.bi[s<0]+=1
  if abs(pc)==K and abs(t-f)==2:
   rf=t+1 if (t&7)==6 else t-2
   rt=t-1 if (t&7)==6 else t+1
   rp=b[rf]
   h^=ZH[rp+6][rf]
   self.sc-=tm(rp,rf)
   b[rt]=rp;b[rf]=0
   h^=ZH[rp+6][rt]
   self.sc+=tm(rp,rt)
  if pc==K:self.c&=~(3 if s>0 else 12)
  elif pc==R and f in CR:self.c&=~CR[f]
  if t in CR:self.c&=~CR[t]
  self.e=-1
  if abs(pc)==P and abs(t-f)==32:self.e=f+16*s
  self.h=0 if abs(pc)==P or cap else self.h+1
  if abs(pc)==K:self.k[s<0]=t
  self.s=-s
  h^=ZS;h^=ZC[self.c]
  if self.e>=0:h^=ZE[self.e&7]
  h^=ZH[npc+6][t]
  self.z=h
  if self.atk(self.k[s<0],self.s):
   self.unmake();return 0
  return 1
 def unmake(self):
  m,cap,cs,c,e,hh,z,sc,np,b0,b1=self.u.pop()
  b=self.b;f=m&127;t=(m>>7)&127;pr=(m>>14)&7;s=-self.s
  self.s=s;pc=b[t];b[t]=0
  if cs>=0:b[cs]=-P if s>0 else P
  elif cap:b[t]=cap
  b[f]=s*P if pr else pc
  if abs(pc)==K and abs(t-f)==2:
   rf=t+1 if (t&7)==6 else t-2
   rt=t-1 if (t&7)==6 else t+1
   b[rt]=0;b[rf]=R if s>0 else -R
  if abs(pc)==K:self.k[s<0]=f
  self.c=c;self.e=e;self.h=hh;self.z=z;self.sc=sc;self.np=np;self.bi[0]=b0;self.bi[1]=b1
def ev(p):
 ph=min(p.np,OM)
 kw=p.k[0];kb=p.k[1]
 s=p.sc
 s+=(T[K][RW[kw]]*ph+T[7][RW[kw]]*(OM-ph))//OM
 s-=(T[K][RB[kb]]*ph+T[7][RB[kb]]*(OM-ph))//OM
 s+=30*((p.bi[0]>1)-(p.bi[1]>1))
 s+=(sum(p.b[t]==1 for t in(21,22,23))-sum(p.b[t]==-1 for t in(101,102,103)))*15
 return s if p.s>0 else -s
class S:
 def __init__(self,p,budget):
  self.p=p;self.bg=budget;self.n=0;self.tt={};self.ki=[[0,0] for _ in range(256)];self.ab=0;self.hi={}
 def order(self,mv,pl,tm=0,qc=0):
  b=self.p.b;sc=[]
  k0,k1=self.ki[pl]
  for i,m in enumerate(mv):
   s=-i
   if m==tm:s=1000000
   elif (m>>14)&7:s=200000+V[(m>>14)&7]
   else:
    f=m&127;t=(m>>7)&127
    if b[t] or (abs(b[f])==P and (t&7)!=(f&7)):
     x=V[abs(b[t] or P)];y=V[abs(b[f])]
     if qc and x<y:continue
     s=100000+10*x-y
    elif m==k0:s=50000
    elif m==k1:s=40000
   sc.append((-s,m))
  return [m for _,m in sorted(sc)]
 def q(self,a,be,pl):
  self.n+=1
  if self.n>=self.bg:self.ab=1;return 0
  p=self.p;ck=p.atk(p.k[p.s<0],-p.s)
  best=-MATE-1
  if not ck:
   st=ev(p)
   if st>=be:return st
   best=st
   if st>a:a=st
  mv=self.order(p.gen(not ck),pl,0,not ck)
  lg=0
  for m in mv:
   if not p.make(m):continue
   lg+=1
   s=-self.q(-be,-a,pl+1)
   p.unmake()
   if self.ab:return 0
   if s>best:best=s
   if s>=be:return s
   if s>a:a=s
  if ck and not lg:return -MATE+pl
  return best
 def nm(self,d,a,be,pl):
  p=self.p
  if pl>0 and (p.h>=100 or self.hi.get(p.z,0)>=3):return 0
  if d<=0:return self.q(a,be,pl)
  self.n+=1
  if self.n>=self.bg:self.ab=1;return 0
  e=self.tt.get(p.z);tm=0
  if e:
   dd,s,fl,mv=e;tm=mv
   if dd>=d:
    s-=pl*((s>MATE-1000)-(s<-MATE+1000))
    if fl==1:return s
    if fl==2 and s>=be:return s
    if fl==3 and s<=a:return s
  if d>2 and p.np and not p.atk(p.k[p.s<0],-p.s):
   z=p.z;p.s=-p.s;p.z^=ZS
   s=-self.nm(d-3,-be,1-be,pl+1)
   p.s=-p.s;p.z=z
   if s>=be:return s
  a0=a
  mv=self.order(p.gen(),pl,tm)
  lg=0;best=-MATE-1;bm=0
  for m in mv:
   if not p.make(m):continue
   lg+=1
   self.hi[p.z]=self.hi.get(p.z,0)+1
   s=-self.nm(d-1,-be,-a,pl+1)
   self.hi[p.z]-=1
   p.unmake()
   if self.ab:return 0
   if s>best:best=s;bm=m
   if s>a:a=s
   if a>=be:
    f=m&127;t=(m>>7)&127
    if not (p.b[t] or ((m>>14)&7) or (abs(p.b[f])==P and (t&7)!=(f&7))):
     if self.ki[pl][0]!=m:self.ki[pl][1]=self.ki[pl][0];self.ki[pl][0]=m
    break
  if not lg:return -MATE+pl if p.atk(p.k[p.s<0],-p.s) else 0
  s=best+pl*((best>MATE-1000)-(best<-MATE+1000))
  fl=3 if best<=a0 else 2 if best>=be else 1
  if len(self.tt)>3e5:self.tt.clear()
  self.tt[p.z]=(d,s,fl,bm)
  return best
 def root(self,md):
  p=self.p
  mv=[m for m in p.gen() if p.make(m) and (p.unmake() or 1)]
  od=[(0,m) for m in mv];best=mv[0]
  for d in range(1,md+1):
   if d>1 and self.n>=self.bg:break
   self.ab=0;sc=[];a=-MATE-1
   for _,m in od:
    p.make(m)
    self.hi[p.z]=self.hi.get(p.z,0)+1
    s=-self.nm(d-1,-MATE-1,-a,1)
    self.hi[p.z]-=1
    p.unmake()
    if self.ab:break
    if s>a:a=s
    sc.append((s,m))
   if self.ab:break
   sc.sort(key=lambda x:x[0],reverse=True)
   od=sc;best=sc[0][1]
   if sc[0][0]>=MATE-1000:break
  return [m for _,m in od] or [best]
def uci(m):
 f=m&127;t=(m>>7)&127;pr=(m>>14)&7
 s=chr(97+(f&7))+str((f>>4)+1)+chr(97+(t&7))+str((t>>4)+1)
 if pr:s+='nbrq'[pr-2]
 return s
ENV=os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL is not set')
BG=int(os.environ.get('ENGINE_NODES','150000'))
def post(path,body):
 r=u.Request(ENV+path,data=json.dumps(body).encode())
 try:
  with u.urlopen(r) as x:return json.load(x)
 except e.HTTPError as ex:return {'_e':ex.code,'_b':ex.read().decode(errors='replace')}
def replay(moves):
 p=Pos();p.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
 h={p.z:1}
 for u in moves:
  f=ord(u[0])-97+(int(u[1])-1)*16
  t=ord(u[2])-97+(int(u[3])-1)*16
  pr='nbrq'.index(u[4])+2 if len(u)==5 else 0
  if not p.make(f|(t<<7)|(pr<<14)):break
  h[p.z]=h.get(p.z,0)+1
 return h
def play(g):
 p=Pos();p.fen(g['fen'])
 sr=S(p,BG);sr.hi=dict(replay(g.get('moves',[])))
 while g['status']=='your_move':
  rk=sr.root(64);ok=0
  for m in rk:
   g2=post('/move',{'game':g['game'],'move':uci(m)})
   if '_e' not in g2:g=g2;ok=1;break
  if not ok:
   g=post('/move',{'game':g['game'],'move':g['legal_moves'][0]})
   if '_e' in g:sys.exit(f"/move: {g}")
  if g['status']!='your_move':break
  p.fen(g['fen']);sr=S(p,BG);sr.hi=dict(replay(g.get('moves',[])))
 print('game',g['game'],g.get('outcome'),g.get('reason'),file=sys.stderr)
 return g
def main():
 while True:
  g=post('/game',{})
  if '_e' in g:sys.exit(f"/game: {g}")
  if g['status']=='done':break
  g=play(g)
 print('done:',g.get('wins'),'won,',g.get('draws'),'drawn,',g.get('losses'),'lost',file=sys.stderr)
if __name__=='__main__':main()
