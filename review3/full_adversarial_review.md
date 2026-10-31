# Pico Stretch 2: full-board adversarial review

Board: `/Users/joshv/git/pico-stretch2` working tree (commit 1d4354a plus the uncommitted DESIGN_REVIEW_3 via fixes),
reviewed 2026-10-31. Evidence pack: `review3/pack_after/`. My own runs are on copies in `/tmp/psr4/adv/`:
- `check.sh`: DRC with refill, parity, ERC, board_lint, partfields and nc_audit, in `check/`.
- `jlcimport-cli production --check-only --json` (stock on 2026-10-31 10:23 CDT), in `prod.json`.
- `path_budget.py`: `pb/usb.json` and `pb/usb.md`.
- My geometry scripts: `scripts/refcheck.py`, `edgecheck.py`, `viacheck.py`, `pthtrack.py`, `padtrack.py`,
  `padpad.py` and `u1pour.py`, all run on `pack_after/board.json`.
- Renders in `r/`.

JLC limits are quoted from jlcpcb.com/capabilities/pcb-capabilities, fetched 2026-10-31.

Accepted items from the brief are not repeated unless noted.

---

## Blocker

### B1. X1 (ABM8-272-T3, C20625731) is out of stock at LCSC/JLC: the order fails as configured

- **What:** X1 is the 12 MHz crystal at (154.36, 101.63).
- **Evidence:**
  - `jlcimport-cli production --check-only` (2026-10-31) gives `{'severity': 'error', 'references': ['X1'], 'message': 'Out of stock'}`, stock 0.
  - `jlcimport-cli search "ABM8-272-T3"` finds no other LCSC number for this MPN.
  - Two days earlier there were 890 and 845 units (DESIGN_REVIEW.md, DESIGN_REVIEW_2.md). The Oct-29 `production/pico-stretch2-report.txt` shows "0 errors".
  - The analysis pack has no sourcing step, so nothing in `review3/` saw the change.
- **Consequence:**
  - JLC will not place X1. A board without a crystal has no USB: the bootrom's USB boot needs XOSC (Hardware design §4: "Applications which rely on exact frequencies are not possible without an external frequency source, USB being a prime example").
  - The boards arrive unable to take firmware over USB until X1 is hand-fitted. That is a 3.2 × 2.5 mm, 4-pad part next to the QFN.
- **Fix, cheapest first:**
  - **(a)** Pre-order or consign ABM8-272-T3, the same route the README already uses for L1. The cost is lead time plus JLC's global-sourcing fee.
  - **(b)** Substitute a crystal on the same ABM8 3.2 × 2.5 4-pad land. Candidates in stock today:
    - ABM8G-12.000MHZ-B4Y-T (C276421, 3,361 pcs, Abracon, 10 pF, ±30 ppm)
    - YXC X322512MMB4SI (C50430, 8,409 pcs, 10 pF)

    The ABM8-272-T3 values are ESR ≤ 50 Ω, CL 10 pF and drive 10–200 µW (Abracon drawing 456603, §1.0). C17/C18 (15 pF) and R28 (1 kΩ) are tuned for exactly these. Hardware design §4.1 says any other crystal "will require extensive testing". I did not verify the candidates' ESR.
  - Either way, add X1 to the README's "often out of stock" note next to L1, and re-run the stock check on the day of ordering.

## Major

### M1. The VREG_LX track is 0.0925 mm from C12's GND pad and 0.0975 mm from C10's 1V1 pad, under JLC's 0.1 mm pad-to-track minimum

- **What:**
  - The /VREG_LX track is 0.20 mm wide, at y 99.20, from (137.35, 99.20) to (134.51, 99.20). It runs between the two regulator capacitors:
    - C12.2 (GND, CIN) at x 135.56–136.18, y 98.45–99.01: gap **0.0925 mm**.
    - C10.1 (1V1, COUT) at x 134.59–135.21, y 99.40–99.96: gap **0.0975 mm**.
  - These are the only two pad-to-track gaps on the board under 0.1 mm (`padtrack.py`, both outer layers). There are no track-to-track gaps under 0.1 mm.
