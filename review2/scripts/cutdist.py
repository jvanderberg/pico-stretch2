import json,sys
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union, nearest_points
for f in sys.argv[1:]:
    B=json.load(open(f))
    cut=[z for z in B['zones'] if z['name']=='VREG_LX cut-out'][0]
    poly=Polygon(cut['outline'][0][0]); print(f.split('/')[-2],'cut-out bounds',poly.bounds)
    for net in ('USB_D+','USB_D-','1V1','/VREG_LX'):
        segs=[t for t in B['tracks'] if t['net']==net and t['layer']=='F.Cu']
        if not segs: continue
        g=unary_union([LineString([t['a'],t['b']]).buffer(t['w']/2) for t in segs])
        p=nearest_points(g,poly)
        print('  ',net,'track edge to cut-out %.3f'%g.distance(poly),[round(c,2) for c in p[0].coords[0]])
    for t in B['tracks']:
        if t['net'] in('USB_D-','USB_D+') and 131<min(t['a'][0],t['b'][0])<138: print('   ',t['net'],t['a'],t['b'],t['w'])
