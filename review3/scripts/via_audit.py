"""Via audit from a pack's board.json: size classes, via-in-pad overhang, copper gaps per layer,
hole-to-hole spacing and inner-plane antipads.  usage: via_audit.py board.json [grow_to_mm]"""
import json, sys, collections
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
from shapely.ops import unary_union

d = json.load(open(sys.argv[1]))
grow = float(sys.argv[2]) if len(sys.argv) > 2 else None
CU = d["layers"]

def mpoly(p):
    return MultiPolygon([Polygon(r[0], r[1:]) for r in p]) if p else None

pads = []
for fp in d["footprints"]:
    for p in fp["pads"]:
        g = mpoly(p["poly"])
        if g is None: continue
        pads.append(dict(ref=fp["ref"], num=p["num"], net=p["net"], layers=p["layers"], g=g.buffer(0), drill=p.get("drill") or 0, x=p["x"], y=p["y"]))
tracks = [dict(net=t["net"], layer=t["layer"], g=LineString([t["a"], t["b"]]).buffer(t["w"] / 2)) for t in d["tracks"] if t["a"] != t["b"]]
fills = collections.defaultdict(list)
for z in d["zones"]:
    if z.get("keepout"): continue
    for lay, f in z["filled"].items():
        g = mpoly(f)
        if g is not None: fills[lay].append((z["net"], g.buffer(0)))
vias = d["vias"]

def vsize(v):
    return grow if (grow and v["size"] < grow) else v["size"]

print(f"{len(vias)} vias; classes:", dict(collections.Counter((v['size'], v['drill']) for v in vias)))
rows = []
for i, v in enumerate(vias):
    c = Point(v["x"], v["y"]); r = vsize(v) / 2; ring = c.buffer(r, 64); hole = c.buffer(v["drill"] / 2, 64)
    inpad = [p for p in pads if p["net"] == v["net"] and any(l in p["layers"] for l in ("F.Cu", "B.Cu")) and p["g"].intersects(c.buffer(v['drill']/2))]
    over = min(max(0.0, r - max(0.0, p["g"].exterior.distance(c) if hasattr(p["g"], "exterior") else p["g"].boundary.distance(c))) for p in inpad) if inpad else None
    # nearest other-net copper on the outer layers (pads, tracks, other vias, fills)
    best = (9, "")
    for lay in ("F.Cu", "B.Cu"):
        for p in pads:
            if p["net"] != v["net"] and lay in p["layers"]:
                dd = ring.distance(p["g"])
                if dd < best[0]: best = (dd, f"{lay} pad {p['ref']}.{p['num']} {p['net']}")
        for t in tracks:
            if t["net"] != v["net"] and t["layer"] == lay:
                dd = ring.distance(t["g"])
                if dd < best[0]: best = (dd, f"{lay} track {t['net']}")
        for net, g in fills[lay]:
            if net != v["net"]:
                dd = ring.distance(g)
                if dd < best[0]: best = (dd, f"{lay} fill {net}")
    for j, w in enumerate(vias):
        if j != i and w["net"] != v["net"]:
            dd = ring.distance(Point(w["x"], w["y"]).buffer(vsize(w) / 2, 64))
            if dd < best[0]: best = (dd, f"via {w['net']} ({w['x']:.2f},{w['y']:.2f})")
    # hole to hole (any net) and hole to other-net PTH drill
    h2h = min(hole.distance(Point(w["x"], w["y"]).buffer(w["drill"] / 2, 64)) for j, w in enumerate(vias) if j != i)
    h2h = min([h2h] + [hole.distance(Point(p["x"], p["y"]).buffer(p["drill"] / 2, 64)) for p in pads if p["drill"]])
    # inner layers: hole edge to nearest other-net copper (plane antipad), and whether the via meets its own plane
    inner = {}
    for lay in ("In1.Cu", "In2.Cu"):
        other = [g for net, g in fills[lay] if net != v["net"]]
        same = [g for net, g in fills[lay] if net == v["net"]]
        inner[lay] = (min((hole.distance(g) for g in other), default=9), any(g.intersects(ring) for g in same))
    rows.append(dict(i=i, x=v["x"], y=v["y"], net=v["net"], size=v["size"], drill=v["drill"], inpad=[f"{p['ref']}.{p['num']}" for p in inpad],
                     overhang=over, gap=best[0], gapto=best[1], h2h=h2h, inner=inner))

def show(title, sel, key):
    print(f"\n## {title}: {len(sel)}")
    for r in sorted(sel, key=key)[:40]:
        print(f"  {r['net']:<18} ({r['x']:.3f},{r['y']:.3f}) {r['size']}/{r['drill']} inpad={','.join(r['inpad']) or '-'} "
              f"overhang={r['overhang'] if r['overhang'] is None else round(r['overhang'],3)} gap={r['gap']:.3f} [{r['gapto']}] h2h={r['h2h']:.3f} "
              f"In1={r['inner']['In1.Cu'][0]:.3f}/{'on' if r['inner']['In1.Cu'][1] else 'off'} In2={r['inner']['In2.Cu'][0]:.3f}/{'on' if r['inner']['In2.Cu'][1] else 'off'}")

show("vias in pads", [r for r in rows if r["inpad"]], lambda r: -(r["overhang"] or 0))
show("tightest outer-layer copper gaps", [r for r in rows if r["gap"] < 0.15], lambda r: r["gap"])
show("hole-to-hole < 0.3", [r for r in rows if r["h2h"] < 0.3], lambda r: r["h2h"])
show("non-GND inner antipad (hole to plane) < 0.25", [r for r in rows if r["net"] != "GND" and min(r["inner"][l][0] for l in r["inner"]) < 0.25], lambda r: min(r["inner"][l][0] for l in r["inner"]))
show("GND vias not meeting a plane", [r for r in rows if r["net"] == "GND" and not any(r["inner"][l][1] for l in r["inner"])], lambda r: r["x"])
print("\nby class and net:")
c = collections.defaultdict(collections.Counter)
for r in rows: c[(r["size"], r["drill"])][r["net"]] += 1
for k, v in sorted(c.items()): print(" ", k, sum(v.values()), dict(v.most_common()))
