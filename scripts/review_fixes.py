#!/usr/bin/env python3
"""Apply the DESIGN_REVIEW.md fixes (M1, m1, m2, m3, m8, m9, m11, m13) and the DESIGN_REVIEW_2.md M1 pad-gap fix
to a copy of the project. Review-1 m4 (VBUS TVS D4) was tried and removed by decision: see DESIGN_REVIEW_2.md m1.

    python3 scripts/review_fixes.py <base_project_dir> <out_project_dir>

Always rebuilds from the base copy; never patch the output. Uses kicad-skills' kicad_sexpr layer.
"""
import glob
import math
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
EPS = 1e-3

base, out = sys.argv[1:3]
if os.path.exists(out):
    shutil.rmtree(out)
shutil.copytree(base, out)

sch = Schematic.load(os.path.join(out, 'pico-stretch2.kicad_sch'))
pcb = Board.load(os.path.join(out, 'pico-stretch2.kicad_pcb'))

MANDATORY = ('Reference', 'Value', 'Footprint', 'Datasheet', 'Description')


def one(items, what):
    assert len(items) == 1, '%s: expected 1, found %d' % (what, len(items))
    return items[0]


def near(a, b):
    return abs(a[0] - b[0]) < EPS and abs(a[1] - b[1]) < EPS


# ------------------------------------------------------------------ field copies (schematic + board)
def copy_sch_fields(dst_ref, src_ref, keep=('Reference', 'Footprint'), overrides=None):
    dst, src = sch.symbol(dst_ref), sch.symbol(src_ref)
    want = {k: v for k, v in src.fields().items() if k not in keep}
    want.update(overrides or {})
    for p in list(dst.node.nodes('property')):
        name = str(p[1])
        if name not in want and name not in keep and name not in MANDATORY:
            dst.node.remove_node(p)
    for k, v in want.items():
        dst.set_field(k, v)


def copy_pcb_fields(dst_ref, src_ref, keep=('Reference',), overrides=None):
    dst, src = pcb.footprint(dst_ref), pcb.footprint(src_ref)
    want = {str(p[1]): str(p[2]) for p in src.node.nodes('property')
            if str(p[1]) not in keep and not str(p[1]).startswith('ki_') and str(p[1]) != 'KiLib_Generator'}
    want.update(overrides or {})
    for p in list(dst.node.nodes('property')):
        name = str(p[1])
        if name not in want and name not in keep and name not in MANDATORY and name != 'KiLib_Generator':
            dst.node.remove_node(p)
    for k, v in want.items():
        dst.set_field(k, v)


# M1: C9 / C15 -> C1525 (0402), the part C1 already uses
for r in ('C9', 'C15'):
    copy_sch_fields(r, 'C1')
    copy_pcb_fields(r, 'C1')

# m3: R14 10k -> 1k (C11702, as R5)
copy_sch_fields('R14', 'R5')
copy_pcb_fields('R14', 'R5')

# m11: U5 (RM2, hand fitted) DNP, no paste on its pads
u5 = sch.symbol('U5')
u5.node.set('dnp', Sym('yes'))
fu5 = pcb.footprint('U5')
attr = fu5.node.need('attr')
if Sym('dnp') not in attr.args:
    attr.append(Sym('dnp'))
for p in fu5.pads():
    lay = p.need('layers')
    lay[:] = [x for x in lay if x != 'F.Paste']
assert not any('F.Paste' in p.need('layers') for p in fu5.pads())

# ------------------------------------------------------------------ board copper helpers
def find_segments(layer, a, b, net):
    hits = []
    for t in pcb.items('segment'):
        s = (t.need('start').number(1), t.need('start').number(2))
        e = (t.need('end').number(1), t.need('end').number(2))
        if t.get('layer') == layer and str(t.need('net')[1]) == net and \
                ((near(s, a) and near(e, b)) or (near(s, b) and near(e, a))):
            hits.append(t)
    return hits


