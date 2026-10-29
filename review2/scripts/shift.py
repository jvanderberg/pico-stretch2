import json,sys
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union
from shapely import affinity
B=json.load(open(sys.argv[1])); ref=sys.argv[2]; dx=float(sys.argv[3]); dy=float(sys.argv[4])
def gp(p): return unary_union([Polygon(r[0] if isinstance(r[0][0],list) else r) for r in p['poly']])
others=[]
for f in B['footprints']:
    for p in f['pads']:
        if 'F.Cu' in p['layers'] and p['poly'] and f['ref']!=ref: others.append((f['ref']+'.'+p['num'],p['net'],gp(p)))
for t in B['tracks']:
    if t['layer']=='F.Cu': others.append(('trk',t['net'],LineString([t['a'],t['b']]).buffer(t['w']/2)))
for v in B['vias']: others.append(('via',v['net'],Point(v['x'],v['y']).buffer(v['size']/2)))
F=[f for f in B['footprints'] if f['ref']==ref][0]
for p in F['pads']:
    g=affinity.translate(gp(p),dx,dy)
    near=sorted((round(g.distance(o[2]),3),o[0],o[1]) for o in others if o[1]!=p['net'] and g.distance(o[2])<0.3)
    print(ref,p['num'],p['net'],near[:4])
