import json,sys
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
for f in sys.argv[1:]:
    B=json.load(open(f))
    fills=[]
    for z in B['zones']:
        if z['net']=='GND' and 'In1.Cu' in (z['filled'] or {}):
            for ring in z['filled']['In1.Cu']: fills.append(Polygon(ring[0], ring[1:]))
    g=unary_union(fills)
    FP={x['ref']:x for x in B['footprints']}
    out=[]
    for ref,num in (('L1','1'),('L1','2'),('C10','1'),('C10','2'),('C12','1'),('C12','2'),('C11','1'),('C11','2'),('U1','63'),('U1','64'),('U1','65'),('U1','62')):
        for p in FP[ref]['pads']:
            if p['num']==num and 'F.Cu' in p['layers']:
                pg=unary_union([Polygon(r[0] if isinstance(r[0][0],list) else r) for r in p['poly']])
                out.append('%s.%s %s %.0f%%'%(ref,num,p['net'],100*pg.intersection(g).area/pg.area))
    for net in ('/VREG_LX','1V1'):
        for z in B['zones']:
            if z['net']==net and 'F.Cu' in (z['filled'] or {}):
                pz=unary_union([Polygon(r[0],r[1:]) for r in z['filled']['F.Cu']])
                # only the pour near the regulator
                from shapely.geometry import box
                pz=pz.intersection(box(131,96,138.5,101.5))
                if pz.area>0: out.append('%s pour %.1f mm2: %.0f%% over In1 GND'%(net,pz.area,100*pz.intersection(g).area/pz.area))
    for v in B['vias']:
        if v['net']=='1V1' and abs(v['x']-134.49)<0.1: out.append('1V1 via (134.49,100.18) dist to In1 GND %.2f'%(Point(v['x'],v['y']).buffer(v['size']/2).distance(g)))
    print(f.split('/')[-2],'; '.join(out))
