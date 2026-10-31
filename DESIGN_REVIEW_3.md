# Pico Stretch 2: design review 3 (full board)

Board: `/Users/joshv/git/pico-stretch2`, commit 1d4354a (review 2 fixes applied, D4 removed), plus the fixes below in
the working tree. RP2350B dev board, 82.4 x 21.3 mm, 4 layers (JLC04161H-7628, 1.6 mm), KiCad 10.0.1, JLCPCB
economic PCBA. Reviewed 2026-10-31 with kicad-skills c16f0b8 and JLCImport 1.7.0. The owner suspected via-size
problems; those are M1 and m1-m2, but every checklist area was reviewed.

## Method

- **Analysis packs:** `review3/pack/` (the committed board) and `review3/pack_after/` (the board with every fix below),
  built by kicad-board-review's `make_pack.sh` with review 2's config, zones refilled, inner copper 15.2 um.
- **Board checks:** `check.sh` (DRC with refill, parity, ERC, `board_lint`, `nc_audit`, `partfields`) against a
  `git archive HEAD` baseline; `board_diff` for change scope; renders (`review3/renders/`), looked at.
- **Via audit:** `review3/scripts/via_audit.py` (size classes, via-in-pad overhang, copper gaps, hole-to-hole, inner
  antipads), `via_mask.py` (via copper to the edge of every pad it is not in) and `via_nudge.py` (scores positions).
- **Assembly and stock:** `jlcimport-cli production --check-only` on a copy (JLC stock, part types, placements solved
  against JLC's footprints), plus `jlcimport-cli search` for alternatives, 2026-10-31.
- **Datasheets read:** RP2350 datasheet (6.1.3 core supply), RP2350 hardware design guide (QSPI_SS pull-up, VREG
  components, crystal), ME6217 (pinout, abs max, electrical characteristics), plus review 2's set for the rest.
- **Fab rules:** JLCPCB capabilities page and its POFV (via-in-pad) page, fetched 2026-10-31.
- **Heat:** the pack's solve at the closed-box h range, and re-solved at the bare-board range (9 / 12 / 16 W/m^2K).
- **Adversarial passes:** a via-focused reviewer (`review3/pack/adversarial_review.md`) and a full-board reviewer
  (`review3/full_adversarial_review.md`). Each claim was re-measured before it was kept (see "Adversarial passes").
- **Fixes:** `scripts/review3_fixes.py` rebuilds all of them from the base copy; applied to the project and
  re-checked there.

---

## Blockers

### B1. X1, the 12 MHz crystal (ABM8-272-T3, C20625731), is out of stock

**Owner decision (2026-10-31): a momentary supply issue, not a design item. Closed; no change.**

- **Evidence:** `jlcimport-cli production --check-only`: "error X1 Out of stock"; `jlcimport-cli search C20625731`:
  stock N/A (global). Review 2 found 845 on 2026-10-29. No other LCSC listing of ABM8-272-T3 has stock.
- **Consequence:** JLC will not place X1. Without the crystal the RP2350 has no USB, so the boards arrive unable to
  take firmware over USB until a crystal is hand-fitted.
- **Why not just substitute:** the RP2350 hardware design guide (4.1): "We highly recommend using this crystal along
  with the accompanying circuitry"; "Pico 2 has been specifically tuned for the ABM8-272-T3" (10 pF, max ESR 50 ohm,
  with the 15 pF caps and 1 kohm damping resistor R28); "Any changes to crystal parameters risk instability"; "Even if
  you use a crystal with similar specifications, you will need to test the circuit over a range of temperatures".
