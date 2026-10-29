import json,sys
from shapely.geometry import Polygon, LineString, Point, MultiPolygon
from shapely.ops import unary_union
B=json.load(open(sys.argv[1])); refs=sys.argv[2].split(',')
def polys(pp):
    out=[]
    for ring in pp:
        r=ring[0] if isinstance(ring[0][0],list) else ring
        out.append(Polygon(r))
    return out
items=[]
for f in B['footprints']:
    for p in f['pads']:
        if not p['poly']: continue
        for L in p['layers']:
            if L.endswith('.Cu'):
                items.append(('pad',f['ref'],p['num'],p['net'],L,unary_union(polys(p['poly']))))
for t in B['tracks']:
    items.append(('trk','','',t['net'],t['layer'],LineString([t['a'],t['b']]).buffer(t['w']/2)))
for v in B['vias']:
    for L in ('F.Cu','B.Cu'):
        items.append(('via','','',v['net'],L,Point(v['x'],v['y']).buffer(v['size']/2)))
for kind,ref,num,net,L,g in items:
    if kind!='pad' or ref not in refs: continue
    best=[]
    for k2,r2,n2,net2,L2,g2 in items:
        if L2!=L or net2==net or (r2==ref and n2==num): continue
        d=g.distance(g2)
        if d<0.3: best.append((round(d,3),k2,r2,n2,net2))
    best.sort()
    print(ref,num,net,L,best[:5])
