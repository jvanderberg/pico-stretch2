# Adversarial review: pico-stretch2, uncommitted fixes on top of 54e971f

Scope: the board and schematic as saved now (identical to `review2/pack/proj/`: `diff -q` is clean on the .kicad_pcb, .kicad_sch and .kicad_dru), compared with HEAD (`/tmp/psr2/headpack`). Scratch scripts are in `/tmp/psr2/adv/` (`gaps2.py`, `fillgap.py`, `bdiff.py`, `j4u5.py`, `hp2.py`, `fpdump.py`, `wrlbb.py`). The JLC limits quoted below come from jlcpcb.com/capabilities/pcb-capabilities, fetched 2026-10-29: SMD pad to pad (different nets) 0.15 mm, pad to track 0.10 mm, green mask dam 0.10 mm, multilayer PTH ring 0.20 mm recommended and 0.15 mm minimum.

`bdiff.py` (HEAD board.json vs now) shows exactly the intended edits and nothing else: C39, C40 and D3 moved, D4 new, R14 value, five tracks added and three removed, three vias removed and one added, and the cut-out zone. The ERC is unchanged (162 items, none new). DRC with refill and parity: 0 errors, 0 unconnected, 0 parity issues, 8 lib_footprint_mismatch and 1 silk_over_copper.

## Blocker

None.

## Major

### 1. D3 pad 1 (GND) is 0.10 mm from C39 pad 1 (VSYS). Both are pasted, with no mask dam to spare.

- **What:**
  - D3.1 GND, 117.25–117.85 × 101.62–102.22, faces C39.1 VSYS, 117.54–118.16 × 102.32–102.88. The edges are 0.10 mm apart along a 0.31 mm overlap.
  - Both pads are on F.Paste.
  - The board has `pad_to_mask_clearance 0`, and neither footprint sets a margin, so the mask web between the pads is exactly 0.10 mm.
- **Evidence:**
  - `gaps2.py`: (0.100, D3.1 GND, C39.1 VSYS). It is new: not present at HEAD.
  - The same scan finds no other new different-net gap under 0.15 mm except D3.1 to the USB2_D+ track: 0.110 mm at y 101.43, and 0.136 mm on the diagonal. Those are pad-to-track gaps, so they meet JLC's 0.10 mm.
  - Coordinator's figure confirmed.
- **Consequence:**
  - The gap breaks JLC's 0.15 mm SMD pad-to-pad rule. Their DFM will either flag it or build it as is.
  - The mask web is at the 0.10 mm green minimum. JLC removes webs that fall below the minimum, which leaves a paste bridge free to form.
  - A bridge here shorts VSYS to GND. The USB host port current-limits, and the board looks dead. The short sits under the tightest cluster on the board, where it is hard to see or rework.
  - KiCad DRC passes only because the netclass clearance is 0.10 mm.
- **Fix:**
  - Move C39 down by 0.08–0.10 mm, to (117.85, 103.16–103.18). That gives a 0.18–0.20 mm gap.
  - Checked: C39.1 is then still more than 0.2 mm from R4.2 (CC2) and C37.1. C39.2 stays on GND next to R4.1. The C39.2 → R4.1 via track and the VSYS pour connection still work.
  - Refill and re-run DRC. About 5 minutes.

### 2. The production outputs are stale, and the new and rotated parts have no placement check

- **What:** Everything in `production/` (bom.csv, positions.csv, designators.csv, netlist.ipc, pico-stretch2.zip) is from 11:46. The board and schematic are from 17:20.
  - The current `bom.csv` still has `"C15, C9",0402,2,100nF,C14663`, which is the very M1 error this change fixes.
  - It also has `C40,0402,…,C15525`, `"R10, R14, R16, R9" … 10kΩ`, and a `U5` line. There is no D4.
  - `positions.csv` still has D3 at the old place (49.98, −29.25, 180) and C40 as an 0402. The gerbers in the zip predate the cut-out, the J4 clip and the D4 copper.
