import json,sys
from shapely.geometry import Polygon, LineString, box
from shapely.ops import unary_union
for f in sys.argv[1:]:
    B=json.load(open(f))
    fills=[]
    for z in B['zones']:
        if z['net']=='GND' and 'In1.Cu' in (z['filled'] or {}):
            for ring in z['filled']['In1.Cu']:
                fills.append(Polygon(ring[0], ring[1:]))
    g=unary_union(fills)
    W=box(126,97,140,102)
    void=W.difference(g)
    for net in ('USB_D+','USB_D-'):
        segs=[t for t in B['tracks'] if t['net']==net and t['layer']=='F.Cu']
        line=unary_union([LineString([t['a'],t['b']]).buffer(t['w']/2) for t in segs]).intersection(W)
        d=line.distance(void); over=line.intersection(void).area
        # nearest point
        from shapely.ops import nearest_points
        p=nearest_points(line,void)
        print(f.split('/')[-2], net, 'edge-to-void %.3f mm'%d, 'at', [round(c,2) for c in p[0].coords[0]], 'overlap area %.4f'%over)