def remove_segment(layer, a, b, net):
    pcb.tree.remove_node(one(find_segments(layer, a, b, net), 'segment %s %s %s-%s' % (layer, net, a, b)))


def remove_via(at, net):
    vs = [v for v in pcb.items('via') if near((v.need('at').number(1), v.need('at').number(2)), at)
          and str(v.need('net')[1]) == net]
    pcb.tree.remove_node(one(vs, 'via %s %s' % (net, at)))


def pad_abs(fp, num):
    return fp.pad_position(num)


# m8: C40 10 uF 0402 -> 0603 (C19702, as C37), moved 0.2 mm down/left to fit
old = pcb.footprint('C40')
c40_path = old.node.get('path')
assert old.pad_net('1') == 'GND' and old.pad_net('2') == '3V3'
pcb.tree.remove_node(old.node)
remove_via((122.3, 101.39), 'GND')                       # old via-in-pad under the 0402 GND pad
c37 = pcb.footprint('C37')
fields = {str(p[1]): str(p[2]) for p in c37.node.nodes('property')
          if str(p[1]) not in ('Reference', 'Value', 'Footprint') and not str(p[1]).startswith('ki_')
          and str(p[1]) != 'KiLib_Generator'}
# rotated 180: GND pad on the right, where a via clears the B.Cu 3V3_EN / Net-(JP1-A) tracks at x 121.1 / 121.87
c40 = pcb.add_footprint(os.path.join(KICAD_FP, 'Capacitor_SMD.pretty/C_0603_1608Metric.kicad_mod'),
                        'Capacitor_SMD:C_0603_1608Metric', 'C40', '10uF', (122.45, 101.6), angle=180, side='F',
                        path=c40_path, fields=fields, pad_nets={'1': 'GND', '2': '3V3'}, hide_reference=True)
assert near(c40.pad_position('1'), (123.225, 101.6)) and near(c40.pad_position('2'), (121.675, 101.6)), \
    (c40.pad_position('1'), c40.pad_position('2'))
pcb.via((123.225, 101.6), 0.4, 0.2, 'GND')                           # via-in-pad, as the 0402 had
pcb.segment((121.675, 101.6), (122.4, 102.608), 0.3, 'F.Cu', '3V3')  # straight to U3.5 (VOUT)
copy_sch_fields('C40', 'C37', keep=('Reference',))

# m2: D3 in line with USB2_D+ on F.Cu, in C39's old place; C39 moves down between R4 and C37
d3 = pcb.footprint('D3')
assert near(pad_abs(d3, '2'), (119.48, 99.25))
for seg in (((119.495, 99.25), (119.495, 101.285)), ((119.495, 101.285), (119.48, 101.3)),
            ((119.495, 100.3), (120.3, 100.3))):
    remove_segment('B.Cu', seg[0], seg[1], 'USB2_D+')
remove_via((119.495, 99.25), 'USB2_D+')                   # via-in-pad of the old D3 D+ pad
remove_via((120.465, 99.25), 'GND')                       # via-in-pad of the old D3 GND pad


def set_fp_pose(fp, at, angle):
    """Move + rotate a footprint: KiCad stores pad/text angles absolute, so shift them by the rotation delta."""
    delta = angle - fp.angle
    a = fp.node.need('at')
    del a[1:]
    a.extend([at[0], at[1]])
    fa = ((angle + 180) % 360) - 180
    if fa:
        a.append(fa)
    if abs(delta) > EPS:
        for item in list(fp.node.nodes('pad')) + list(fp.node.nodes('property')) + list(fp.node.nodes('fp_text')):
            ia = item.need('at')
            cur = ia.number(3, 0.0)
            na = ((cur + delta) % 360)
            del ia[3:]
            if abs(na) > EPS:
                ia.append(round(na, 6))