- **Consequence:**
  - Uploading the existing zip/BOM/CPL orders the old board with M1 still wrong.
  - Even after regenerating, the earlier rotation sign-off ("Auto Translate confirmed in JLC preview") does not cover D3 (now 0°), C39 (270°), C40 (180°) or the new D4 (270°).
  - D4 is the one that matters:
    - `transformations.csv` (Fabrication Toolkit 10.0) has no `D_SOD-523` rule, so JLC receives KiCad's raw 270°.
    - D4's silk was deleted (`review_fixes.py`), so the bare board has no polarity mark.
    - D4 rotated 180° is a forward diode across VBUS. It conducts as soon as power is applied: the TVS burns, or the host port trips.
  - D3 (RClamp0521P) is bidirectional, and C39/C40 are not polarised, so for those parts only the position matters.
- **Fix:**
  - Regenerate with Fabrication Toolkit (AUTO FILL is on).
  - In JLC's placement preview, confirm that D4's cathode band faces pad 1, toward the J4.64 VBUS track at y 94.3 (ESD5Z datasheet p.1: pin 1 = cathode, band end).
  - Optionally put back a small silk cathode bar beside D4, at x 112.0–112.8, y < 93.9, clear of the "VBUS" label.
  - Cost: about 10 minutes.

## Minor

### 3. D4 (ESD5Z5.0T1G) barely changes the hot-plug peak, and the m4 status overstates the fix

- **What:** D4 sits at (112.4, 95.0) on the J4.64 branch of VBUS, not at USB1. Its VBR is 6.2 V minimum @ 1 mA, and VC is 11.6 V typical @ 5 A, which is about 1 Ω dynamic (ESD5Z datasheet p.3, electrical characteristics table).
- **Evidence:**
  - **Coordinator's model** (`/tmp/psr2/hotplug.py`):
    - Worst case (1.5 µH, 0.1 Ω, 5 µF effective VSYS): VSYS 7.58 V without D4, 7.26 V with D4.
  - **My variant** (`hp2.py`) adds the LDO start-up current, charging the 3V3 bank at 0.35–0.6 A from VSYS > 2 V:
    - VSYS 7.40 → 7.12 V at 0.35 A, and 7.26 → 7.02 V at 0.6 A.
    - So the coordinator's ~0.3 V benefit stands. The model is not optimistic: C37 (CL10A106KP8NNNC, 10 V X5R 0603) loses more capacitance at 7 V than the fixed 5 µF assumes, which pushes the peak up.
    - ME6217 VIN absolute maximum is 7.0 V (me6217.pdf, Absolute Maximum Ratings). Operating maximum is 6.5 V.
  - **Placement:** D4 is about 9.8 mm of 0.25 mm F.Cu from USB1.2, by way of the D1 junction. At about 0.36 nH/mm microstrip over In1 (w 0.25, h 0.21) that is about 3.5 nH.
    - Positive connector ESD is handled by D1 into C37 anyway. For negative ESD, D4 is the only clamp, and it is 3.5 nH away.
    - It mainly protects castellated pad 64.
- **Consequence:**
  - The worst case is still at or above the LDO's absolute maximum. The exposure is narrower than m4 implies, though:
    - A USB-C source on a C-to-C cable does not hot-plug VBUS. It switches vSafe5V on after it sees Rd.
    - The case is a legacy A-to-C cable or an always-live 5 V supply with a low-resistance cable. Typical A-to-C cables, at ≥ 0.2 Ω loop, give ≤ 6.8 V in the model.
  - D4 does no harm. The status line "m4 applied" should not be read as "hot-plug solved".
- **Fix, if wanted:**
  - The coordinator's best option, a 10 µF + 1 Ω damper (6.08 V), adds bulk capacitance. USB 2.0 §7.2.4.1 limits a device to 10 µF at attach, and C37 already uses that budget. Use 4.7 µF/1 Ω (6.54 V) at most, or accept the risk.
  - An SMF5.0A-class TVS (6.61 V) needs an SOD-123F land. There is room only by moving D4's VBUS tap.
  - Otherwise, reword the m4 status line. Cost: text, or one part plus about 30 minutes of layout.

