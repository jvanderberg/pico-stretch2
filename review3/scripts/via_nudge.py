"""Score candidate positions for a via: min gap to other-net copper on F/B (pads, tracks, other vias; zone fills
excluded because they refill) and min gap to same-net pads it is not in.  usage: via_nudge.py board.json"""
import json, sys, itertools
from shapely.geometry import Point, MultiPolygon, Polygon, LineString
d = json.load(open(sys.argv[1]))
pads = [(fp["ref"] + "." + p["num"], p["net"], p["layers"], MultiPolygon([Polygon(r[0], r[1:]) for r in p["poly"]]).buffer(0))
        for fp in d["footprints"] for p in fp["pads"] if p["poly"]]
tr = [(t["net"], t["layer"], LineString([t["a"], t["b"]]).buffer(t["w"] / 2)) for t in d["tracks"] if t["a"] != t["b"]]
def score(v, x, y):
    ring = Point(x, y).buffer(v["size"] / 2, 64); other = (9, ""); same = (9, "")
    for name, net, layers, g in pads:
        if not ({"F.Cu", "B.Cu"} & set(layers)): continue
        dd = ring.distance(g)
        if net != v["net"]: other = min(other, (dd, name))
        elif not g.contains(Point(x, y)): same = min(same, (dd, name))
    for net, lay, g in tr:
        if net != v["net"] and lay in ("F.Cu", "B.Cu"): other = min(other, (ring.distance(g), "track " + net + " " + lay))
    for w in d["vias"]:
        if w is not v and w["net"] != v["net"]: other = min(other, (ring.distance(Point(w["x"], w["y"]).buffer(w["size"] / 2, 64)), "via " + w["net"]))
    return other, same
for vx, vy in [(147.870, 101.6025), (147.755, 100.007), (134.493, 100.1776), (146.528, 100.4024), (127.800, 97.450)]:
    v = min(d["vias"], key=lambda w: (w["x"] - vx) ** 2 + (w["y"] - vy) ** 2)
    o, s = score(v, v["x"], v["y"])
    print(f"== {v['net']} ({v['x']:.3f},{v['y']:.3f}) now: other {o[0]:.3f} [{o[1]}], same-net pad {s[0]:.3f} [{s[1]}]")
    best = []
    for dx, dy in itertools.product([i * 0.025 for i in range(-6, 7)], repeat=2):
        o, s = score(v, v["x"] + dx, v["y"] + dy)
        if o[0] >= 0.1 and s[0] >= 0.09: best.append((abs(dx) + abs(dy), dx, dy, o, s))
    for b in sorted(best)[:3]: print(f"   move ({b[1]:+.3f},{b[2]:+.3f}): other {b[3][0]:.3f} [{b[3][1]}], same-net pad {b[4][0]:.3f} [{b[4][1]}]")
    if not best: print("   no position within 0.15 mm meets both")