set_fp_pose(d3, (118.05, 101.92), 0)
assert near(pad_abs(d3, '1'), (117.55, 101.92)) and near(pad_abs(d3, '2'), (118.55, 101.92)), \
    (pad_abs(d3, '1'), pad_abs(d3, '2'))
assert d3.pad_net('1') == 'GND' and d3.pad_net('2') == 'USB2_D+'
# GND via (117.59, 101.92) of C39's old GND pad now sits in D3's GND pad; D+ pad hangs 0.5 mm under the track
pcb.segment((118.55, 101.43), (118.55, 101.92), 0.16, 'F.Cu', 'USB2_D+')
# TP4 keeps a short B.Cu spur from R3's via
pcb.segment((119.48, 101.3), (120.3, 100.3), 0.2, 'B.Cu', 'USB2_D+')

c39 = pcb.footprint('C39')
assert c39.pad_net('1') == 'VSYS' and c39.pad_net('2') == 'GND'
# review 2 M1: GND pad up, facing D3.1 (GND, same net) instead of VSYS 0.10 mm from it (JLC: 0.15 mm between
# different-net SMD pads); the VSYS pad faces the VSYS pour, which keeps the pour's neck to R11.1 open (moving C39
# down 0.1 mm instead closed it and left R11's VSYS pour piece unconnected)
set_fp_pose(c39, (117.85, 103.08), 90)
assert near(pad_abs(c39, '1'), (117.85, 103.56)) and near(pad_abs(c39, '2'), (117.85, 102.6)), \
    (pad_abs(c39, '1'), pad_abs(c39, '2'))
pcb.segment((117.85, 102.6), (117.59, 101.92), 0.2, 'F.Cu', 'GND')  # to D3.1's GND via-in-pad

# review 2 M1: C13 (1V1) 0.05 mm up, so its 1V1 pad clears U1.50 (3V3) by 0.177 mm instead of 0.127; its GND via
# (142.325, 95.595) stays inside the GND pad, and the 1V1 track from U1.51 is re-ended on the moved pad
c13 = pcb.footprint('C13')
assert near(pad_abs(c13, '1'), (142.325, 95.595)) and near(pad_abs(c13, '2'), (142.325, 96.555))
assert c13.pad_net('1') == 'GND' and c13.pad_net('2') == '1V1'
set_fp_pose(c13, (142.325, 96.025), -90)
assert near(pad_abs(c13, '2'), (142.325, 96.505)), pad_abs(c13, '2')
segs = find_segments('F.Cu', (142.060102, 96.819898), (142.325, 96.555), '1V1')
assert len(segs) in (1, 2), len(segs)          # the board holds this segment twice (duplicate, as found)
for s in segs:
    for end in ('start', 'end'):
        n = s.need(end)
        if near((n.number(1), n.number(2)), (142.325, 96.555)):
            del n[1:]
            n.extend([142.325, 96.505])


# silk of the moved/new small parts collides with neighbours' pads and labels; they keep their F.Fab outline
for ref in ('D3', 'C40'):
    fp = pcb.footprint(ref).node
    for g in [g for g in fp.nodes() if g.head in ('fp_line', 'fp_poly', 'fp_arc', 'fp_circle', 'fp_rect')
              and g.get('layer') == 'F.SilkS']:
        fp.remove_node(g)

# m9: J4 pads 29-36 (next to the RM2): pull the inboard end of the oval in 0.15 mm (ring 0.35 -> 0.2 at the tip)
def clip_oval(fp_node):
    n = 0
    for p in fp_node.nodes('pad'):
        if str(p[1]) in ('29', '30', '31', '32', '33', '34', '35', '36') and str(p[3]) == 'oval':
            sz, off = p.need('size'), p.need('drill').need('offset')
            assert abs(sz.number(1) - 1.7) < EPS and abs(sz.number(2) - 3.3) < EPS and \
                abs(off.number(2) + 0.8) < EPS, (sz, off)
            sz[2] = 3.15
            off[2] = -0.875
            n += 1
    assert n == 8, n