- **Evidence:**
  - JLC capabilities, multilayer, 1 oz: "Pad-to-track clearance: 0.1 mm minimum (min. 0.09 mm locally for BGA pads)".
  - DRC passes because `min_clearance` is 0.09 mm.
  - DESIGN_REVIEW_2 only audited pad-to-pad gaps. The pack has no fab-capability check.
  - Render: `r/vreg_f.png`.
- **Consequence:**
  - JLC DFM may flag it, or etch it as drawn with a mask web at its 0.09 mm opening-to-trace limit.
  - A bridge here costs more than anywhere else on the board:
    - LX to C10.1 shorts the inductor, so DVDD sees the raw 0 to 3.3 V switch node. That very likely destroys the RP2350, the same class of failure DESIGN_REVIEW_2 M1 ranked Major.
    - LX to C12.2 shorts the switch node to PGND, and the regulator never comes up.
  - The probability is low. The severity and the fix cost match DESIGN_REVIEW_2 M1.
- **Fix:**
  - Neck the LX track to 0.18 mm over x 134.5–136.3 and centre it at y 99.205. That gives 0.105 mm to both pads.
  - The pads are 0.39 mm apart (99.01 to 99.40), so a 0.19 mm track centred there is the widest that clears 0.1 mm on both sides.
  - 0.18 mm over 2.8 mm adds about 1 mΩ at about 0.2 A core current: negligible.
  - A few minutes' work. Then re-run DRC with a local clearance of 0.1 mm on the LX net, so it stays enforced.

## Minor

### m1. Every non-3V3 U1 pad sits 0.100 mm from another net's pour under the package, and the exposed pad (100 % paste, accepted m7) is ringed by 1V1 at 0.100 mm

- **What:**
  - Under U1, the "3v3_cpu" zone (priority 7) fills between the pin ring and a "1v1_cpu" ring (priority 8). That ring surrounds the GND exposed pad. Both zones have 0.1 mm clearance.
  - `u1pour.py` counts 71 U1 pads at exactly 0.100 mm from another net's pour. They include:
    - DVDD 10, 32 and 51 and VREG_FB 65 (1V1) to 3V3
    - VREG_LX 63 to 3V3
    - USB_D± 66/67 to 3V3
    - PGND 62 to 3V3
    - the 11.6 mm² exposed pad 81 (GND) to the 1V1 ring
  - Render: `r/u1c.png`.
