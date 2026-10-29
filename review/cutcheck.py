# Connectivity of every net on the board with everything right of XCUT removed (the Pico-size cut-down board).
# usage: PYTHONPATH=<kicad-board-review>/scripts python3 cutcheck.py PACK_DIR   (a pack built with boarddump_patched.py; XCUT=160.33 to override the cut x)
from common import *
XCUT=float(os.environ.get('XCUT','159.83'))
CL=box(0,0,XCUT,500)
def comps(net, clip):
    nodes=[]  # (layer, geom)
    for L in LAYERS:
        g=copper(net,L)
        if clip: g=g.intersection(CL)
        if g.is_empty: continue
        parts=list(g.geoms) if hasattr(g,'geoms') else [g]
        for p in parts: nodes.append((L,p))
    n=len(nodes); par=list(range(n))
    def f(i):
        while par[i]!=i: par[i]=par[par[i]]; i=par[i]
        return i
    # inter-layer joins: vias and TH pads
    joins=[Point(v['x'],v['y']) for v in B['vias'] if v['net']==net]
    joins+=[Point(p['x'],p['y']) for fp in B['footprints'] for p in fp['pads'] if p['net']==net and p['th']]
    if clip: joins=[j for j in joins if j.x<XCUT]
    for j in joins:
        hit=[i for i,(L,g) in enumerate(nodes) if g.buffer(0.01).contains(j)]
        for a in hit[1:]: par[f(a)]=f(hit[0])
    # pads
    padmap=collections.defaultdict(list)
    for fp in B['footprints']:
        for p in fp['pads']:
            if p['net']!=net: continue
            if clip and p['x']>=XCUT: continue
            pt=Point(p['x'],p['y'])
            for i,(L,g) in enumerate(nodes):
                if L in p['layers'] and g.buffer(0.01).contains(pt):
                    padmap[f(i)].append(f"{fp['ref']}.{p['num']}"); break
            else:
                padmap['ISOLATED'].append(f"{fp['ref']}.{p['num']}")
    out=collections.defaultdict(set)
    for k,v in padmap.items():
        out[f(k) if k!='ISOLATED' else k]|=set(v)
    return [sorted(v) for v in out.values()]
nets=sorted({p['net'] for fp in B['footprints'] for p in fp['pads'] if p['net'] and not p['net'].startswith('unconnected')})
for net in nets:
    full=comps(net,False); cut=comps(net,True)
    if len(cut)>1 or len(full)>1:
        print(net, '\n   full:', full if len(full)>1 else 'connected', '\n   cut :', cut)
# copper crossing the cut line
print('\nCopper crossing x=%.2f:'%XCUT)
line=LineString([(XCUT,0),(XCUT,500)])
for L in LAYERS:
    nets=collections.Counter()
    for t in B['tracks']:
        if t['layer']==L and track_geom(t).intersects(line): nets[t['net']]+=1
    zn=[z['net'] for z in B['zones'] if not z['keepout'] and L in z['filled'] and unary_union(polys(z['filled'][L])).intersects(line)]
    print(L,'tracks:',dict(nets),'zones:',zn)