### 4. U1.50 (3V3) to C13.2 (1V1) is 0.13 mm, below JLC's 0.15 mm (pre-existing)

- **What:** C13.2 (1V1) spans 142.01–142.63 × 96.28–96.83. U1.50 (3V3) spans 142.36–142.56 × 96.96–97.63. The gap is 0.127 mm (`padgaps.py`, present at HEAD as well).
- **Consequence:** A DFM flag at JLC. A bridge would short 3V3 to 1V1 (the core regulator output), right at the QFN.
- **Fix:** Move C13 up 0.03–0.05 mm. C13.1 (GND) has room toward y 95.3. Minutes.

### 5. The DESIGN_REVIEW.md Status section misdescribes three applied fixes

- **m1, distance:** "It stops 0.63 mm (3 × prepreg) short of the USB pair" is false.
  - The step corner at (134.75, 100.15) is 0.335 mm from the USB_D− copper at y 100.56, x 134.71–136.7 (the coordinator's figure, re-measured).
  - The 0.63 mm figure holds only against the y 100.86 run at x < 134.41.
  - Electrically this is negligible at full speed: one corner about 2h from the trace centre over about 0.3 mm. The text is still wrong.
- **m1, coverage:** "covers L1, … the 1V1 pad and via" is also false.
  - The cut-out ends at y 100.15. L1 pad 2 (1V1, y 99.69–100.69) is only 46 % covered.
  - The 1V1 via (134.49, 100.18), 0.45 mm, has its centre 0.03 mm outside the cut-out. In1 GND wraps its lower half at 0.125 mm (`fillgap.py`).
  - Full Fig. 27 coverage is impossible without moving the USB pair: L1 pad 2's lower edge is 0.095 mm above the D− track edge. The text should say so.
- **m13:** The front "40A0" is 0.8 × 0.55 (height × width) in the board, set by `review_fixes.py`. The Status text says "0.7 × 0.6".
- **Fix:** Edit the three sentences. Cost: text only.

## Problems with the analysis pack

- **`emc.md` decoupling "U6.8: FAIL, no capacitor reachable"** is an artefact, so the coordinator is right.
  - The F.Cu 3V3 pour (priority 2) runs continuously from U6.8 (129.57–131.52 × 96.12–96.72) around C16.2 to C16.1, 0.4 mm away. See the render `/tmp/psr2/adv/u6.png`.
  - The same FAIL is in the HEAD pack, so it is not caused by this change.
- **`emc.md` decoupling marks U5.16 "ok"** with a 6.2 mm path and "0 of 16" caps within the table's own 5.0 mm limit. Its status logic disagrees with its threshold. This is the radio, which the owner accepted, but the row is wrong.
- **The hot-loop table now pairs U3's output with C38 (100 nF)**, chosen because it is nearest, instead of C40 (10 µF, the ME6217's required CL). The "100 % through one via at (124.18, 101.77)" note is about C38's via, not the bulk cap's. C40's loop is in the per-cap table: 1.52 mm, 0.7 nH. Read the C40 row.
- **USB2 "skew 1.21 mm"** counts the TP4/TP3 test-pad spurs as pair length. It is not a real skew.
- **`power.md` vbus run** does not model D4, which is correct for DC. Nothing in the pack models hot-plug or ESD, so m4 and finding 3 rest on the hand models only.
- **No islands declared:** same-net isolation (the PGND island, the cut-out) is not machine-checked. I checked it by hand (below).

## Checked and found fine

- **Netlist diff vs HEAD:** exactly the intended changes.
  - C9 and C15 are C1525 / CL05B104KO5NNNC.
  - R14 is 1 kΩ C11702.
  - C40 is 10 µF 0603 C19702.
  - D4 is VBUS(pin 1, C) / GND(pin 2, A).
  - U5 is DNP.
