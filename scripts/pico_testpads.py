#!/usr/bin/env python3
"""Put the USB D-, D+ and GND test pads where the Raspberry Pi Pico 2 has its TP2, TP3 and TP1, so the board can be
reflowed (hot plate) onto a carrier that uses the Pico / Pico 2 SMT footprint.

    python3 scripts/pico_testpads.py <base_project_dir> <out_project_dir>

Base: the output of scripts/review3_fixes.py. Always rebuilds from the base copy; never patch the output.

Pico 2 datasheet 3.2, Figure 5 (carrier footprint, origin at the board's bottom-left corner, USB end up): test
points 1.5 x 1.5 mm with 0.3 mm corner radius; TP1 GND (10.5, 46.5), TP2 USB DM (11.5, 49.8), TP3 USB DP (9.5, 49.8)
(Figure 4 names them). Pico 2 pin 1 hole is at (1.61, 49.63) (Figure 3: 21 mm wide, 17.78 mm rows, 48.26 mm from pin 1
to pin 20). Our J4 pin 1 hole is at (110.8, 110.38) with the rows 17.78 mm apart and 1.61 mm from each edge, the
USB end at -x: Pico (x, y) -> board (110.8 - (y - 49.63), 110.38 - (x - 1.61)).

- TP3 (USB2_D-) and TP4 (USB2_D+) move to the Pico TP2 / TP3 positions on a 1.5 x 1.5 mm R0.3 pad
  (Custom:TestPoint_Pad_1.5x1.5mm_R0.3mm); each gets one new B.Cu stub. Existing tracks are kept, except TP4's
  0.2 mm spur from R3's via, which the new stub replaces.
- TP5 (new, GND) at the Pico TP1 position, joined to In1 / In2 by a via inside its pad, placed off-centre to clear the
  F.Cu VBUS track above it.
- The two GND stitching vias at (110.9, 100.59) and (110.9, 102.58), which sit where the D- / D+ pads go, are removed.
- TP1-TP5 and J4 (copper only) are left out of the BOM and position files, as JP1-JP4 already are.
- The back "D-" / "D+" labels move beside the new pads; a "G" label is added for TP5; JP1's reference moves off TP4.
"""
import glob
import os
import shutil
import sys


def _version(path):  # .../kicad-skills/<version>/skills/kicad-pcb-workflow/scripts
    return tuple(int(x) if x.isdigit() else 0 for x in path.split(os.sep)[-4].split('.'))


sys.path.insert(0, max(glob.glob(os.path.expanduser(
    '~/.claude/plugins/cache/kicad-skills/kicad-skills/*/skills/kicad-pcb-workflow/scripts')), key=_version))
from kicad_sexpr import Board, Node, Schematic, load, save  # noqa: E402
from kicad_sexpr.sexp import Sym  # noqa: E402

KICAD_FP = '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints'
FP_NAME = 'TestPoint_Pad_1.5x1.5mm_R0.3mm'
FP_ID = 'Custom:' + FP_NAME
EPS = 1e-3

PICO_PIN1 = (1.61, 49.63)
J4_PIN1 = (110.8, 110.38)


def pico(x, y):
    return (round(J4_PIN1[0] - (y - PICO_PIN1[1]), 3), round(J4_PIN1[1] - (x - PICO_PIN1[0]), 3))


D_MINUS = pico(11.5, 49.8)   # Pico TP2 -> (110.63, 100.49)
D_PLUS = pico(9.5, 49.8)     # Pico TP3 -> (110.63, 102.49)
GND = pico(10.5, 46.5)       # Pico TP1 -> (113.93, 101.49)
GND_VIA = (round(GND[0] + 0.30, 3), round(GND[1] - 0.45, 3))   # inside the pad, >= 0.5 mm from F.Cu VBUS

base, out = sys.argv[1:3]
if os.path.exists(out):
    shutil.rmtree(out)
shutil.copytree(base, out)


def near(a, b):
    return abs(a[0] - b[0]) < EPS and abs(a[1] - b[1]) < EPS


# ------------------------------------------------------------------ library footprint (Pico test-point pad)
fp = load(os.path.join(KICAD_FP, 'TestPoint.pretty', 'TestPoint_Pad_1.5x1.5mm.kicad_mod'))
fp[1] = FP_NAME
fp.set('descr', 'SMD test point pad, 1.5 x 1.5 mm, 0.3 mm corner radius, as the Raspberry Pi Pico / Pico 2 '
                'SMT footprint (Pico 2 datasheet 3.2, Figure 5)')
