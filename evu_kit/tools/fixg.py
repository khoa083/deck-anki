# usage: fixg.py file word "G: text" [word "G: text"...] — replace empty grammar field "-" for given words
import sys
p=sys.argv[1]; m=dict(zip(sys.argv[2::2],sys.argv[3::2]))
L=open(p).read().split('\n')
for i,l in enumerate(L):
    f=l.split(' | ')
    if f[0] in m:
        core=[j for j,x in enumerate(f) if not x.startswith(('exb=','ex=','sense='))]
        if len(core)>=10 and f[core[9]]=='-': f[core[9]]=m[f[0]]; L[i]=' | '.join(f)
open(p,'w').write('\n'.join(L))