clip_oval(pcb.footprint('J4').node)

# m1: Inner1 cut-out under the whole VREG (L1, LX, VOUT pad and via, CIN/COUT supply pads), Fig. 27,
# stopping >= 0.63 mm (3 x prepreg) short of the USB pair at y 100.56 / 100.865
cut = one([z for z in pcb.items('zone') if z.get('name') == 'VREG_LX cut-out'], 'cut-out zone')
pts = cut.need('polygon').need('pts')
del pts[1:]
for x, y in ((132.5, 97.45), (134.55, 97.45), (134.55, 99.05), (137.3, 99.05), (137.3, 99.38),
             (136.25, 99.38), (136.25, 99.85), (134.75, 99.85), (134.75, 100.15), (132.5, 100.15)):
    pts.append(Node('xy', x, y))

# m13: silkscreen
def text_at(txt, layer, at):
    return one([t for t in pcb.items('gr_text') if t[1] == txt and t.get('layer') == layer
                and near((t.need('at').number(1), t.need('at').number(2)), at)], 'text %s %s' % (txt, layer))


t = text_at('40', 'F.SilkS', (179.884194, 95.25619))
t[1] = '40A0'                                  # narrower font: the 4-char label must end above RM2 pad 8 (y 96.44)
t.need('at')[2] = 96.25
t.need('effects').need('font').set('size', 0.8, 0.55)  # (height width), min height 0.8
t = text_at('40', 'B.SilkS', (178.88, 95.246))
t[1] = '40A0'
t.need('at')[2] = 96.672
text_at('0', 'B.SilkS', (110.3, 109.46)).need('at')[2] = 109.62


def jp_ref(ref, local, angle):
    fp = pcb.footprint(ref)
    f = fp.field('Reference')
    a = f.need('at')
    del a[1:]
    a.extend([local[0], local[1], angle])
    eff = f.need('effects')
    font = eff.need('font')
    font.set('size', 0.8, 0.8)
    font.set('thickness', 0.12)


jp_ref('JP2', (0, 1.675), 180)     # footprint at 180 deg: abs (169.7, 105.0), horizontal
jp_ref('JP3', (0, -1.75), 0)       # abs (163.35, 105.0)

pcb.save()
sch.save()

# keep the project-local library footprints in step with the board
lf = os.path.join(out, 'Castellated.pretty/Castellated_Pad_64.kicad_mod')
t = load(lf)
clip_oval(t)
save(t, lf)
lf = os.path.join(out, 'Custom.pretty/rpi_rmc20452t.kicad_mod')
t = load(lf)
for p in t.nodes('pad'):
    lay = p.need('layers')
    lay[:] = [x for x in lay if x != 'F.Paste']
save(t, lf)

# named courtyard exemptions for the new tight placements (D3 / D3-R2 pair is gone: D3 left R2)
dru = os.path.join(out, 'pico-stretch2.kicad_dru')
txt = open(dru).read()
gone = "|| (A.Reference == 'D3' && B.Reference == 'R2') || (A.Reference == 'R2' && B.Reference == 'D3') "
assert txt.count(gone) == 1
txt = txt.replace(gone, '')
pairs = [('C40', 'C38'), ('C40', 'U3'), ('D3', 'C37'), ('C39', 'C37'), ('D3', 'R3'),
         ('D3', 'R4'), ('D3', 'C39'), ('C39', 'R4')]
add = ''.join(" || (A.Reference == '%s' && B.Reference == '%s') || (A.Reference == '%s' && B.Reference == '%s')"
              % (a, b, b, a) for a, b in pairs)
tail = "(A.Reference == 'R5' && B.Reference == 'Boot1')\")"
assert txt.count(tail) == 1
txt = txt.replace(tail, tail[:-2] + add + '")')
open(dru, 'w').write(txt)
print('ok')