fp.set('tags', 'test point SMD pad Pico castellated module')
for p in fp.nodes('property'):
    if p[1] == 'Value':
        p[2] = FP_NAME
for ln in list(fp.nodes('fp_line')):
    if ln.need('layer')[1] == 'F.SilkS':
        fp.remove_node(ln)                           # pads 2 mm apart: no silk box
    elif ln.need('layer')[1] == 'F.CrtYd':
        for end in ('start', 'end'):
            e = ln.need(end)
            e[1], e[2] = (0.95 if e.number(1) > 0 else -0.95), (0.95 if e.number(2) > 0 else -0.95)
pad = fp.need('pad')
pad[3] = Sym('roundrect')
pad.set('roundrect_rratio', 0.2)                     # 0.3 mm on 1.5 mm
lib_path = os.path.join(out, 'Custom.pretty', FP_NAME + '.kicad_mod')
save(fp, lib_path)

sch = Schematic.load(os.path.join(out, 'pico-stretch2.kicad_sch'))
pcb = Board.load(os.path.join(out, 'pico-stretch2.kicad_pcb'))

# ------------------------------------------------------------------ schematic: footprints, TP5 on GND
for ref in ('TP3', 'TP4'):
    sch.symbol(ref).set_field('Footprint', FP_ID)
tp = sch.symbol('TP3')
tp5 = sch.add_symbol('Connector:TestPoint', 'TP5', 'TestPoint', (298.45, 236.22), footprint=FP_ID,
                     datasheet=tp.field_value('Datasheet'), description=tp.field_value('Description'))
for name in ('Reference', 'Value'):
    src = tp.field(name).need('at')
    tp5.set_field(name, at=(src.number(1) + 12.7, src.number(2)))
sch.power('power:GND', (298.45, 241.3))
sch.wire((298.45, 236.22), (298.45, 241.3))


# ------------------------------------------------------------------ board
def fields_of(ref):
    f = pcb.footprint(ref)
    return {str(p[1]): str(p[2]) for p in f.node.nodes('property')
            if str(p[1]) not in ('Reference', 'Value', 'Footprint')}, f


def replace_tp(ref, at, net):
    fields, old = fields_of(ref)
    path = str(old.node.need('path')[1])          # the schematic link; the footprint's own uuid is new
    pcb.tree.remove_node(old.node)
    new = pcb.add_footprint(lib_path, FP_ID, ref, 'TestPoint', at, angle=180, side='B', fields=fields,
                            pad_nets={'1': net}, path=path, sheetname='/', sheetfile='pico-stretch2.kicad_sch',
                            hide_reference=True)
    return new


old_tp3 = pcb.footprint('TP3').at
old_tp4 = pcb.footprint('TP4').at
assert near(old_tp3, (116.45, 101.0)) and near(old_tp4, (120.3, 100.3)), (old_tp3, old_tp4)
replace_tp('TP3', D_MINUS, 'USB2_D-')
replace_tp('TP4', D_PLUS, 'USB2_D+')
fields5, _ = fields_of('TP3')
pcb.add_footprint(lib_path, FP_ID, 'TP5', 'TestPoint', GND, angle=180, side='B', fields=fields5,
                  pad_nets={'1': 'GND'}, path='/' + tp5.uuid, sheetname='/', sheetfile='pico-stretch2.kicad_sch',
                  hide_reference=True)


def remove_via(at, net):
    vs = [v for v in pcb.items('via') if near((v.need('at').number(1), v.need('at').number(2)), at)
          and str(v.need('net')[1]) == net]
    assert len(vs) == 1, 'via %s %s: %d' % (net, at, len(vs))
    pcb.tree.remove_node(vs[0])


def segments(net, layer):
    return [t for t in pcb.items('segment') if str(t.need('net')[1]) == net and t.get('layer') == layer]


def ends(t):
    return ((t.need('start').number(1), t.need('start').number(2)), (t.need('end').number(1), t.need('end').number(2)))


remove_via((110.9, 100.59), 'GND')
remove_via((110.9, 102.58), 'GND')
pcb.via(GND_VIA, 0.45, 0.2, 'GND')                  # TP5 to In1 / In2, filled and capped like every via-in-pad

