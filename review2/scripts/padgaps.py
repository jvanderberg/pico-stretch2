import json,sys
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree
B=json.load(open(sys.argv[1]))
pads=[]
for f in B['footprints']:
    for p in f['pads']:
        if not p['poly'] or p['th']: continue
        g=unary_union([Polygon(r[0] if isinstance(r[0][0],list) else r) for r in p['poly']])
        for L in ('F.Cu','B.Cu'):
            if L in p['layers']: pads.append((f['ref'],p['num'],p['net'],L,g))
out=[]
for i,a in enumerate(pads):
    for b in pads[i+1:]:
        if a[0]==b[0] or a[3]!=b[3] or a[2]==b[2]: continue
        d=a[4].distance(b[4])
        if d<0.2: out.append((round(d,3),a[0]+'.'+a[1],a[2],b[0]+'.'+b[1],b[2]))
for o in sorted(out): print(o)
