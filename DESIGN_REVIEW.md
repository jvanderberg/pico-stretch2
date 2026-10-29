# Pico Stretch 2: engineering design review

Board: `/Users/joshv/git/pico-stretch2` at HEAD 8e0d15f (2026-10-29 11:41). Production files exported 11:46 from the same board. RP2350B dev board, 82.4 x 21.3 mm, 4 layers (JLC04161H-7628), KiCad 10.0.1, JLCPCB economic PCBA.

Scope: review only. Nothing in the project was modified. Supporting files are in `review/`.

## Method

- **Analysis pack:** `review/pack/` (kicad-board-review). Zones were refilled on a copy, with DRC and schematic parity. It includes the netlist digest, DC solver runs at 15.2 µm inner copper (the stackup's real value), and plane, EMC and crosstalk geometry. Net classes and power runs are in `review/pack/review_config.json`.
- **Datasheets:** read (local copies, not in the repo):
  - RP2350 datasheet §1.2, §6.3.8 (Fig. 25–28), §9.3, §14.2 (Fig. 150), Table 1683 and errata E9/E14
  - Hardware design with RP2350
  - Pico 2 and RM2 datasheets
  - ME6217, W25Q128JV, APS6404L, DFLS130L, RClamp0521P, ABM8-272-T3, AOTA-B201610S3R3, K2-1808SN and the USB-C receptacle
- **Sourcing:** BOM and LCSC check with `bom_check.py` and `jlcimport-cli` (global stock, 2026-10-29).
- **Board checks:**
  - `board_lint`, `nc_audit`, and a `board_diff` from the initial commit c014245 to HEAD.
  - A scripted connectivity check of the cut-down board.
  - A label-by-label check of the back silkscreen against the netlist.
  - Renders, which I looked at.
- **Independent adversarial review:** `review/pack/adversarial_review.md`. Every finding below was re-checked against the files. Findings that did not survive the check, or that the coordinator ruled out (part rotations, now confirmed in JLC's preview), are dropped.

### Tool workaround (not a board finding)

`emc.py` crashed with `KeyError: 'Top Layer'`. The board's copper layers carry user names (Top Layer, Inner1, Inner2, Bottom Layer), and `boarddump.py` wrote those names, while the stackup is keyed F.Cu, In1.Cu, In2.Cu, B.Cu.

The same mismatch would also have silently broken the DC solver. `power.py` and `fem.py` decide outer vs inner copper by the literal names `F.Cu`/`B.Cu`, so with user names every layer would have been treated as inner copper.

Fix: in a copy of the scripts (`review/boarddump_patched.py`), I made the dump write `pcbnew.BOARD.GetStandardLayerName()` for pad layers, track layers and the layer list. The whole pack then uses canonical names and `emc.py`, `planes.py` and `power.py` run unmodified. The plugin's own files were not touched.

### Status (2026-10-29, `scripts/review_fixes.py`)

Applied: **M1, m1, m2, m3, m8, m9, m11, m13**. Not done (by decision): M2 (cut-down board, aspirational), m4 (VBUS TVS: tried, then removed; see below), m5–m7, m10, m12, m14–m16. Each applied fix differs from the original suggestion as follows:

- **M1:** C9/C15 carry C1's fields (C1525, CL05B104KO5NNNC), in schematic and board.
- **m1:** the In1 cut-out now spans 132.5–137.3 × 97.45–100.15, with a step at x 134.75 up to y 99.85. It covers L1's LX pad and the LX pour. It covers part of the rest:
  - L1's 1V1 pad: about half (53 % of it is still over In1 GND).
  - C10/C12 supply pads: 14 % and 20 % still over In1 GND.
  - 1V1 pour: 40 % still over In1 GND.
  - The 1V1 via's centre (134.49, 100.18) is 0.03 mm outside the cut-out; only its antipad joins it.

  It stops short of the USB pair so it does not reach y 100.8 as first suggested. The gap to USB_D− copper is 0.635 mm along x 134.75–136.25, but only 0.335 mm at the step corner (134.75, 100.15). The pair still runs over no void (DESIGN_REVIEW_2.md m2). The GND vias at (134.90, 98.72) and (135.87, 98.71) stay on plane.
- **m2:** D3 sits in C39's old place (118.05, 101.92), with its D+ pad 0.5 mm under the F.Cu D+ track and its GND pad on the existing via. The B.Cu stub and both of D3's old vias are gone. TP4 hangs off R3's via. C39 moved to (117.85, 103.08), between R4 and C37, rotated 90° so that its GND pad faces D3's GND pad. That pad joins D3's via with a short track. With the VSYS pad at the top it sat 0.10 mm from D3's GND pad (DESIGN_REVIEW_2.md M1).
- **m3:** R14 is 1 kΩ (C11702).
- **m4:** not done. A VBUS TVS (D4, ESD5Z5.0T1G) was fitted and then removed, by decision. Its 6.2 V knee lowered the modelled worst-case hot-plug peak by only 0.2–0.3 V (DESIGN_REVIEW_2.md m1). The hot-plug ring needs a legacy A-to-C cable or an always-live supply; USB-C sources do not hot-plug VBUS.
- **m8:** C40 is a 10 µF 0603 (C19702), at (122.45, 101.6) rotated 180, with a GND via in its pad. A track joins its 3V3 pad to U3.5.
- **m9:** on J4 pads 29–36, the inboard end of the oval is 0.15 mm shorter. The gap to the RM2 pads is now 0.39 mm (was 0.24), with a 0.2 mm ring at the tip. The RM2 pads can't move, and the hole limits how far the pad can be clipped. Castellated.pretty was updated to match.
- **m11:** U5 is DNP and has no F.Paste on its pads. Custom.pretty was updated to match.
- **m13:** the pad 37 label is "40A0" on both sides; the front one uses a 0.8 × 0.55 font to stay clear of RM2 pad 8. The JP2/JP3 references are horizontal, above their boxes. The back "0" moved off JP1's box. The front "41A1" was left horizontal, because parts block the vertical slot.

The courtyard overlaps of the new tight placements are named pairs in `pico-stretch2.kicad_dru`. The D3/R2 pair was removed. All 22 named pairs are real overlaps.

Also from DESIGN_REVIEW_2.md M1: C13 moved 0.05 mm up, to (142.325, 96.025), so its 1V1 pad clears U1 pin 50 (3V3) by 0.177 mm instead of 0.127.

---

## Blockers

None found. As drawn, the board should power up, enumerate on USB, boot from flash and debug over SWD.

## Major

### M1. C9 and C15 carry an 0603 part number on 0402 footprints

- **What:**
  - C9 (100 nF, 3V3, at 135.79, 101.56) decouples U1 pins 68/69, USB_OTP_VDD and QSPI_IOVDD.
  - C15 (100 nF, RUN, at 167.31, 100.25) is the RUN capacitor.
  - Both have footprint `C_0402_1005Metric` but LCSC **C14663**, which is Yageo CC0603KRX7R9BB104, an **0603** part (jlcimport: "100nF 50V X7R ±10% 0603").
- **Evidence:**
  - Netlist digest bill: `C9, C15 | 100nF | C_0402_1005Metric | C14663 | CC0603KRX7R9BB104`.
  - The current `production/bom.csv` row is `"C15, C9",0402,2,100nF,C14663`.
- **Consequence:** JLC either stops the order at DFM review for a package mismatch, or places 1.6 × 0.8 mm parts on 0402 lands. That gives tombstoning or opens, at C9 in the middle of the U1 decoupling field. The placement preview checks rotation, not this.
- **Fix:** Set LCSC to **C1525** (CL05B104KO5NNNC, 0402, Basic, already used for 13 other capacitors) on both symbols and regenerate the BOM. Cost: none.

### M2. The cut-down (Pico-size) board works electrically, but sawing at x = 160.33 risks shorts and leaves SWD on sawn half-pads

What I checked, and what holds:

- I removed all copper right of x = 160.33 (and, for kerf, right of 159.83 and 159.6) and re-checked the connectivity of every net. No net on the kept side splits or loses a pad (`review/cutcheck.py`).
- Power works: USB1 → D1 → U3 → 3V3, the VREG/L1 regulator, and all decoupling except C21/C23/C24 (which serve the radio) are left of the line.
- Flash, crystal, BOOT and USB all survive.
- RUN keeps the RP2350's internal ~50 kΩ pull-up (Pico 2 datasheet, RUN description). Losing C15 and Reset1 is benign.
- Castellated pads 1–20 and 45–64 match the Pico pinout (README table, netlist J4).

What is wrong:

1. **Short risk at the sawn edge.**
   - The line crosses 22 F.Cu GPIO tracks (0.12 mm, about 0.1 mm gaps, y 93.6–97.2 and 105.6–108.2) and four B.Cu tracks: SWCLK, SWDIO, RUN, and **3V3 0.4 mm at y 105.36** (feeding the RM2).
   - Both inner GND planes run the full width with no pull-back. The board edge sits 0.21 mm of prepreg from the outer tracks.
   - A saw or rotary tool smears copper. A smear from the 3V3 track to In2 GND is a hard short: the ME6217 limits at about 350 mA, then thermal shutdown. A smear from RUN to GND holds the chip in reset. GPIO-to-GPIO or GPIO-to-GND smears are also possible.
   - Evidence: `review/cutcheck.py` crossing list; `board.json` In1/In2 GND fills to x 190.78; stackup prepreg 0.2104 mm.
2. **SWD.** The line runs through the centres of J2's three holes (x 160.35). The cut-down board keeps only sawn half-pads, about 0.8 × 1.7 mm with half a barrel, for SWCLK, GND and SWDIO. A wire can be soldered to them, but a header or pogo pins cannot be used.

- **Consequence:** A user following the README "saw it in half" option can end up with a dead board (3V3 or RUN shorted), with no indication why. The full-length board is unaffected.
- **Fix, cheapest first:**
  - **(a) Documentation, no layout change.** In the README, tell users to cut on the waste side of the line and sand the edge flat, never with a rotary tool at speed. Before powering, measure 3V3–GND, RUN–GND, SWCLK–GND and SWDIO–GND. Say that SWD becomes three edge half-pads.
  - **(b) Layout, about an hour.**
    - Add a ~1.2 mm keep-out band at x 159.75–160.95 on In1 and In2. Keep one GND bridge band (for example y 99.5–103.5, where no outer track crosses) so the radio half keeps its plane connection.
    - Move J2 left of the line, around x 157.5.
    - Move C15 to U1 pin 35.

---

## Minor

Ranked by consequence.

### m1. The Inner1 cut-out is narrower than RP2350 datasheet Fig. 27, and narrower than the fix applied to pico-stretch

- **What:** The "VREG_LX cut-out" rule area on In1 (commit cd2d11c) is (132.5–134.55, 97.45–99.05) plus a strip (…–137.3, 99.05–99.38). It covers L1's LX pad, the LX pour and the LX trace.
  - Fig. 27 (datasheet p.412) also removes layer-2 copper under the whole inductor, the VOUT pour and its vias, the CIN VIN pad, the COUT VOUT pad and the FB/VIN/LX pin traces. Only the GND pads and GND vias stay over plane.
  - On this board, In1 GND is still under L1 pad 2 (1V1, 132.63–134.23 × 99.69–100.69), the 1V1 pour and via (134.49, 100.18), and the C10/C12 supply pads.
  - The old pico-stretch board's cut-out (136.9–143.35 × 96.55–100.25) followed Fig. 27 in full.
- **Evidence:** `region.py In1.Cu` keep-out outline; `review/renders/in1_vreg_gpio47.png`; `ds/fig27.png`; `pico-stretch.kicad_pcb` zone "VREG_LX cut-out".
- **Consequence:** §6.3.8.3 says the leakage field in the LX → L → COUT loop affects the control loop, and RPi says deviations are "at your own risk". The datasheet's sentence ("cut away copper immediately underneath LX/VREG_LX") is met; its worked example is not. The effect size is unverified, but most likely small.
- **Fix:** Extend the rule area to about x 132.4–135.3, y 97.4–100.8, staying off the GND vias at (134.90, 98.72) and (135.87, 98.71) and off the C10/C12 GND pads. Then refill. One zone edit.

### m2. The D+ ESD diode D3 hangs off a 2 mm back-side stub through two vias

- **What:** USB2_D+ runs on F.Cu from USB1 pins 6/8 to R3's pad, where a via in the pad (119.48, 101.30) drops to B.Cu. A 2.0 mm B.Cu track runs up to a via in D3's pad (119.495, 99.25).
  - D− is routed through D2's pad in line.
  - The stub has been there since c014245. TP4 (new) sits on it.
  - The pico-stretch review moved D2/D3 in line ("D3's back-side route and its via-in-pad are gone"). That fix was not carried to pico-stretch2.
- **Consequence:** About 1.5–2.5 nH in series with the clamp. At the IEC 61000-4-2 contact rise (about 30 A in under 1 ns) that adds tens of volts at the tap. R3 (33 Ω) and the RP2350's own pad ESD stand between the tap and the chip, so this is margin, not a certain failure.
- **Fix:** Put D3 in line on F.Cu like D2 (there is room at about 119.5–120.5, 101.6–102.4), or route the D+ track through D3's pad. Delete the B.Cu stub and keep TP4 on a short spur.

### m3. With U6 fitted, PSRAM CE# sits below its VIH at power-up

- **What:** R14 (10 kΩ, 123.43, 96.39) pulls Net-(JP1-A) to 3V3. With JP1 or JP4 closed, GPIO0 or GPIO47 is "pulled low" at reset (RP2350 §9.3), and RPD is 36–113 kΩ at 3.3 V (Table 1683, p.1336).
- **Evidence:**
  - CE# = 3.3 × 36/46 = 2.58 V worst case, about 2.75 V typical.
  - APS6404L VIH min is VDD − 0.4 = 2.9 V (DC table, p.22).
  - §7 power-up asks CE# to track VDD within 200 mV for 150 µs.
- **Consequence:** Out of spec only while the pin is undriven (power-up, the bootrom's flash access on CS0). Most CMOS inputs read 2.6 V as high, so the real risk is low. It does not apply with U6 DNP.
- **Fix:** Change R14 to 1 kΩ (C11702, already on the BOM), giving 3.21 V worst case. BOM change only.

### m4. VBUS has no TVS and no capacitor; hot-plug ringing reaches the LDO

- **What:** The VBUS net is only USB1.2/11, D1.2 and J4.64. C37 (10 µF 0603 10 V) is on VSYS, after D1. There is no ESD part on VBUS or CC.
- **Consequence:** A long cable (about 1 µH) into about 5 µF effective capacitance can overshoot VSYS to roughly 6–8 V, depending on cable resistance. That is near or above the ME6217 limits: VIN max 6.5 V operating, 7.0 V absolute (ME6217 datasheet p.2, p.4). This is an estimate, not a simulation. The same topology works on many hobby boards. The issue was open on pico-stretch (m5).
- **Fix:** Add a 5 V unidirectional TVS (SOD-323 or SOD-523, standoff ≥ 5.0 V) from VBUS to GND at USB1, plus optionally a 1–4.7 µF VBUS capacitor. One or two parts.

### m5. VBUS and VSYS are 0.25 mm tracks with single 0.2 mm vias; VBUS runs under the USB-C shell

- **What:**
  - VBUS is 0.25 mm F.Cu everywhere: USB1 → D1, and → castellated pad 64.
  - VSYS is 0.254 mm B.Cu from via (120.15, 97.99) to via (119.33, 102.12), one via per transition.
  - A VBUS segment at x = 113.23, y 97.3–101.3 runs under the receptacle's metal shell (GND), with only solder mask between.
- **Evidence:** `power.py` ad hoc runs:
  - USB1:2 → J4:64 at 1.0 A gives 17 mV.
  - J4:63 → U3:1 at 0.5 A gives 16 mV, with 0.50 A in each single via.
  - pack `power.md` flags 4.3 A/mm on VBUS at 0.9 A.
- **Consequence:** Through the VSYS path, current is limited by the LDO, so this is fine. VBUS pass-through to a carrier is a different case: Pico users treat pin 40 as a 5 V source, and a USB-C charger can supply 1.5–3 A. At those currents the 0.25 mm track heats up (an IPC-2221 estimate is about 30 °C rise at 1.5 A).
- **Fix:** Widen VBUS to 0.5–0.8 mm where there is room and move the under-shell segment to B.Cu. Use two vias per VSYS transition. Or document a VBUS pin pass-through limit of about 1 A. About an hour of layout, or text only.

### m6. USB series resistors are 33 Ω at the connector end; the datasheet says 27 Ω near the chip

- **What:** R2 and R3 (119.99, 100.31 / 101.30) sit about 17 mm from U1 pins 66/67. The RP2350 pin table says "A 27 Ω series termination resistor is required on each pin". Hardware design §5.1 says "placed close to the chip".
- **Consequence:** Full speed (12 Mb/s) over 17 mm works. The source impedance is off-spec, so USB-IF eye compliance is not assured. This was previously left unchanged on pico-stretch (m3: 27 Ω C25100 is Extended; 33 Ω works on earlier boards).
- **Fix:** If wanted: 27 Ω (C25100) placed near U1, around (136, 100.6–101.2).

### m7. U1 land pattern: 100 % paste on the exposed pad, and short signal pads

- **What:**
  - Pad 81 is 3.4 × 3.4 mm with `solder_paste_margin 0`, so the aperture is a single full window over nine filled vias (0.63/0.30 at 141.17–143.46, 101.22–103.25).
  - Signal pads are 0.20 × 0.665 mm, spanning 4.575–5.24 mm from centre. Datasheet Fig. 150 (p.1327) gives 0.22 × 0.78 mm, spanning 4.507–5.287 mm.
- **Consequence:** Extra EP solder can float a 0.4 mm-pitch QFN and open or bridge peripheral joints, and short heels weaken the fillets. This is a yield risk, not a certainty. The same footprint was built on pico-stretch.
- **Fix:** Window-pane EP paste at about 60–70 % (four apertures). Optionally lengthen the signal pads toward Fig. 150. Footprint editor, about 30 minutes.

### m8. LDO output capacitance after DC bias

- **What:** C40 (CL05A106MQ5NUNC, 10 µF 6.3 V X5R 0402, at 122.78, 101.39) is the only bulk capacitor at the U3 output. At 3.3 V bias, a 0402 10 µF typically keeps about 30–45 %, roughly 3–4.5 µF (unverified against the Samsung curve).
- **Evidence:** ME6217 precautions item 3 asks for CL ≥ 4.7 µF (p.6), and its characterisation uses 10 µF. The rest of the 3V3 bulk is C12 (4.7 µF 0402, 13 mm away) and C24 (4.7 µF 0603, at the radio). The total on the net is probably adequate, but the local value is marginal under 271 mA RM2 bursts.
- **Fix:** Use the 0603 10 µF already on the BOM (C19702) at C40. There is room. Cost: none.

### m9. RM2 pads 1, 3, 5 and 6 sit 0.24 mm from castellated pads 33–36

- **What:** These are user-soldered joints with a 0.24 mm copper gap:

  | RM2 pad | Net | J4 pad | Net |
  |---|---|---|---|
  | U5.1 | GND | 33 | GPIO37 |
  | U5.3 | GPIO29 (radio clock) | 34 | GND |
  | U5.5 | GPIO24 | 35 | GPIO38 |
  | U5.6 | DO | 36 | GPIO39 |

  U5.16/17/19/21 are 0.34 mm from pads 29–32. (Measured from `board.json`; DRC passes at 0.09 mm.)
- **Consequence:** Hand-fitting the RM2, or soldering header pins into J4 33–36 with the RM2 fitted, bridges easily. A GPIO29–GND bridge silently kills the radio clock.
- **Fix:** Shorten the inboard end of J4's full-hole pads 33–36 (oval to round) for about 0.6 mm clearance, and keep the mask web. Footprint edit only.

### m10. The radio gSPI lines are long and run beside user GPIOs (carried from pico-stretch m8)

- **What:**
  - GPIO29 (radio SCLK) is 61 mm from U1.37 to U5.3. It passes castellated pad 24 and runs 30 mm beside GPIO30 at 0.248 mm centre spacing.
  - GPIO24 (data) is 57 mm.
- **Evidence:** pack `emc.md` (k ≈ 0.42).
- **Consequence:** The pack's "10 % NEXT" is the saturated figure. With a 30 mm coupled length (about 0.4 ns round trip) against 1–2 ns edges, the real coupled noise is about 3–5 %, roughly 100–150 mV. Margin is reduced, failure is unlikely at the SDK's default 31 MHz gSPI clock, and any load a user puts on pads 22/24 adds to the line. Not simulated.
- **Fix:** Optionally add a 22–33 Ω series footprint on GPIO29 at U1. Widen the GPIO29/GPIO30 spacing. In the README, note that pads 22 and 24 should stay unloaded when the radio is used.

### m11. U5 (RM2) is not DNP

- **What:** U5 is `in_bom yes` and not DNP, so it appears in `production/bom.csv` and `positions.csv` with no LCSC number. Its 21 pads are on F.Paste, so the stencil prints paste on them.
- **Consequence:** JLC shows an unmatched line. The reflowed solder bumps can keep a hand-fitted RM2 from sitting flat on its castellations.
- **Fix:** Mark U5 DNP. Optionally remove F.Paste from its pads, or keep it if pre-tinning is wanted.

### m12. Decoupling gaps

- IOVDD pin 15 (144.06, 107.11) has its nearest capacitor 3.5 mm away (C3). Pin 50 (142.46, 97.29) is 4.0 mm from C36. The other IOVDD, DVDD, VREG and QSPI pins have a capacitor within 0.1–1.5 mm (pad-edge distances).
- The PSRAM (U6) VDD has only C16 (100 nF, 0.6 mm). APS6404L §14.3 asks for a low-ESR 1 µF at VDD; this was not changed on pico-stretch (m7).
- **Fix:** Add or move a 100 nF to pins 15 and 50 if there is room, and add a 1 µF 0402 next to U6 pin 8.

### m13. Silkscreen

- **Collisions:**
  - Back: "JP2" overlaps the "25" pad label and "JP3" overlaps "23" (`review/renders/jp23.png`).
  - Back: the "0" label touches JP1's box.
- **Labels:**
  - Pad 37 reads "40" on both sides, while 38–44 read "41A1".."47A7". It should be "40A0".
  - The front "41A1" (175.38, 94.67) is horizontal and offset toward pad 39, unlike its neighbours.
- **Hidden under the radio:** the front pad labels for 29–39 and the front "pico Stretch" logo sit inside U5's body and are hidden when the radio is fitted. The back labels cover them.
- **DRC:** it cannot catch these, because `min_silk_clearance` is 0.
- **Checked fine:** all 64 back labels match the netlist and are correctly mirrored.
- **Fix:** about 15 minutes of text moves.

### m14. Back-side exposed copper vs mounting on a carrier

- **What:** JP1–JP4 and TP1–TP4 are exposed on B.Cu. TP3 and TP4 put USB D−/D+ on the underside.
- **Consequence:** A closed jumper's blob, or exposed test pads, can stop the board sitting flat on a carrier, or short to carrier copper.
- **Fix:** Add a carrier keep-out note to the README, next to the existing antenna note.

### m15. Documentation and firmware-visible items

- **ME6217 back-feed.** With 3V3 driven externally and 3V3_EN low, current flows through the PMOS body diode into VSYS. The datasheet says VOUT must not exceed VIN + 0.3 V (p.5). The README should say not to back-feed 3V3. On the Pico 2 that is allowed.
- **Pico 2 firmware assumptions do not hold.**
  - GPIO24 is radio data, not VBUS sense.
  - GPIO29 is the radio clock, and not an ADC pin on RP2350B, so there is no VSYS/3 reading.
  - GPIO25 is not an LED; the only LED is PWR_LED1 on 3V3.
  - VSYS must stay at or above about 3.5 V (an LDO, not a buck-boost).
  - Pico 2 projects that run from 2×AA or a sagging LiPo will brown out.
  - A board definition is needed: RP2350B, 16 MB W25Q128JV, CYW43 pins 23/24/25/29, no LED.
- **PSRAM on GPIO47 (JP4).** RP2350-E14 (A2 stepping only): the bootrom's `connect_internal_flash()` configures CS1 pads only on pin 0. Firmware must set GPIO47 to XIP_CS1 and clear its pad isolation itself. The silicon stepping JLC supplies under C42415655 is unknown (unverified).
- **ERC hygiene.** The schematic has:
  - 7 ERC errors, mostly symbol pin-type noise
  - hierarchical labels VREG_LX/VREG_FB in a root sheet
  - four 0.0127 mm wire stubs
  - two dangling no-connect flags

  U6 still uses the `ESP-PSRAM32` symbol, with the Espressif datasheet link; its pinout matches APS6404L. None of this is electrical, but it buries real ERC hits.
- **R6 (VREG_AVDD filter) layout.** R6 sits about 0.2 mm from the VREG_LX pour. Fig. 26 keeps R_FILT/C_FILT on the PGND side. The coupling into C11's 4.7 µF is tiny.

### m16. The USB-C shell slots are slightly shorter than the vendor's recommended layout (unverified)

- **What:** The footprint (identical to LCSC's) has 0.6 × 1.5 and 0.6 × 1.2 mm plated slots. The SHOU HAN drawing (`usbc.pdf` p.1) shows 1.7 and 1.4 mm.
- **Consequence:** Shell legs may bind. The same footprint was built on pico-stretch, so the risk is low.
- **Fix:** Lengthen the slots by 0.2 mm in the footprint.

---

## Accepted decisions (not findings)

- **Via-in-pad.** Order with epoxy-filled, capped vias. The board file's own `(filling no) (capping no)` settings do not drive JLC's process; the order option does.
- **ME6217 LDO running the RM2.** At USB power VSYS is about 4.7 V. At about 0.4 A peak (271 mA radio Tx plus MCU and flash) that is about 0.56 W in SOT-23-5, which is thermal shutdown territory if sustained. The README documents bursty-only transmit and VSYS ≥ 3.5 V. Short-circuit on the 3V3 pad is limited at about 350 mA (ME6217 p.4).
- **L1 (AOTA-B201610S3R3-101-T, C42411119).** Sourced by pre-order or consignment; 1,689 in global stock on 2026-10-29.
- **Named courtyard exemptions** in `pico-stretch2.kicad_dru`. I checked that the rule names pairs only and is not a blanket category.
- **Fabrication Toolkit Auto Translate ON.** Rotations were confirmed in JLC's placement preview (coordinator, 2026-10-29), so they are not reviewed here.

## Checked and found fine

- **DRC and parity:** with zones refilled, 0 errors, 0 unconnected and parity 0. There are 5 warnings, all `lib_footprint_mismatch` (C37, R3, C39, USB1, J2). For USB1, the pads are identical to the library; only their order differs.
- **Saved fills:** they match a fresh refill, per the adversarial check.
- **RP2350B symbol:** all 81 pins match datasheet Fig. 3 (QFN-80): QSPI 70–75, USB 66/67, VREG 61–65, DVDD 10/32/51, eight IOVDD, ADC_AVDD 59. The footprint numbers counter-clockwise from pin 1 at the bottom-left of the rotated package.
- **RP2350 regulator vs §6.3.8 / Fig. 26, item by item:**
  - The layout is a true rotation of Fig. 26 (not mirrored): AVDD, PGND, LX, VIN and FB run top to bottom.
  - CIN (C12) is between VIN and PGND. COUT (C10) is beside it.
  - The LX trace passes between both capacitors' pads, as in the figure.
  - L1's dot (footprint silk/fab dot at pad 2) is on the 1V1/VOUT end, matching Fig. 28's current direction.
  - The PGND/CIN/COUT island reaches the plane through exactly two adjacent vias (134.90, 98.72 and 135.87, 98.71).
  - CFILT (C11) has its own via (135.63, 97.73).
  - FB is taken from the C10 output.
  - All parts are on the top side.
  - The second 4.7 µF (C5) is at DVDD pin 10.
  - The values match: 33 Ω + 4.7 µF on AVDD, 4.7 µF 0402 CIN and COUT.
  - The cut-out's extent is m1.
- **JP4/GPIO47 link on In1 (8e0d15f):**
  - It is crossed on F.Cu only by 3V3 (tracks and pour), RUN and ADC_VREF, all static, exactly as the commit says. On B.Cu, GPIO26–28 cross it, and they reference the unbroken In2.
  - In2 is 93 % solid under the link.
  - `board_diff` c014245 → HEAD shows only the intended changes: JP4, TP3, TP4 and their tracks, the In1 rule area, silk, and the logo moved. No footprints moved.
- **Power:**
  - D1 OR-ing (VSYS cannot back-feed VBUS). 3V3_EN is pulled to VSYS by 100 kΩ; CE is active-high and ≤ VIN.
  - The ADC_VREF network (200 Ω, 1 Ω, 4.7 µF) is equivalent to the Pico 2's.
  - DC drops at 15.2 µm inner copper:
    - 3V3 from U3 to the RM2: 28 mV with all loads (RM2 0.35 A, 3V3 pad 0.3 A).
    - 3V3 to U1: 11 mV.
    - 1V1 from L1 to DVDD: 5 mV at 0.2 A.
    - Ground return: < 2 mV.
- **Planes:** In1 and In2 are each one GND piece (80.6 % and 81.2 %). The only inner track is the GPIO47 link. There are 93 edge stitching vias with no gap over 10 mm, and no weakly stitched pieces. Copper is at least 0.5 mm from the board edge except at the castellations.
- **Signals:**
  - **Data direction:**
    - QSPI: SD0 → DI/SI, SD1 → DO/SO, SD2/SD3 → IO2/IO3, SCLK, and SS → U4 CS# (BOOT via 1 kΩ).
    - gSPI matches RM2 Table 1/2: 29 → SCLK, 24 → DI direct, DO via 470 Ω, nIRQ via 10 kΩ, 25 → JP2 → CS, 23 → JP3 → WL_ON + BT_ON, with pull-downs on the radio side.
  - **USB pair:** over In1 on F.Cu, skew 0.13 mm. TP3/TP4 stubs are about 2 mm, negligible at full speed.
  - **Edge distance:** no fast net within 1 mm of the edge.
  - **Crystal:** ABM8-272-T3, 12 MHz, CL 10 pF, with 15 pF caps and a 1 kΩ XOUT resistor, as in Hardware design §4. Pins 1/3 are the crystal and 2/4 are GND.
  - **Layer changes:** QSPI layer changes keep a GND reference (In1 ↔ In2 are both GND), with the nearest return via 1.2–2.8 mm away.
- **Part pinouts and lands:** ME6217C33M5G SOT-23-5 (1 VIN, 2 VSS, 3 CE, 5 VOUT); W25Q128JVSIQ in 208 mil SOIC; APS6404L-3SQR (3.3 V, 150 mil); DFLS130L (cathode = VSYS); RClamp0521P; and USB-C (CC1/CC2 each 5.1 kΩ, shell to GND, A/B pin order). The K2-1808SN pairs (1–2 and 3–4) agree with the LCSC symbol and the drawing's circuit diagram, so Boot1 and Reset1 switch correctly.
- **RM2 footprint:** it matches RM2 datasheet Fig. 6/7. The RF keep-out starts at x 190.71; inner GND ends at 190.78 (a 0.07 mm sliver, negligible) and the board edge is at 191.41. The README covers carriers.
- **Sourcing:** all 26 LCSC numbers resolve with stock. The low ones are L1 (1,689, accepted), X1 ABM8-272-T3 (890) and RP2350B (2,444). There are 9 Extended parts.
- **Production files (current, 11:46):**
  - U6 is excluded from the BOM and CPL.
  - Only top-side parts are placed.
  - The BOM rows match the schematic apart from M1 and m11.
  - The GPIO47 track on Inner1 in the gerbers was confirmed by the user and not re-plotted by me.
- **Back silkscreen:** all 64 castellation labels are correct and mirrored, and TP labels D−, D+, 3v3 and 1v1 are correct (README matches).
- **No missing 3D models or courtyards** (`board_lint`).

## Limits of this analysis

- **DC only.** There is no AC impedance, ringing, thermal model or RF evaluation. Hot-plug overshoot (m4), gSPI coupling (m10), EP paste float (m7), MLCC DC-bias values (m8) and ESD stub voltage (m2) are estimates, not simulations or measurements.
- **Crosstalk:** the pack's NEXT column is the saturated figure. For these short runs (well under the rise-time length) the real values are 3–5 times smaller. The hot-loop table cannot represent the regulator's LX → L → COUT loop, so §6.3.8 was checked by hand against Fig. 26/27.
- **Other pack quirks:** `emc.md` treats the In1 GPIO47 track as referenced to F.Cu ("10 mm over void"). Its real return is In1 GND either side of the slot, plus In2. The pin audit's "no LED resistor" is wrong: R12 is 2 kΩ, about 0.7 mA.
- **Load currents** in the power runs are datasheet or Pico-spec figures, not measurements.
- **Not verified:**
  - USB-C leg dimensions against a physical part.
  - The K2 switch's internal pairing beyond the drawing.
  - The RP2350B stepping JLC will ship.
  - 3D clearances.
  - Gerber content beyond what the user reported.
- **Design checks are not qualification.** Electrical, thermal, reflow and RF behaviour on real hardware still need a built board.

## Files

- `review/pack/`: the analysis pack's reports. That is `netlist.md`, `power.md`, `emc.md`, `drc.md`, `board_overview.md`, `adversarial_review.md` and `review_config.json`. The large JSON dumps were left out.
- `review/cutcheck.py`: the connectivity check for the Pico-footprint cut-down board.
- `review/boarddump_patched.py`: a copy of kicad-board-review's `boarddump.py`, patched to write standard layer names (F.Cu, In1.Cu, ...) so `emc.py` runs on this board. See jvanderberg/kicad-skills#4.
- `review/renders/`: `usb_fcu.png`, `usb_bcu.png`, `vreg_fcu.png`, `in1_vreg_gpio47.png`, `front_silk_L.png`, `front_silk_R.png`, `back_silk_L.png`, `back_silk_R.png` and `jp23.png`.
- Datasheet figures (`ds/fig26.png`, `fig27.png`, `fig28.png`, `fig150.png`) are not copied. They are Figures 26–28 and 150 of the RP2350 datasheet.