# D-: the old TP3 pad centre (116.45, 101.0) is the end of the stub from D2's via; extend it to the new pad
d_minus = [t for t in segments('USB2_D-', 'B.Cu') if any(near(e, old_tp3) for e in ends(t))]
assert len(d_minus) == 1, len(d_minus)
w = d_minus[0].need('width').number(1)
pcb.track([old_tp3, (115.9, 100.45), (111.4, 100.45), D_MINUS], w, 'B.Cu', 'USB2_D-')   # above TP5 (pad top 100.74)

# D+: TP4's spur from R3's via-in-pad (119.48, 101.3) is replaced by a stub that passes under the VSYS via at
# (119.33, 102.12) and runs along y 102.75 to the new pad
R3_VIA = (119.48, 101.3)
spur = [t for t in segments('USB2_D+', 'B.Cu') if any(near(e, old_tp4) for e in ends(t))]
assert len(spur) == 1 and any(near(e, R3_VIA) for e in ends(spur[0])), spur
w = spur[0].need('width').number(1)
pcb.tree.remove_node(spur[0])
pcb.track([R3_VIA, (119.9, 101.72), (119.9, 102.75), (111.0, 102.75), D_PLUS], w, 'B.Cu', 'USB2_D+')

# ------------------------------------------------------------------ back labels
def place_label(t, x, y):
    t.need('at')[1], t.need('at')[2] = x, y
    t.need('effects').set('justify', Sym('mirror'))   # centred: the D pads and TP5 leave a 1.8 mm gap at x 111.4-113.2


for t in pcb.items('gr_text'):
    if t.get('layer') == 'B.SilkS' and str(t[1]) in ('D-', 'D+'):
        place_label(t, 112.28, D_MINUS[1] if str(t[1]) == 'D-' else D_PLUS[1])
lbl = [t for t in pcb.items('gr_text') if t.get('layer') == 'B.SilkS' and str(t[1]) == 'D-'][0].deepcopy()
lbl[1] = 'G'
place_label(lbl, 115.35, GND[1])
lbl.remove_all('uuid')
lbl.insert(len(lbl) - 1, Node('uuid', ''))
pcb.add(lbl)

# JP1's reference sat at (111.55, 103.2), on the new TP4 pad: move it clear, still beside JP1
jp1 = pcb.footprint('JP1')
ref = jp1.field('Reference').need('at')
assert near(jp1.at, (111.6, 107.8)) and abs(jp1.angle - 180) < EPS
ref[1], ref[2] = -1.35, 3.1        # local to JP1 (rotated 180): (112.95, 104.7) on the board

# ------------------------------------------------------------------ bare copper out of the BOM and position files
# Test pads and the castellated edge (J4) are copper only: nothing for JLC to place, and TP1-TP5 on the back would
# otherwise appear as bottom-side placements in the CPL. Same treatment as the solder jumpers JP1-JP4.
for ref in ('TP1', 'TP2', 'TP3', 'TP4', 'TP5', 'J4'):
    n = sch.symbol(ref).node
    n.set('in_bom', False)
    n.set('in_pos_files', False)
    f = pcb.footprint(ref).node
    kind = [a for a in (f.find('attr') or Node('attr')).args if str(a) in ('smd', 'through_hole')]
    attr = Node('attr', *kind, Sym('exclude_from_pos_files'), Sym('exclude_from_bom'))
    if f.find('attr') is not None:
        f.remove_all('attr')
    f.insert_before('duplicate_pad_numbers_are_jumpers', attr) if f.find('duplicate_pad_numbers_are_jumpers') is not None \
        else f.insert_before('fp_line', attr)
castellated = os.path.join(out, 'Castellated.pretty', 'Castellated_Pad_64.kicad_mod')
cp = load(castellated)
old_attr = cp.need('attr')
cp.insert(cp.index(old_attr), Node('attr', Sym('smd'), Sym('exclude_from_pos_files'), Sym('exclude_from_bom')))
cp.remove_node(old_attr)                             # same place in the file as the old (attr smd)
save(cp, castellated)

pcb.save()
sch.save()
print('TP3 D- %s, TP4 D+ %s, TP5 GND %s (via %s); GND vias at (110.9, 100.59) / (110.9, 102.58) removed'
      % (D_MINUS, D_PLUS, GND, GND_VIA))
