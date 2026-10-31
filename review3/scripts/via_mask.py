"""Gap from each via's copper to the nearest pad it does not sit in (any net; mask is 1:1, so a pad edge is a mask
opening edge).  usage: via_mask.py board.json [limit_mm]"""
import json, sys
from shapely.geometry import Point, MultiPolygon, Polygon
d = json.load(open(sys.argv[1])); lim = float(sys.argv[2]) if len(sys.argv) > 2 else 0.09
pads = []
for fp in d["footprints"]:
    for p in fp["pads"]:
        if p["poly"]:
            pads.append((fp["ref"], p["num"], p["net"], p["layers"], MultiPolygon([Polygon(r[0], r[1:]) for r in p["poly"]]).buffer(0)))
out = []
for v in d["vias"]:
    c = Point(v["x"], v["y"]); ring = c.buffer(v["size"] / 2, 64)
    for ref, num, net, layers, g in pads:
        if not any(l in layers for l in v["layers"]): continue
        if g.contains(c):
            o = ring.difference(g).area
            if o > 1e-5: out.append((-1, f"via {v['net']} {v['size']} ({v['x']:.3f},{v['y']:.3f}) overhangs {ref}.{num} ({net}) by {100*o/ring.area:.0f} % of its copper"))
            continue
        dd = ring.distance(g)
        if dd < lim: out.append((dd, f"via {v['net']} {v['size']} ({v['x']:.3f},{v['y']:.3f}) {dd:.3f} mm from {ref}.{num} ({net}){' SAME NET' if net == v['net'] else ''}{' TOUCHES' if dd == 0 else ''}"))
for _, s in sorted(out): print(s)
