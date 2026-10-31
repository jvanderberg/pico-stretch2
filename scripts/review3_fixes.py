#!/usr/bin/env python3
"""Apply the DESIGN_REVIEW_3.md fixes to a copy of the project (base: commit 1d4354a).

    python3 scripts/review3_fixes.py <base_project_dir> <out_project_dir>

- M2: the VREG_LX track beside C10 / C12 narrows from 0.20 to 0.18 mm, so both pads clear it by at least 0.1 mm
  (JLC "Pad to track clearance (1oz) 0.1mm"; it was 0.0925 / 0.0975, passed by the pads' 0.09 mm local clearance).
- m3: C2 (DVDD pin 32, the pin furthest from the regulator) and C5 (pin 10) swap values: 4.7 uF on pin 32, 100 nF on
  pin 10, as RP2350 datasheet 6.1.3 asks. Fields copied from C10 (4.7 uF) and C1 (100 nF), schematic and board.
- M1: every 0.4/0.2 mm via becomes 0.45/0.2 mm, JLCPCB's smallest via with no extra charge on 4+ layers ("0.2mm or
  0.25mm hole size with via diameter less than 0.45mm" costs more, jlcpcb.com/capabilities/pcb-capabilities).
- M1: the Default net class via becomes 0.45/0.2 and the board's minimum via diameter 0.45, so DRC flags a new
  charged via.
- m1: C9's GND via-in-pad moves to the pad centre; at y 101.74 it hung 0.07 mm (0.095 mm at 0.45) past the pad.
  The RUN via by U1.35 and the GPIO47 via by JP4.2 move 0.025 mm off their own pads, to at least 0.1 mm.
- m2: a 0.45 mm hole-to-hole rule from vias to plated holes (JLC POFV), and hole_to_hole raised to an error.

Always rebuilds from the base copy; never patch the output. Uses kicad-skills' kicad_sexpr layer.
"""
import glob
import json
import os
import shutil
import sys

def _version(path):  # .../kicad-skills/<version>/skills/kicad-pcb-workflow/scripts
    return tuple(int(x) if x.isdigit() else 0 for x in path.split(os.sep)[-4].split('.'))


sys.path.insert(0, max(glob.glob(os.path.expanduser(
    '~/.claude/plugins/cache/kicad-skills/kicad-skills/*/skills/kicad-pcb-workflow/scripts')), key=_version))
from kicad_sexpr import Board, Schematic  # noqa: E402

EPS = 1e-3
PRO = 'pico-stretch2.kicad_pro'

base, out = sys.argv[1:3]
if os.path.exists(out):
    shutil.rmtree(out)
shutil.copytree(base, out)

pcb = Board.load(os.path.join(out, 'pico-stretch2.kicad_pcb'))
sch = Schematic.load(os.path.join(out, 'pico-stretch2.kicad_sch'))
MANDATORY = ('Reference', 'Value', 'Footprint', 'Datasheet', 'Description')


def near(a, b):
    return abs(a[0] - b[0]) < EPS and abs(a[1] - b[1]) < EPS


# ------------------------------------------------------------------ M1: 0.4/0.2 -> 0.45/0.2
grown = 0
for v in pcb.items('via'):
    if abs(v.need('size').number(1) - 0.4) < EPS and abs(v.need('drill').number(1) - 0.2) < EPS:
        v.set('size', 0.45)
        grown += 1
assert grown == 87, 'expected 87 vias at 0.4/0.2, found %d' % grown

# ------------------------------------------------------------------ m1: C9 GND via to its pad centre
c9 = [v for v in pcb.items('via') if near((v.need('at').number(1), v.need('at').number(2)), (135.31, 101.74))]
assert len(c9) == 1, 'C9 via: expected 1, found %d' % len(c9)
c9[0].set('at', 135.31, 101.56)


# ------------------------------------------------------------------ m1: tented vias 0.075-0.082 mm from their own pad
def move_via(at, to):
    vs = [v for v in pcb.items('via') if near((v.need('at').number(1), v.need('at').number(2)), at)]
    assert len(vs) == 1, 'via %s: expected 1, found %d' % (at, len(vs))
    vs[0].set('at', *to)
    ends = 0
    for t in pcb.items('segment'):
        for end in ('start', 'end'):
            e = t.need(end)
            if near((e.number(1), e.number(2)), at):
                t.set(end, *to)
                ends += 1
    assert ends, 'via %s: no track ends on it' % (at,)


