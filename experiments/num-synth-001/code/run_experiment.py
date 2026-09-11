#!/usr/bin/env python3
"""Frozen held-out numerical oracle, CG/diagonal-PCG, and bad-control check."""
import json
from pathlib import Path
import numpy as np

OUT=Path(__file__).resolve().parents[1]/"reproduced"
HELD=[(32,"contrast","low"),(64,"smooth","mixed"),(128,"constant","polyexp"),(128,"anisotropic","polyexp"),(64,"contrast","mixed")]
DESIGN=[(32,"constant","low"),(64,"constant","mixed"),(64,"smooth","low"),(128,"smooth","polyexp"),(64,"anisotropic","mixed"),(128,"anisotropic","low"),(64,"contrast","polyexp"),(128,"contrast","mixed")]
def coef(kind,x,y):
    if kind=="constant": return np.ones_like(x),np.ones_like(x)
    if kind=="smooth": a=1+.45*np.sin(2*np.pi*x)*np.sin(np.pi*y); return a,a
    if kind=="anisotropic": return 1+.7*np.cos(np.pi*y)**2,.25+.5*np.sin(np.pi*x)**2
    a=np.exp(2.2*np.sin(2*np.pi*x)*np.sin(2*np.pi*y)); return a,a
def exact(kind,x,y):
    if kind=="low": return np.sin(np.pi*x)*np.sin(np.pi*y)
    if kind=="mixed": return np.sin(3*np.pi*x)*np.sin(2*np.pi*y)+.35*np.sin(5*np.pi*x)*np.sin(np.pi*y)
    return x*(1-x)*y*(1-y)*np.exp(.7*x-.4*y)
def problem(n,coefficient,solution):
    h=1/(n+1); q=np.arange(n+2)*h; x,y=np.meshgrid(q,q,indexing="ij"); u=exact(solution,x,y); ax,ay=coef(coefficient,x,y)
    hm=lambda a,b:2*a*b/(a+b); xp=hm(ax[1:-1,1:-1],ax[2:,1:-1]); xm=hm(ax[1:-1,1:-1],ax[:-2,1:-1]); yp=hm(ay[1:-1,1:-1],ay[1:-1,2:]); ym=hm(ay[1:-1,1:-1],ay[1:-1,:-2]); d=(xp+xm+yp+ym)/h**2
    def A(v):
        z=np.zeros((n+2,n+2)); z[1:-1,1:-1]=v.reshape(n,n); return (d*z[1:-1,1:-1]-xp*z[2:,1:-1]-xm*z[:-2,1:-1]-yp*z[1:-1,2:]-ym*z[1:-1,:-2]).ravel()
    return A,d.ravel(),A(u[1:-1,1:-1].ravel()),u[1:-1,1:-1].ravel()
def cg(p,precondition=False):
    A,d,b,u=p; x=np.zeros_like(b); r=b-A(x); z=r/d if precondition else r.copy(); v=z.copy(); rz=r@z
    for k in range(1,10001):
        a=rz/(v@A(v)); x+=a*v; r-=a*A(v)
        if np.linalg.norm(r)/np.linalg.norm(b)<1e-8: break
        z=r/d if precondition else r; nxt=r@z; v=z+nxt/rz*v; rz=nxt
    return {"iterations":k,"relative_error":float(np.linalg.norm(x-u)/np.linalg.norm(u)),"relative_residual":float(np.linalg.norm(r)/np.linalg.norm(b))}
def bad_wj(p):
    A,d,b,_=p; x=np.zeros_like(b)
    for k in range(250): x+=1.95*(b-A(x))/d
    return bool(np.isfinite(x).all() and np.linalg.norm(b-A(x))/np.linalg.norm(b)<1e-8)
def main():
    OUT.mkdir(exist_ok=True); held=[]
    for case in HELD:
        p=problem(*case); held.append({"case":case,"CG":cg(p),"PCG":cg(p,True)})
    failures=sum(not bad_wj(problem(*case)) for case in DESIGN)
    result={"held_out":held,"bad_weighted_jacobi_design_failures":failures}
    (OUT/"reproduction.json").write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result,indent=2))
if __name__=="__main__": main()