- **D4 polarity in design:**
  - Symbol pin 1 is "C", pin 2 is "A".
  - KiCad D_SOD-523 pad 1 is the cathode; the F.Fab bar is at y 94.8, at the pad 1 end.
  - Pad 1 is on VBUS, matching ESD5Z p.1 (pin 1 cathode).
  - The VBUS diagonal (110.88, 92.78)→(113.2, 95.1) passes through pad 1's centre, and DRC confirms the connection.
- **D4 mechanics:**
  - The USB1 3D model's body spans y 96.59–105.53. D4's pads end at y 96.00, so D4 is not under the shell.
  - The D4–USB1 courtyard overlap is the 0.22 mm courtyard margin at the shell-leg pads.
  - D4.2 to the shell pad 13 (same net) is 0.13 mm.
- **D4 land:** KiCad's 0.6 × 0.7 pads at ±0.7 mm are larger than onsemi's recommended 0.40 × 0.48 at 1.80 mm overall (p.5). That is acceptable for SOD-523 reflow.
- **Courtyard exemptions:** running DRC without the .dru shows every named pair (C40/C38, C40/U3, D3/C37, C39/C37, D3/R3, D4/USB1, D3/R4, D3/C39, C39/R4) really overlapping. The removed D3/R2 pair no longer overlaps.
- **J4 clip:**
  - Gap to RM2 pads 1/3/5/6 is 0.39 mm (was 0.24); to 16/17/19/21 it is 0.49 mm (was 0.34) (`j4u5.py`).
  - Hole positions are unchanged: KiCad's drill offset moves the shape, not the hole.
  - The 0.20 mm tip ring meets JLC's multilayer recommendation of 0.20 mm (minimum 0.15). The library footprint matches the board.
- **C40:**
  - 3V3 pad → 0.3 mm track → U3.5. The GND via-in-pad clears the B.Cu 3V3_EN (x 121.1) and Net-(JP1-A) (x 121.87) tracks.
  - C40.1 to the 3V3 pour is 0.096 mm, at the 0.10 mm netclass value within KiCad's arc error. That is pad-to-pour, so JLC's 0.10 mm pad-to-track applies.
  - The p3v3 DC run is unchanged (28.4 mV worst).
- **D3 in line:**
  - The B.Cu stub and both of D3's old vias are gone, with no dangling copper (DRC `--all-track-errors` is clean).
  - The TP4 spur is 1.3 mm on B.Cu, 0.155 mm from the VSYS B.Cu track (pre-existing via).
  - The D3 GND via is in its pad, over In1.
- **In1 cut-out:**
  - It does not split In1 (one piece).
  - The PGND vias (134.90, 98.72) and (135.87, 98.71) stay on plane, with a 0.13 mm neck above the strip.
  - No F.Cu signal other than LX/1V1 crosses it, and the In1 GPIO47 link is far away.
- **Fills:** the user's saved file has the same fills as the refilled copy (areas identical in the USB/LDO window; the files are byte-identical).
- **No new silk collisions** at D4 / D3 / C39 / C40 (SVG render `/tmp/psr2/adv/F_usb.png`). "VBUS" and "VSYS" sit either side of D4, clear of its pads.
- **Thermal:** unchanged, apart from D4 listed as off below 6.2 V, which is correct for 5.0–5.5 V VBUS (IR ≤ 50 µA at VRWM).
- **U5:** `(attr smd dnp)`, no F.Paste, and Fabrication Toolkit has `EXCLUDE DNP: true`.

## Could not verify

- JLC/LCSC stock for C82044. Neither the JLC nor the LCSC page states a quantity; JLC lists it as Extended, PCBA-supported.
- JLC's zero orientation for C82044's SOD-523, which is the reason for the preview check in finding 2.
- Whether JLC's DFM rejects or only warns on the 0.10 mm (finding 1) and 0.127 mm (finding 4) pad gaps, and whether CAM keeps a 0.10 mm mask web.
- Real hot-plug and ESD behaviour. These are models only, with C37's DC-bias curve not taken from the Samsung data.
- C40's effective capacitance at 3.3 V. The CL10A106KP8NNNC DC-bias curve was not read; ≥ 4.7 µF is likely.