- **Evidence:** JLC "Pad-to-track clearance 0.1 mm minimum", and "Keep at least 0.09 mm clearance between soldermask openings and neighboring traces". Mask openings are 1:1 (JLC: "Pad-to-opening ratio is 1:1"). The board is at the limit everywhere under the chip, not under it.
- **Consequence:**
  - The one area that collects excess solder, a 100 %-paste exposed pad (m7), is separated from the core rail only by a 0.1 mm mask web.
  - Exposed-pad squeeze-out over a slightly misregistered web bridges GND to 1V1 (the regulator's current limit, no boot). A heel bridge on pins 10/32/51/65 puts 3.3 V on DVDD.
  - This is a new mechanism that makes accepted m7 worse than described. m7 only considered floating and peripheral opens.
- **Fix:**
  - Set the clearance of zones "3v3_cpu" and "1v1_cpu" to 0.15 mm (0.2 mm where it still fills to the IOVDD and DVDD heels). Refill, then confirm 0 unconnected.
  - Window-pane the exposed-pad paste to about 60–70 %, which m7 already proposes. Together these remove the mechanism.
  - One zone property edit and a footprint paste change.

### m2. The 4.7 µF DVDD capacitor is on pin 10, not on the DVDD pin furthest from the regulator (pin 32)

- **What:**
  - Measured from VREG_LX (pin 63, 137.35, 99.20): DVDD 51 is 5.1 mm away, DVDD 10 is 9.2 mm and DVDD 32 is **10.1 mm**.
  - C5 (4.7 µF) sits at pin 10. C2 (100 nF) sits at pin 32.
- **Evidence:**
  - RP2350 datasheet §6.1.3: "the two DVDD pins closest to the regulator should be decoupled with a 100nF capacitor … The DVDD pin furthest from the regulator should be decoupled with a 4.7μF capacitor".
  - §6.3.8.1 places the second 4.7 µF "on the bottom edge of the package (DVDD pin 23 on the QFN-60)", which is the edge opposite the regulator. On QFN-80 that edge is pins 21–40, so pin 32.
  - Earlier reviews accepted pin 10 without checking which pin is furthest.
- **Consequence:**
  - The far edge of the core sees only 100 nF locally. DVDD transients must stay within ±100 mV (Table 1688, note b).
  - The effect is likely small, because 1V1 is also distributed by the F.Cu ring and the B.Cu track. It is a datasheet deviation, not a known failure.
- **Fix:** change C2 to 4.7 µF (C23733, the same 0402 land, Basic, already on the BOM). Keep C5 as it is or make it 100 nF. BOM change only.

### m3. `production/` holds two different generators' outputs, and the README names the wrong set

- **What:** `production/` contains two sets of files from two tools, with different rotation logic:
  - The Fabrication Toolkit set (10:46): `bom.csv`, `positions.csv`, `pico-stretch2.zip`. It uses Auto Translate.
  - The JLCImport set (18:34, untracked): `pico-stretch2-bom.csv`, `pico-stretch2-cpl.csv`, `pico-stretch2-gerbers.zip`. It uses rotations solved from JLC's own footprints.

  The README lists only the Fabrication Toolkit names.
- **Consequence:** uploading the BOM from one set and the CPL from the other, or the stale set, mixes rotation conventions. This is not the stale-BOM item, which is accepted. It is about which generator is the release path.
- **Fix:** pick one generator, delete the other's files when regenerating, and update the README file list.

---

## Problems with the analysis pack and the tooling

1. **No sourcing step.** The pack has no `sourcing.json` or `bom_check`, so B1 was invisible to every pack-based check. DESIGN_REVIEW_3's "nothing else got worse" table could not have caught it.
2. **No fab-capability clearance check.**
   - `drc.md` is clean because the board's own `min_clearance` is 0.09 mm.
   - JLC's 0.1 mm pad-to-track rule (M1) and the pour-to-pad web (m1) are not tested.
   - The via audit in DESIGN_REVIEW_3 covered vias only.
3. **The VBUS run's title does not match its sinks.** It says "USB-C VBUS pins to D1 anode and castellated VBUS pad, 0.9 A", but the only sink is D1:2. The pass-through to J4.64, which is the high-current case in accepted m5, is not solved, so the "0.00 A busiest via" figure means nothing.
4. **Thermal uses closed-box h (5/7/10) and 35 °C ambient for a bare dev board.**
   - The checklist's bare-board range is 9/12/16 W/m²K.
   - At h = 12, the radio_tx peak scales to about 35 + 99.8 × 7/12 ≈ **93 °C**, not 135 °C.
   - The conclusion does not change: ME6217 Topr is 85 °C and RM2 ambient is 70 °C, so sustained Tx is not viable. The accepted bursty-Tx decision stands.
   - The stale D4 thermal entry is still there.
5. **No islands were declared, so the pack's same-net isolation check is NOT CHECKED.** I checked the datasheet's single-point PGND rule (§6.3.8.1) by hand. Zone GND_VREG is one piece of 1.75 mm² containing only U1.62, C10.2 and C12.2. It reaches the plane through exactly two adjacent vias, (134.90, 98.72) and (135.87, 98.71). It has no F.Cu join to the exposed pad. C11 (CFILT) has its own via at (135.63, 97.73). This passes, but the pack did not prove it.
6. **Classification.** GPIO12–19 (HSTX-capable, about 300 Mb/s DDR) fell through to "slow".
   - My `refcheck.py` checks every net, not just the fast ones. Those nets only cross their own via antipads and the J4 pad clearances, so nothing is hidden there.
   - It does show the classification blind spot. `refcheck.py` also confirms that RUN and ADC_VREF are the only other F.Cu nets over the In1 GPIO47 slot.
7. **Tooling nit.** `scripts/review_fixes.py` now picks the kicad-skills version with `sorted(glob(...))[-1]`. That is a string sort, so a future "0.10.0" sorts before "0.2.0". Use a version-aware sort.

## Checked and found fine (per checklist area)

### 1. Power entry
- **Operating point:** `path_budget.py` (`pb/usb.md`) from USB 4.40–5.25 V through 0.1–0.2 Ω of cable, VBUS copper (3.6 mΩ), D1 and VSYS copper (17.9 mΩ) at 0.40 A.
  - VSYS is 3.93–4.92 V, against the 3.67 V the LDO needs (3.3 V plus the 180 mV maximum dropout at 300 mA, ME6217 p.4, plus margin).
  - Only the attach transient at the USB 2.0 low-power minimum with a worst-case cable dips to 3.52 V, for under a millisecond during soft charge. That is harmless.
- **D1:** DFLS130L IF(AV) is 1 A, and it carries 0.4 A (datasheet p.2).
- **Other entry items:** VBUS-to-VSYS OR-ing; R11 holds CE at VSYS, within the ME6217 CE abs max of VIN + 0.3 V; CE is active-high (Table 1, p.5). The netlist audit flag "CE tied to rail" is the intended behaviour.

### 1b. Start-up
- VREG_VIN and VREG_AVDD come up together through the 33 Ω/4.7 µF filter (about 155 µs time constant; §6.1.8).
- RUN has its internal ~50 kΩ pull-up (Pico 2 datasheet) and C15.

### 2. Copper
- Power drops match the pack: vbus 3.2 mV, vsys 19.9 mV, 3V3 28.3 mV, 1V1 4.2 mV.
- 3V3 at the RM2 in the worst case: about 3.267 V (−1 %) − 50 mV (load regulation) − 17–28 mV of copper ≈ 3.19–3.20 V. That is inside RM2 VIN 3.0–4.8 V but at the "below 3.2 V reduces RF performance" line (RM2 §2.6). Noted, not a finding.

### 3. Ground
- In1 and In2 are each one piece.
- The only inner track is GPIO47 (In1). It is crossed on F.Cu only by 3V3, RUN and ADC_VREF (`refcheck.py`), and In2 is solid under it.
- No outer track crosses a plane void except its own via antipads, the J4 pad clearances and the accepted VREG cut-out.

### 4. Regulators
- The RP2350 VREG matches §6.3.8:
  - CIN C12 and COUT C10 are 4.7 µF 0402.
  - L1 is the specified polarity-marked AOTA part.
  - FB is taken from COUT.
  - The PGND single point is proven (pack item 5).
- The ME6217 has CIN (C37, 10 µF) and CL (C40, 10 µF, plus C38) at its pins, meeting "4.7 µF or more, ESR ≤ 0.5 Ω" (p.6).

### 5. SI/EMC
- No fast net is within 1 mm of the edge.
- Copper-to-edge is at least 0.5 mm except at the castellations. JLC's routed-edge minimum is 0.2 mm.
- Inner GND is at least 0.30 mm from every non-GND castellated hole (JLC inner PTH hole to copper: 0.3 mm). The 0.30 mm are the clipped pads 29–36, exactly at the limit.

### 6. ESD
D2 and D3 sit at the connector, on the connector side of R2/R3 (33 Ω), and the shell goes to GND.

### 7. Datasheets and pinouts
- **Pinouts:**
  - The ME6217C pinout is SOT-23-5 (1 VIN, 2 VSS, 3 CE, 4 NC, 5 VOUT; p.2).
  - QSPI direction: SD0 → DI/SI, SD1 ← DO/SO, SD2/SD3 → IO2/IO3.
  - QMI CS1n is available on GPIO0 and GPIO47 (RP2350 GPIO function table).
- **RM2 wiring** matches RM2 Table 1/2 (470 Ω on DO, 10 kΩ on nIRQ, WL_ON and BT_ON both on GPIO23).
- **ADC network:** R8 200 Ω, R7 1 Ω and C19 match Pico 2 §5.3.
- **Crystal network:** 15 pF / 1 kΩ (Hardware design §4).
- **QSPI_SS:** no pull-up is needed with the W25Q128JVS (Hardware design §3.1).
- **K2-1808SN switch:** the drawing's circuit diagram connects the terminals across the 4.2 mm length (C92589 drawing). Footprint pads 1–2 and 3–4 are on those rows, so Boot1 and Reset1 switch correctly. The land is 5.6/3.2 × 2.85/1.55 mm against the drawing's 5.2/3.1 × 2.8/1.5: slightly generous, fine.
- **QFN-80 exposed pad:** 3.4 mm, which matches D2/E2 (Fig. 149).

### 8. Sourcing and assembly
- Every part except X1 is in stock (2026-10-31):
  - L1: 464 (pre-order is accepted)
  - RP2350B: 1,932
  - D1: 6,062
  - K2 switches: 12,466
  - U6 (DNP, for anyone who clears DNP): C5333729, 3,346
- The board is one-sided assembly. There are 9 extended parts. JLCImport reports R7 (C25086) as Preferred now.

### 9. Mechanical
- **USB-C:** the 3D model's front (y_fp = 1.2 + 3.665 = 4.865 mm) puts the shell about 0.45 mm past the board edge (108.69 against 109.145), so the plug's overmold clears the board.
- **Castellations:** the inner hole rows are 17.78 mm apart (breadboard-compatible), at a 2.54 mm pitch. Holes are 1.0 mm, more than 1 mm from the board's short edges, with 0.6 mm hole-to-hole (JLC castellated: Φ ≥ 0.5, edge ≥ 1, hole-to-hole ≥ 0.5).
- **Via-to-PTH:** the nearest via to a plated hole is 0.600 mm, and the new DRU rule enforces 0.45 mm.
- **PTH hole to other-net copper:** at least 0.351 mm (USB1 shell to VBUS; JLC 0.28 mm minimum, 0.35 mm recommended).

### Recent change (via grow and DRU)
- 226 vias at 0.45/0.2 mm and 9 at 0.63/0.3 mm.
- The tightest via to other-net copper is 0.125 mm (`viacheck.py`, which agrees with DESIGN_REVIEW_3).
- Every non-GND via is at least 0.24 mm from inner copper (JLC inner via hole to copper: 0.2 mm).
- DRC: 8 accepted warnings, 0 errors, 0 unconnected. ERC: the 162 accepted items.
- The board diff outside via sizes is only the C9, RUN and GPIO47 via moves and the 3V3 refill around them.

## Could not verify

- The ESR and drive level of the X1 substitutes (B1b). Their datasheets were not read.
- JLC's DFM verdict on M1 and m1, and its mask registration tolerance (not published on the capabilities page).
- The DC-bias capacitance of C37 and C40 (no Samsung curve available). C37 at 4.7 V may sit near the ME6217's 4.7 µF CIN recommendation.
- Whether the KiCad DRU via-to-pad rule is evaluated in both A/B orders. I relied on DESIGN_REVIEW_3's live test.
- RF and antenna performance, ESD levels and the hot-plug ring (accepted): models only.
- Junction temperatures: the RP2350B θJA/θJB are "TBD" (Table 1671), and ME6217 and RM2 give none.