- **Fix (owner's choice):**
  - (a) **Pre-order or consign ABM8-272-T3**, as the README already does for L1. Keeps the tuned circuit. Preferred.
  - (b) A substitute on the same 3225 land, tested over temperature. In-stock 10 pF parts: YXC X322512MMB4SI (C50430,
    13,346, but ESR 80 ohm, above the 50 ohm the circuit was tuned for), HELE X3S012000BA1HA-X (C254364, 2,975, ESR
    not in the listing); the full reviewer also names ABM8G-12.000MHZ-B4Y-T (C276421). Each needs its ESR and drive
    level checked against R28 before use.
  - (c) Order without X1 and hand-fit it.

## Major

### M1. 87 vias (and the net-class default) were in JLCPCB's charged via class - fixed

- **What:** 87 of 235 vias were 0.4 mm pads on 0.2 mm holes. The Default net class placed 0.4 / 0.2 vias and the
  rules allowed down to 0.4 mm, so DRC did not stop new ones.
- **Evidence:** JLCPCB capabilities, "Via hole size/diameter": "③ 0.1mm or 0.15mm hole size with any size via
  diameter, and 0.2mm or 0.25mm hole size with via diameter less than 0.45mm" will cost more. Please select
  corresponding via size option when placing order." The 139 at 0.45 / 0.2 and the 9 at 0.63 / 0.3 are free.
- **Consequence:** cost and order risk, not electrical. The smaller-via option on a 5-pc 4-layer quote has taken the
  price from $13.10 to $49.78 (kicad-new-board reference, 2026-10-30); without it, JLC may hold or reprice the order.
- **Fix (applied):** all 87 grown to 0.45 / 0.2 in place (same position and hole; ring 0.10 -> 0.125 mm); Default net
  class via 0.45 / 0.2 and `min_via_diameter` 0.45, so DRC now reports a smaller via as an error (checked: the rule
  alone flags all 87 on the old board). Tightest via-to-other-net copper after the fix: 0.125 mm, as the existing 0.45
  mm vias already had, against JLC's 0.09 mm.

### M2. The VREG_LX switch-node track was under JLC's pad-to-track clearance at C10 and C12 - fixed

- **What:** the F.Cu VREG_LX track (0.20 mm, y 99.20, x 134.51-137.35) between L1 and U1.63 passed 0.0925 mm from
  C12.2 (GND) and 0.0975 mm from C10.1 (1V1). They were the only pad-to-track gaps on the board under 0.1 mm. DRC
  passed because C10 and C12 carry a 0.09 mm local pad clearance.
- **Evidence:** JLCPCB capabilities: "Pad to track clearance (1oz)... 0.1mm". Measured on the filled board.
- **Consequence:** a fab short or bridge to C10 puts the 0-3.3 V switching node on the 1.1 V core rail; one to C12
  shorts the switch to ground. Low probability, high cost, and the DFM check is likely to flag it.
- **Fix (applied):** the segment narrowed to 0.18 mm in place: 0.1025 mm to C12.2, 0.1075 mm to C10.1. 0.18 mm of 1 oz
  outer copper carries the core regulator's 200 mA with a large margin. DRC unchanged; no track-to-pad gap on the
  board is now under 0.1 mm.

## Minor

### m1. Vias crowding their own pad's mask opening - partly fixed

The mask is 1:1 (`pad_to_mask_clearance 0`), so a pad edge is its mask opening. A tented via closer than about
0.09 mm leaves a mask web JLC cannot hold (soldermask: "Keep at least 0.09 mm clearance between soldermask openings
and neighboring traces"; minimum bridge 0.10 mm), and solder wets onto the via. All are same-net (no short); DRC and
`board_lint` cannot see it.

| Via (net) | Pad | Gap before | After |
|---|---|---|---|
| (135.31, 101.74) GND, in the pad | C9.1 (0402) | hung 0.07 mm past the pad | centred (135.31, 101.56) |
| (146.528, 100.402) RUN | U1.35 | 0.082 | 0.107 (moved 0.025 mm) |
| (127.80, 97.45) GPIO47 | JP4.2 | 0.075 after M1 | 0.100 (moved 0.025 mm) |
| (147.87, 101.60) 1V1 | C2.1 (0402) | 0.028 | unchanged: boxed in |
| (147.755, 100.007) GPIO28 | U1.36, toe | 0.030 | unchanged: boxed in |
| (134.493, 100.178) 1V1 | L1.2 / C10.1 | 0.038 / 0.064 | unchanged: boxed in |

The last three have no position within 0.15 mm that keeps 0.1 mm to other-net copper (`via_nudge.py`): XOUT,
GPIO27 and USB_D- respectively. Inspect C2, U1.36 and L1/C10 at first assembly.

### m2. DRC did not enforce JLC's spacing from a filled via to a plated hole - fixed

- **Evidence:** JLC POFV: via hole 0.2-0.5 mm, "Should be placed more than 0.45 mm from regular PTHs or NPTHs";
  capabilities: "Pad Hole-to-Hole Spacing 0.45mm". The board rule was 0.25 mm, at warning severity.
- **Today:** fine (closest 0.600 mm, GND via at 162.80, 92.60 to J4.44's castellated hole).
- **Fix (applied):** `.kicad_dru` rule "via to plated hole" (hole_to_hole 0.45 mm) and `hole_to_hole` raised to error.
  Checked live: at 0.65 mm on a copy it reports the J4.44 via and six others as errors.

### m3. The 4.7 uF core capacitor was on the wrong DVDD pin - fixed

- **Evidence:** RP2350 datasheet 6.1.3: "the two DVDD pins closest to the regulator should be decoupled with a 100nF
  capacitor close to the pins. The DVDD pin furthest from the regulator should be decoupled with a 4.7μF capacitor."
  Pin 32 is the furthest: 12.5 mm from the regulator output (L1 / C10) against 10.7 mm for pin 10 and much less for
  pin 51. The board had C5 (4.7 uF) on pin 10 and C2 (100 nF) on pin 32.
- **Fix (applied):** C2 and C5 swap values and all fields (C2 = C23733 CL05A475MP5NRNC 4.7 uF, C5 = C1525 100 nF),
  schematic and board. Same 0402 land and part count. The pack now gives C2 4.7 uF at 1.3 mm from pin 32.

### m4. Silkscreen and documentation

- No board revision on the silkscreen; the back logo reads "pico Stretch" (the README calls it Pico Stretch 2).
  Add a version and date, e.g. "v2 2026-10", so boards, BOM and gerbers can be matched.
- Front silk shows two stray references, R5 (by BOOT, on Boot1's and U4's bodies per `board_lint`) and R9 (by the
  RM2), while every other reference is hidden.
- The README's `images/` are from 2026-05-18 and predate JP4, TP3/TP4, the back pin labels and every review fix.
  Re-run `scripts/render-images.sh`.
- The README's "Production files" section names the Fabrication Toolkit set (`pico-stretch2.zip`, `bom.csv`,
  `positions.csv`), while `production/` now also holds an untracked JLCImport set (`pico-stretch2-*.csv`, gerbers
  zip, report, 2026-10-29 18:34). Both predate this review. Regenerate one set, delete the other, and match the README.

---

## Checked and found fine

**1. Power entry and protection.** USB-C VBUS -> D1 (DFLS130L) -> VSYS -> U3 (ME6217) -> 3V3; external VSYS (J4.63)
cannot back-feed USB through D1. ME6217: SOT-23-5 pinout 1 VIN, 2 VSS, 3 CE, 4 NC, 5 VOUT as wired (datasheet p.1);
CE held to VSYS through R11 100 k, inside "VSS-0.3~VIN+0.3" and above VCEH 1.5 V; dropout 100 / 180 mV typ / max at
300 mA. Operating point (full reviewer's solve, 4.40-5.25 V at the receptacle): VSYS 3.93-4.92 V against the
~3.5 V U3 needs; my hand check at 0.4 A agrees (4.4 V - 0.25 V D1 - 23 mV copper = 4.13 V). The VBUS TVS was tried and
removed by decision (review 2 m1); hot-plug overshoot on a short legacy cable remains a known limit.

**2. Copper capacity and heat.** Power runs (power.md): VBUS 3.2 mV, VSYS 19.9 mV, 3V3 28.3 mV, 1V1 4.2 mV drop at
the configured currents; ground return -0.6 mV. Busiest via 0.90 A (VSYS, about 2.2 mOhm at 18 um plating: 2 mV,
1.8 mW; accepted m5). Heat-source table (thermal.md): U3, D1, U1, U5 with losses; U4, U6, L1, D2, D3, J4, USB1, R7
negligible with reasons; 0 UNKNOWN.

| Corner | Loss | h closed box (5 / 7 / 10) peak | h bare board (9 / 12 / 16) peak | U3 board T (bare, nominal) |
|---|---|---|---|---|
| typical (80 mA on 3V3) | 0.24 W | 60 / 55 / 52 C | 53 / 50 / 48 C | 50 C |
| radio_tx, sustained | 1.65 W | 162 / 135 / 114 C | 120 / 107 / 96 C | 106 C |

Typical use is far from every limit. Sustained full-rate transmit takes U3 past the ME6217's 85 C operating range
(TOPR -40~+85 C) even on a bare board, though under its 160 C shutdown: that is the accepted "bursty transmit"
decision, now with a bare-board number. No junction estimates (no psi_JB / theta_JC for U3; RP2350B's is TBD).

**3. Ground and return paths.** In1 and In2 GND are one piece each (80.6 % / 81.3 %). The only inner track is the
GPIO47 link on In1 (review 1: crossed only by static nets on F.Cu, B.Cu crossers reference In2). 93 ground vias /
plated holes within 3 mm of the edge, no gap over 10 mm, no weakly stitched piece. Same-net isolation: no islands
declared in the config; the full reviewer checked the RP2350 VREG single-point ground (PGND to the plane at C10/C12)
by hand and it holds.

**4. Regulators and decoupling.** RP2350 VREG parts match the hardware design guide: L1 AOTA-B201610S3R3 (the
polarity-marked part), 4.7 uF on VREG_VIN (C12) and VOUT (C10), 33 ohm + 4.7 uF on VREG_AVDD (R6 / C11), and after m3
4.7 uF on the furthest DVDD pin. Decoupling (emc.md): all 22 IC supply pins have a capacitor within 5 mm of copper
path, 0 flagged (the new connectivity-based check no longer reports review 2's U6.8 artefact). The emc.md hot-loop
rows name the nearest capacitors (C36, C13) rather than CIN / COUT (C12, C10); both have their own GND via-in-pad to
In1, and a 0.2 mm barrel to In1 is about 0.05-0.13 nH. ME6217: C37 10 uF in, C40 10 uF out (>= 4.7 uF, ESR <= 0.5 ohm).

**5. Signal integrity and EMC.** emc.md reference spans: high 4 (GPIO47 In1 link, VREG_LX, RUN, ADC_VREF), medium 0,
low 11 - the same rows as reviews 1 and 2, each explained in review 1 (the In1 link returns through In1 GND beside it
and In2; the others are static or under the VREG cut-out by design). Crosstalk top rows are slow or static pairs and
short QSPI runs. USB is full speed: the 133 / 144 ohm Zdiff estimates do not matter at 12 Mb/s.

**6. ESD and external interfaces.** USB D+/D- clamped at the connector by D2/D3 (RCLAMP0521P) on the connector side
of R2/R3; CC1/CC2 5.1 k to GND; shell to GND. Castellated GPIO pads have no ESD parts, as on the Pico 2. Buttons
drive QSPI_SS through R5 (1 k) and RUN with C15.

**7. Datasheet compliance.** Flash and PSRAM data lines traced pin to pin: QSPI_SD0 -> U4 DI / U6 SI-SIO0, SD1 -> U4
DO / U6 SO-SIO1, SD2 / SD3 to IO2 / IO3, SCLK to CLK; U4 CS# on QSPI_SS; U6 CE on JP1/JP4 with R14 1 k pull-up. QSPI_SS
has no external pull-up: the hardware design guide fits none with this flash ("with this particular flash device,
the external pull-up is unnecessary"; it is a W25Q128JV) and requires the 1 k to the BOOT button (R5). RM2: VIN and
VDDIO on 3V3, WL_ON/BT_ON held off by R10 when JP3 is open, CS via JP2 with R9, data via R15 / R16 per review 1. NC
audit: U3.4 is NC in the datasheet; Reset1.1 is the switch's internally joined pin; USB SBU1/2 unused (USB 2.0 device);
the RM2 NC pins follow its datasheet. Derived values re-checked by hand (no `design-values.json`): CC 5.1 k, LED 2 k
(0.7 mA), R14 1 k (review 2), VREG_AVDD RC, crystal 15 pF for CL 10 pF (7.5 + ~3 pF stray), R28 1 k damping.

**8. Sourcing and assembly.** Every BOM part except X1 is in stock at JLC (global, 2026-10-31); lowest L1 464
(pre-order by decision), U1 1,932, D1 6,062. 8 extended parts with a loading fee (about $24) plus 1 preferred. U5 and
U6 are DNP and left out of BOM and CPL. Placements: 7 high confidence, 48 to check in the preview (symmetric 2-terminal
parts), 6 unverified (J2, J4, TP1-4: no LCSC number, not assembled); D1 and PWR_LED1 polarised - check them in JLC's
preview. Schematic and board fields match (`partfields`: the 28 problems are blank Datasheet / LCSC on J2, J4, TP1-4).

**9. Mechanical and silkscreen.** Copper is at least 0.5 mm from the edge (rule `min_copper_edge_clearance` 0.5, JLC
0.2 mm). No mounting holes (castellated module). `board_lint`: no SILK OUTLINE or UNDER HARDWARE items; SILK ON PART
pad labels under J4/U5 accepted; the rest under m4. Vias: hole-to-hole at least 0.375 mm, inner antipads 0.25 mm,
every GND via on both planes, 8:1 aspect ratio, all 78 vias in pads within JLC's 0.2-0.5 mm filled-via hole range
(ordered filled and capped, accepted); `board_lint`'s PASTE ON HOLE / VIA IN PAD lines are those vias.

**10. Firmware-visible consequences.** Unchanged from review 1 m15: PSRAM CS on GPIO0 (JP1) or GPIO47 (JP4), never
both, and firmware sets the chosen pin to XIP_CS1; flash clock divider 2 as on the Pico 2, raise it if QSPI errors
appear with PSRAM fitted; radio pins GPIO23-25/29 belong to the RM2 when JP2/JP3 are closed; limit sustained transmit
(heat above). If X1 is substituted (B1 (b)), test start-up and USB over temperature before trusting it.

## Fix before / after

| Measure | Before (`review3/pack`) | After (`review3/pack_after`) |
|---|---|---|
| Vias at 0.4 / 0.2 (charged) | 87 | 0 |
| Default net-class via / DRC minimum via | 0.4 / 0.4 mm | 0.45 / 0.45 mm |
| Via to plated hole: rule / measured | 0.25 mm warning / 0.600 mm | 0.45 mm error / 0.600 mm |
| Vias within 0.09 mm of their own pad, or off it | 5 | 3 (boxed in) |
| Track-to-pad gaps under JLC's 0.1 mm | 2 (VREG_LX) | 0 |
| 4.7 uF on DVDD pin 32 (furthest) | no (100 nF) | yes |
| Tightest via-to-other-net copper / hole-to-hole | 0.125 / 0.375 mm | 0.125 / 0.375 mm |
| DRC / unconnected / parity / ERC | 8 / 0 / 0 / 162 | 8 / 0 / 0 / 162, 0 new |
| Drops vbus / vsys / 3V3 / 1V1 | 3.2 / 19.9 / 28.4 / 4.2 mV | 3.2 / 19.9 / 28.3 / 4.2 mV |
| In1 / In2 GND | 80.6 % / 81.3 %, 1 piece each | same |
| radio_tx peak (closed box, nominal h) | 134.8 C | 134.8 C |

## Adversarial passes

- **Via reviewer** (`review3/pack/adversarial_review.md`): M1 reached independently; its via-to-mask finding kept as
  m1 (re-measured, plus the GPIO47 case the grow creates); its via-to-PTH rule kept as m2. Not kept: "U1's 0.63 / 0.30
  vias exceed JLC's 0.15-0.55 mm filled-via range" - that range starts at JLC's minimum hole (0.15 mm), not its
  minimum pad (0.25 mm), so it is a hole size, and the POFV page states 0.2-0.5 mm hole; 0.3 mm fits both.
- **Full reviewer** (`review3/full_adversarial_review.md`):
  - Kept: B1 (found independently by both of us), M2 (re-measured: 0.0925 / 0.0975 mm, and the 0.09 mm pad
    overrides explain why DRC passed), m3 (datasheet re-read; fixed by swapping C2/C5 rather than adding a capacitor),
    the mixed `production/` sets (m4), the thermal h range (re-solved above), and a script nit (the plugin path was
    picked with a string sort; both fix scripts now compare versions numerically).
  - Not kept: "71 U1 pads sit exactly 0.1 mm from other-net pour" - that is JLC's minimum, not under it, and the pour
    is under mask. Raising the two zones' clearance to 0.15 mm would add margin; not done without a reason to.
- **Pack limits both raised:** no stock check (B1 was invisible to the pack), no check against the fab's pad-to-track
  and via-price rules (M1, M2), the VBUS run titled as reaching J4.64 with no sink there, thermal stitching advice
  naming planes that do not exist, the closed-box h default on a bare board, and GPIO12-19 (HSTX-capable) classed as
  slow (the full reviewer checked them against the planes by hand: nothing hidden).

## After the review: USB test pads on the Pico footprint (`scripts/pico_testpads.py`)

At the owner's request, so the board can be hot-plate soldered onto a carrier made for the Pico / Pico 2 SMT
footprint (Pico 2 datasheet 3.2, Figure 5; pin 1 hole at (1.61, 49.63) per Figure 3; J4 pin 1 hole at
(110.8, 110.38), rows 17.78 mm apart, 1.61 mm from each edge):

- TP3 (USB2_D-) to the Pico TP2 position (110.63, 100.49), TP4 (USB2_D+) to the Pico TP3 position (110.63, 102.49),
  new TP5 (GND) at the Pico TP1 position (113.93, 101.49), all on `Custom:TestPoint_Pad_1.5x1.5mm_R0.3mm`
  (1.5 x 1.5 mm, 0.3 mm radius, as the Pico's). Each overlaps its Pico pad by 97 % (the corner rounding).
- TP5 joins In1 / In2 through a via in its pad at (114.23, 101.04), 0.5 mm clear of the F.Cu VBUS track above it.
- New B.Cu stubs: D- 6.4 mm (above TP5, 0.21 mm clear), D+ 10.4 mm replacing TP4's spur from R3's via (under the
  VSYS via at 119.33, 102.12). Existing tracks unchanged. USB2_D+ / D- now 17.7 / 15.3 mm; at full speed a stub
  this short is invisible.
- Removed: the GND stitching vias at (110.9, 100.59) and (110.9, 102.58), which sat on the new pads. Edge
  stitching 93 -> 91 vias, still no gap over 10 mm.
- Carrier check: nothing of this board's bare back copper lands on the Pico footprint's TP4-TP7 pads; its shell
  pads A-D meet only the USB-C shell legs (GND, as on the Pico) and the NPTH pegs. The USB-C 3D model reaches
  0.90 mm below the top surface, inside the 1.6 mm board (not checked against the connector's drawing).
- Verified on the project: DRC 8 items, 0 new, 0 unconnected, parity 0; ERC 162, 0 new.

## Before ordering

1. Regenerate `production/` from the current board with one tool, remove the other set, update the README (m4).
2. Order options: epoxy-filled and capped vias; castellated holes; JLC04161H-7628; leave the via-size option at its
   default (no charged vias remain).
3. Check D1, PWR_LED1, U1, U3, U4 and the moved C39 / C40 / D3 / C13 in JLC's placement preview.
4. Pre-order or consign L1.

## Limits

- JLC's charge and DFM verdicts are read from its published rules; no quote or DFM run was done.
- Via resistance and inductance are hand models (barrel only). Heat is a steady-state model in still air with no
  junction estimates.
- Not verified: the substitute crystals' ESR and drive level; C37 / C40 DC-bias capacitance; how JLC's CAM treats the
  three boxed-in via/pad webs.

## Files

- `review3/pack/`, `review3/pack_after/`: analysis packs before and after (project copies removed).
- `review3/pack/adversarial_review.md`, `review3/full_adversarial_review.md`: the two reviewers' reports.
- `review3/scripts/via_audit.py`, `via_mask.py`, `via_nudge.py`: via measurements. `review3/renders/`: 3D renders.
- `scripts/review3_fixes.py`: every fix above, rebuilt from the base copy; `scripts/pico_testpads.py` on top of it.
- `review3/renders/pico_tp_back.png`: the new test pads.
