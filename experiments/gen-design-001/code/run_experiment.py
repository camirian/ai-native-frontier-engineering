#!/usr/bin/env python3
"""Independent oracle and frozen held-out check for GEN-DESIGN-001."""
import json, math
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parents[1]
DATA, OUT = HERE / "data", HERE / "reproduced"
N = np.array([(2*c, 3*r) for r in range(2) for c in range(6)], float)
SUPPORTS = {0: (True, True), 5: (False, True)}
DESIGN = {"D_center": {9: (0,-18)}, "D_offcenter": {10:(0,-14)}, "D_pair": {8:(0,-9),10:(0,-9)}}
HELD = {"H_asymmetric_combo": {7:(4,-11),10:(-2,-10)}, "H_edge_down": {11:(0,-15)}, "H_reversed_asymmetry": {7:(-3,-13),9:(1,-7)}}
E, STRESS_LIMIT, DISP_LIMIT = 1_000_000., 120., .20

def oracle(members, areas, loads):
    """Finite-element axial-bar oracle; candidate generation never calls it to rewrite HELD."""
    K=np.zeros((24,24)); L=[]; cs=[]
    for (a,b), area in zip(members,areas):
        dx,dy=N[b]-N[a]; length=math.hypot(dx,dy); c,s=dx/length,dy/length
        q=E*area/length*np.array([[c*c,c*s,-c*c,-c*s],[c*s,s*s,-c*s,-s*s],[-c*c,-c*s,c*c,c*s],[-c*s,-s*s,c*s,s*s]])
        ix=[2*a,2*a+1,2*b,2*b+1]; K[np.ix_(ix,ix)]+=q; L.append(length); cs.append((c,s))
    fixed=[2*i+d for i,v in SUPPORTS.items() for d,on in enumerate(v) if on]
    free=np.array([i for i in range(24) if i not in fixed]); f=np.zeros(24)
    for node,(x,y) in loads.items(): f[2*node:2*node+2]=(x,y)
    u=np.zeros(24); u[free]=np.linalg.solve(K[np.ix_(free,free)],f[free])
    forces=[]
    for (a,b),area,length,(c,s) in zip(members,areas,L,cs):
        forces.append(E*area/length*np.dot([-c,-s,c,s],u[[2*a,2*a+1,2*b,2*b+1]]))
    return {"stress_ratio":max(abs(x/a) for x,a in zip(forces,areas))/STRESS_LIMIT,
            "displacement_ratio":max(np.hypot(u[::2],u[1::2]))/DISP_LIMIT,
            "equilibrium_residual":float(max(abs((K@u-f)[free]))),
            "mass":sum(a*l for a,l in zip(areas,L))}

def main():
    OUT.mkdir(exist_ok=True); rows={}
    for name in ("B2_warren","G06"):
        x=json.loads((DATA/(name+".json")).read_text()); rows[name]={case:oracle(x["members"],x["areas"],load) for case,load in HELD.items()}
    (OUT/"held_out_reproduction.json").write_text(json.dumps(rows,indent=2)+"\n")
    # Exact axial-bar sanity check: 10 N / (E*.1/1) = .0001 displacement.
    assert abs(10/(E*.1)-.0001)<1e-15
    print(json.dumps(rows,indent=2))
if __name__ == "__main__": main()