move_via((146.527646, 100.402354), (146.502646, 100.402354))  # RUN: 0.082 -> 0.107 mm from U1.35
move_via((127.8, 97.45), (127.8, 97.475))                      # GPIO47: 0.075 -> 0.100 mm from JP4.2 (after the grow)

# ------------------------------------------------------------------ M2: VREG_LX 0.20 -> 0.18 mm beside C10 / C12
lx = [t for t in pcb.items('segment') if str(t.need('net')[1]) == '/VREG_LX'
      and near((t.need('start').number(1), t.need('start').number(2)), (137.352456, 99.202456))
      and near((t.need('end').number(1), t.need('end').number(2)), (134.512456, 99.202456))]
assert len(lx) == 1 and abs(lx[0].need('width').number(1) - 0.2) < EPS
lx[0].set('width', 0.18)


# ------------------------------------------------------------------ m3: C2 <-> C5 values (fields from C10 / C1)
def copy_sch_fields(dst_ref, src_ref, keep=('Reference', 'Footprint')):
    dst, src = sch.symbol(dst_ref), sch.symbol(src_ref)
    want = {k: v for k, v in src.fields().items() if k not in keep}
    for p in list(dst.node.nodes('property')):
        name = str(p[1])
        if name not in want and name not in keep and name not in MANDATORY:
            dst.node.remove_node(p)
    for k, v in want.items():
        dst.set_field(k, v)


def copy_pcb_fields(dst_ref, src_ref, keep=('Reference',)):
    dst, src = pcb.footprint(dst_ref), pcb.footprint(src_ref)
    want = {str(p[1]): str(p[2]) for p in src.node.nodes('property')
            if str(p[1]) not in keep and not str(p[1]).startswith('ki_') and str(p[1]) != 'KiLib_Generator'}
    for p in list(dst.node.nodes('property')):
        name = str(p[1])
        if name not in want and name not in keep and name not in MANDATORY and name != 'KiLib_Generator':
            dst.node.remove_node(p)
    for k, v in want.items():
        dst.set_field(k, v)


assert sch.symbol('C2').fields()['Value'] == '100nF' and sch.symbol('C5').fields()['Value'] == '4.7uF'
copy_sch_fields('C2', 'C10')
copy_pcb_fields('C2', 'C10')
copy_sch_fields('C5', 'C1')
copy_pcb_fields('C5', 'C1')

pcb.save()
sch.save()

# ------------------------------------------------------------------ m2: JLC's 0.45 mm from a filled via to a plated hole
dru = os.path.join(out, 'pico-stretch2.kicad_dru')
with open(dru) as f:
    text = f.read()
assert 'via to plated hole' not in text
with open(dru, 'a') as f:
    f.write('(rule "via to plated hole (JLC POFV 0.45 mm)"\n'
            '    (condition "A.Type == \'Via\' && B.Type == \'Pad\'")\n'
            '    (constraint hole_to_hole (min 0.45mm))\n'
            ')\n')

# ------------------------------------------------------------------ M1: net class and minimum via
path = os.path.join(out, PRO)
with open(path) as f:
    pro = json.load(f)
default = [c for c in pro['net_settings']['classes'] if c['name'] == 'Default']
assert len(default) == 1
default[0]['via_diameter'] = 0.45
pro['board']['design_settings']['rules']['min_via_diameter'] = 0.45
pro['board']['design_settings']['rule_severities']['hole_to_hole'] = 'error'   # m2: was warning
with open(path, 'w') as f:
    json.dump(pro, f, indent=2)
    f.write('\n')
print('grew %d vias to 0.45/0.2; moved the C9, RUN and GPIO47 vias; Default via 0.45/0.2, min via 0.45; '
      'via-to-plated-hole 0.45 mm, hole_to_hole an error; VREG_LX 0.18 mm by C10/C12; C2 4.7 uF, C5 100 nF' % grown)
