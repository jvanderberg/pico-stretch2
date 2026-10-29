import json,sys
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
for f in sys.argv[1:]:
    B=json.load(open(f))
    FP={x['ref']:x for x in B['footprints']}
    def g(p): return unary_union([Polygon(r[0] if isinstance(r[0][0],list) else r) for r in p['poly']])
    res=[]
    for p in FP['J4']['pads']:
        if p['num'] not in [str(i) for i in range(27,40)] : continue
        for q in FP['U5']['pads']:
            if 'F.Cu' in q['layers'] and 'F.Cu' in p['layers']:
                d=g(p).distance(g(q))
                if d<0.6: res.append((round(d,3),'J4.'+p['num'],p['net'],'U5.'+q['num'],q['net']))
    print(f.split('/')[-3]); [print(' ',r) for r in sorted(res)]
