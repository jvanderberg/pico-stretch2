# Pico Stretch 2: adversarial review

Scope: /Users/joshv/git/pico-stretch2 at HEAD 8e0d15f (only production/ differs in the working tree). Read-only. My own scripts, renders and data are in `review/adv/` and `review/advscripts/`. Datasheet citations use the PDF page numbers printed on the page.

Not re-reported (already accepted or already found): via-in-pad, the LDO running the RM2, L1 sourcing, the named courtyard exemptions, Auto Translate, stale production/ and images/, C9/C15 = C14663 (0603) on 0402 footprints, the RP2350B pin map, the L1 dot orientation, and the claim that no net loses connection on the cut-down board.

**Result: no Blockers. 1 Major, 15 Minor.** The board should power up, enumerate and boot as drawn. The Major is the advertised "saw it in half" option. Most Minors are cheap BOM or layout edits.

---

## Blocker

None found.

## Major

### M1. Sawing at x = 160.33 cuts J2 and leaves bare inner GND planes 0.21 mm from 3V3 and RUN

- **What:** The front silk cut line at x = 160.33 runs through the centres of the three J2 plated holes: SWCLK (160.35, 98.91), GND (160.35, 101.45) and SWDIO (160.35, 103.99). It also crosses:
  - 22 F.Cu GPIO tracks at y 93.61–97.15 and 105.56–108.19. These are 0.12 mm wide on a 0.22–0.25 mm pitch, so about 0.1 mm gaps.
  - 4 B.Cu tracks: SWCLK (y 98.91), RUN 0.15 mm (y 97.51), SWDIO (y 103.99) and **3V3 0.4 mm (y 105.36)**.
  - Both inner GND pours. In1 and In2 run the full width (y 91.49–111.49) with no pull-back at the cut.

  Right of the line, and so lost, are C15 (the only RUN capacitor, at 167.31, 100.25), Reset1, U5 and all of SWD.
- **Evidence:**
  - My `advscripts/cross.py` run lists the crossing tracks, pads and zones.
  - From `board.json`: J2 pin x = 160.35, In1/In2 fill bounds x 109.65–190.78.
  - Stackup: B.Cu to In2 is 0.21 mm of prepreg, F.Cu to In1 is the same.
- **Consequence:**
  - A saw or Dremel cut smears copper across 0.21 mm of prepreg. It can join the B.Cu 3V3 track to In2 GND (a dead short on the 3V3 rail), or RUN to GND (the chip is held in reset). Smears between the 0.1 mm-spaced F.Cu GPIO stubs are also likely.
  - SWD is destroyed: no SWD pads remain on the cut board, whereas the Pico has them.
  - RUN loses its 100 nF capacitor and the reset button.

  The lead reviewer's check (connectivity only) does not cover any of this.
- **Fix (cheap, layout only):**
  1. Add a keep-out rule area about 1.2 mm wide (x 159.75–160.95) on In1 and In2 so no plane copper reaches the kerf. Pads 20/45 end at 159.91, so check the pour still reaches the GND pads at x ≤ 158.
  2. Move J2 left (around x 157.5, between X1 and pad 20/45) so it survives the cut.
  3. Move C15 next to U1 pin 35 (147.17, ~100.4).
  4. Route the RM2 3V3 feed and RUN across the line on F.Cu, or accept them and say so.
  5. In the README, tell users to dress the sawn edge and to measure 3V3–GND and RUN–GND before powering.

  Cost: about an hour of layout, no BOM change.

## Minor

### m1. PSRAM CE# pull-up R14 (10 kΩ) cannot hold CE# at a valid high against the RP2350 default pull-down

- **What:** R14 at (123.43, 96.39) pulls Net-(JP1-A) to 3V3. With JP1 or JP4 closed, GPIO0 or GPIO47 sits at its reset-default pull-down: RPD is 36–113 kΩ at IOVDD = 3.3 V (RP2350 datasheet, GPIO DC table, p.1336). The hardware design guide confirms GPIO0 is pulled low at power-up (§3.2).
- **Evidence:**
  - CE# = 3.3 V × 36/(36 + 10) = 2.58 V worst case, about 2.75 V typical.
  - APS6404L VIH min is VDD − 0.4 V = 2.9 V (DC table, p.21).
  - Power-up §7 requires CE# to "track VDD within 200 mV" for 150 µs.
- **Consequence:** CE# is out of spec during power-up and during the bootrom's flash probe on CS0. The PSRAM may treat flash traffic as its own and drive SIO. This only applies when U6 is fitted. A CMOS input will usually read 2.75 V as high, so the real risk is low, but it is a datasheet violation.
- **Fix:** Change R14 to 2.2 kΩ (C25879) or 1 kΩ (C11702, already in the BOM). That gives 3.11 V or 3.21 V worst case. BOM-only change.

### m2. The In1 cut-out is smaller than RP2350 datasheet Figure 27

- **What:** The keep-out covers L1's LX pad, the LX pour and a 0.33 mm strip under the LX trace: (132.5–134.55, 97.45–99.05) plus (…–137.3, 99.05–99.38). Figure 27 (p.412) removes layer-2 copper under the whole inductor (both pads), the VOUT pour and its vias, the COUT VOUT pad, the CIN VIN pad and the FB/VIN/LX pin traces. Only the GND pads and vias stay over plane.
- **Evidence:** `adv/vreg_in1.png` shows In1 GND still present under L1 pad 2 (132.63–134.23, 99.69–100.69), the 1v1_VREG pour and the C10/C12 inner pads.
- **Consequence:** §6.3.8.3 says leakage field coupling in the LX→L→COUT loop affects regulation. Eddy currents in the plane under the inductor's 1V1 half change that coupling compared with the verified Pico 2 layout. Effect size is unverified.
- **Fix:** Extend the keep-out polygon to roughly x 132.4–135.3, y 97.4–100.8. Keep it off the GND vias at (134.90, 98.72) and (135.87, 98.71) and the C10/C12 GND pads, as in Figure 27. One zone edit, then refill.

### m3. USB series resistors are 33 Ω at the connector end; the datasheet requires 27 Ω, and the guide places them near the chip

- **What:** R2 and R3 are at (119.99, 100.31) and (119.99, 101.30), which is 5–6 mm from USB1 and about 17 mm from U1 pins 66/67.
- **Evidence:**
  - RP2350 datasheet pin table (p.11): "A 27 Ω series termination resistor is required on each pin". The same is on p.1333.
  - Hardware design guide §5.1: "27 Ω … placed close to the chip".
  - The 17 mm chip-side pair is 0.15 mm wide at a 0.35 mm pitch over In1 at 0.21 mm. The pack estimates about 82 Ω single-ended, roughly 120 Ω differential.
- **Consequence:** Full speed will almost certainly work, but the source impedance and placement are off-spec.
- **Fix:** Use 27 Ω (0402WGF270JTCE, C25100). Ideally move R2/R3 next to U1, where there is room around (136, 100.6–101.2). The BOM change is trivial; the move is about 30 minutes of layout.

### m4. U1 land pattern and paste: 100 % paste on the exposed pad, and pads shorter than Figure 150

- **What:**
  - Pad 81 (EP) is 3.4 × 3.4 mm with `solder_paste_margin 0`, so the aperture is one full window. Nine filled, capped vias in it stop any wicking.
  - Signal pads are 0.20 × 0.665 mm, spanning 4.575–5.24 mm from centre. Datasheet Figure 150 (p.1327) recommends 0.22 × 0.78 mm spanning 4.507–5.287 mm, so the board has almost no heel extension.
- **Consequence:** Extra EP solder can float the 0.4 mm-pitch QFN and open peripheral joints. The short heel reduces fillet inspection and strength. JLC builds this LCSC footprint routinely, so this is a yield risk, not a certain failure (unverified).
- **Fix:** Give the EP four windowpane paste apertures at about 60–70 % coverage (custom F.Paste shapes, paste margin −). Optionally lengthen the signal pads toward Figure 150. About 30 minutes in the footprint editor.

### m5. VBUS and VSYS are 0.25 mm tracks with single 0.2 mm vias, and VBUS runs under the USB-C shell

- **What:**
  - VBUS from USB1 pins 2/11 to D1 and to castellated pad 64 is 0.25 mm F.Cu throughout: (113.2, 95.1)→(117.3, 95.1), and (113.23, 97.33)→(113.23, 101.26)→(115.43, 103.46).
  - VSYS from D1 to U3 is 0.25 mm B.Cu through one via at each end, (120.15, 97.99) and (119.33, 102.12).
  - The VBUS segment at x = 113.23, y 97.3–103.5 lies under the receptacle's metal (GND) shell, with only solder mask between.
- **Evidence:**
  - `region.py` output.
  - My solve: `power.py --net VBUS --source USB1:2 --source USB1:11 --sink J4:64=1.5` gives 25 mV and 0.53 A in the busiest via.
  - IPC-2221 gives about 34 °C rise at 1.5 A on 0.25 mm of 35 µm copper.
- **Consequence:** Pico users treat the VBUS pin as a pass-through from the USB source (the connector is rated 3 A). Above about 1 A the track heats noticeably. A VBUS-to-shell short through damaged mask is possible.
- **Fix:** Widen VBUS and VSYS to ≥ 0.5 mm where room allows. Use two vias per VSYS layer change. Move the under-shell VBUS run to B.Cu, which is empty there apart from TP3. About an hour of layout.

### m6. VBUS has no capacitor or TVS; hot-plug ringing lands on VSYS

- **What:** The VBUS net is only D1.2, J4.64 and USB1. C37 (10 µF 0603 10 V) and C39 sit after D1.
- **Consequence:** With about 1 µH of cable and the roughly 6 µF effective of C37 at 5 V, the estimated overshoot is about 6.1–6.5 V, which D1 holds on VSYS. That is close to ME6217 VIN max of 6.5 V operating / 7 V absolute (datasheet p.2, p.4). There is also no ESD protection on VBUS or CC.
- **Fix:** Add a 5 V TVS on VBUS (for example SMF5.0A, or a small 0402/SOD-523 unidirectional 5 V part) near USB1. One part.

### m7. LDO output capacitance is below the ME6217 recommendation after DC bias

- **What:** C40 is CL05A106MQ5NUNC (10 µF, 6.3 V, X5R, 0402) at (122.78, 101.39). At 3.3 V it keeps roughly 30–40 %, about 3–4 µF. The next bulk capacitors are C12 (4.7 µF 0402, 13 mm away) and C24 (4.7 µF 0603, at the radio).
- **Evidence:** ME6217 precautions item 3 (p.6) asks for CL ≥ 4.7 µF; its characterisation uses CL = 10 µF (p.4). The RM2 transmits in 271 mA bursts (RM2 datasheet §1.1).
- **Fix:** Change C40 to the 0603 10 µF already in the BOM (C19702) or a 10 V 0402. BOM plus footprint swap; there is room at (122.8, 101.4).

### m8. RM2 pads 1, 3, 5 and 6 sit 0.24 mm from castellated pads 33–36

- **What:** These are hand-fitted joints with a 0.24 mm gap:

  | RM2 pad | Net | J4 pad | Net |
  |---|---|---|---|
  | U5.1 | GND | 33 | GPIO37 |
  | U5.3 | GPIO29 (radio SCLK) | 34 | GND |
  | U5.5 | GPIO24 | 35 | GPIO38 |
  | U5.6 | DO | 36 | GPIO39 |

  U5.8 is also 0.19 mm from R16.2.
- **Evidence:** My `advscripts/gaps.py` run. U5 pads end at y 93.69; the J4 full-hole pads end at 93.45.
- **Consequence:** Soldering the RM2 by hand, or soldering header pins into J4 33–36 with the RM2 fitted, can easily bridge. A GPIO29–GND bridge kills the radio clock.
- **Fix:** Shorten the J4 full-hole pads 33–36 on their inboard side. An oval to round pad on those four gives about 0.6 mm. Add a solder-mask dam. Footprint edit only.

### m9. The gSPI radio lines are long, unterminated and tightly coupled to user GPIOs (unverified)

- **What:**
  - GPIO29 (SCLK) is 61.1 mm from U1.37 to U5.3. It passes through castellated pad 24 at 32.5 mm and has one layer change.
  - GPIO24 (data) is 57 mm, with castellated pad 22 at 19.5 mm.
  - GPIO29 runs 30 mm beside GPIO30 at about 0.13 mm gap (k ≈ 0.42, about 10 % NEXT). GPIO24 runs beside GPIO25 and GPIO23 (pack emc.md crosstalk table).
- **Evidence:** My `advscripts/topo.py` run.
- **Consequence:**
  - The SCLK edges see a mismatched line with a mid-line stub. Any wire a user attaches to pads 22 or 24 adds load.
  - The read path (DO → 470 Ω → 46 mm → U1) has an RC of roughly 5–6 ns, against 16 ns half-periods at 31.25 MHz.
  - Pico 2 W and RM2 reference routes are much shorter.
  - Toggling GPIO30 couples into SCLK.

  This is unlikely to fail at the SDK default clock, but margin is reduced. Not simulated.
- **Fix:** Add a 0402 series resistor footprint (22–33 Ω) on GPIO29 at U1. Increase GPIO29/GPIO30 spacing to ≥ 0.3 mm, or put a GND guard between them. Note in the README that pads 22 and 24 should stay unloaded when the radio is used.

### m10. README assembly checklist misses L1, the most orientation-critical part

- **What:** The README says "Check pin 1 of U1, U3, U4 and the diodes". It does not mention L1, which per RP2350 datasheet §6.3.8.3 (p.413) must be the right way round. It also omits PWR_LED1 and X1. With Auto Translate on and EasyEDA footprints, JLC's rotation for L1 is not guaranteed.
- **Fix:** Add "L1 dot toward the 1V1 pad (toward C10), LED cathode, X1 pin 1" to the README and to the order-time check. Text only.

### m11. Back-side jumpers and test pads interfere with surface-mounting on a carrier

- **What:** JP1–JP4 and TP1–TP4 are exposed copper on B.Cu. A closed jumper's solder blob stands about 0.2–0.5 mm proud. TP3 and TP4 (added in 7b352e1) expose USB D−/D+ on the underside.
- **Consequence:** When the board is used as a castellated module on a carrier (which the README describes for the RM2 case), the blob stops the board sitting flat and the pads can short to carrier copper. The Pico datasheet handles its back-side test points with a carrier keep-out.
- **Fix:** Document a carrier keep-out (no exposed copper under JP1–4 and TP1–4) in the README. Optionally use jumpers on F.Cu for future revisions.

### m12. Back silkscreen collisions and a missing ADC label

- **What:**
  - The "JP2" reference overlaps the "25" pad label, and "JP3" overlaps "23" (around x 166–163, y 107–109).
  - The "0" label at (110.3, 109.46) touches JP1's silk box.
  - "VBUS" crowds the USB shell pad opening at about (110.3, 96).
  - Pad 37 is labelled "40" on both sides, while 41–47 read "41A1".."47A7". It should read "40A0" (README: GPIO40/ADC0).

  The DRC did not flag the overlaps because `min_silk_clearance` is 0.
- **Evidence:** `adv/back_l_m.png`, `adv/back_r_m.png`, `adv/jp23.png`, `adv/front_r.png`.

  I checked every back label against the netlist; all 64 are correct, and the mirroring is correct.
- **Fix:** Move the JP2/JP3 references above their boxes, nudge the JP1 box or the "0", and add "A0". 15 minutes.

### m13. U5 is not DNP: it reaches the BOM and CPL with no LCSC part and gets a paste stencil

- **What:** U5 has `in_bom yes`, `dnp no` and pads on F.Paste (`advscripts` grep). The working-tree production/bom.csv includes it with no LCSC number.
- **Consequence:** JLC shows an unmatched part. The stencil prints paste on 21 bare pads, and the reflowed bumps stop a hand-fitted RM2 from sitting flat.
- **Fix:** Mark U5 DNP and remove F.Paste from the U5 footprint pads. Two clicks.

### m14. USB-C shell slots are shorter than the vendor layout (unverified fit)

- **What:** The USB1 footprint (identical to the LCSC original) has slots of 0.6 × 1.5 and 0.6 × 1.2 mm, pads of 1.1 × 2.0 and 1.2 × 1.8, and 0.70 mm NPTH holes. The SHOU HAN drawing (usbc.pdf p.1, "Recommended PCB layout") shows 1.70 and 1.40 mm slots, 2.10 and 1.80 mm pads, and Ø0.65 pegs.
- **Consequence:** Shell legs may bind in 0.2 mm-shorter plated slots, especially after plating build-up. This footprint is widely used, so the risk is low.
- **Fix:** Lengthen the slots to 0.6 × 1.7 and 0.6 × 1.4. Footprint edit only.

### m15. Small layout and documentation items

- The VREG_AVDD filter (R6 at 133.68, 97.12) sits 0.2 mm from the VREG_LX pour and the L1 LX pad. In Figure 26 (p.411), R_FILT/C_FILT are on the PGND side away from LX. The coupling is tiny into C11's 4.7 µF, but it is a deviation from "avoid anything that might couple noise into VREG_AVDD" (§6.3.8.1).
- ME6217 back-feed: with 3V3 driven externally and 3V3_EN low, current flows through the PMOS body diode into VSYS. That violates "VOUT ≤ VIN + 0.3 V" (p.2, p.5). The README should say 3V3 must not be back-fed.
- U6 still uses the `Memory_RAM:ESP-PSRAM32` symbol, with SCLK typed as output (ERC noise). The pinout happens to match the APS6404L (APS datasheet p.3).

---

## Problems with the analysis pack

1. **power.md `vbus` run** omits J4:64 (the VBUS pin pass-through) as a sink. That hides the 0.25 mm VBUS bottleneck (m5). The flagged hotspot "F.Cu 4.3 A/mm @116.6, 98.6" is that track, but it is not called out.
2. **`vsys` 0.9 A** cannot happen: the ME6217 in SOT-23-5 thermally limits near 0.35 A from 4.7 V. This is conservative for copper but misleading as a load case.
3. **emc.md treats In1.Cu tracks as referenced to F.Cu** (a signal layer, 0.21 mm away). That produces "GPIO47 10 mm over void". The real return is the coplanar In1 GND either side of the slot, plus In2 at 1.06 mm.
4. **The hot-loop table cannot represent the regulator loop** (LX → L1 → C10 → PGND). The "1V1/COUT" rows are DVDD decoupling caps, and the CIN rows list C38/C40 at 13–15 mm. Do not read it as a check of §6.3.8.
5. **The pin audit "LED series resistor: none found"** is wrong. PWR_LED1 + R12 (2 kΩ) on 3V3 exists and works out to about 0.7 mA.
6. **drc.md**: `min_silk_clearance` is 0 and 7 checks are ignored (courtyard, PTH/NPTH in courtyard, among others). A clean DRC therefore says nothing about silk collisions (m12) or the USB/D1 3D overlap.
7. **No check of the cut line** (inner planes and tracks at the kerf), or of exposed pads next to user-soldered RM2 pads.
8. **Cosmetic**: about 40 zero-length or near-zero track stubs (for example GPIO24 0.09 mm at 177.27, 96.57). Harmless.

## Checked and found fine

- **Recent commits:**
  - JP4/GPIO47: the In1 track is crossed on F.Cu only by 3V3 ×3, RUN and ADC_VREF (all static), and on B.Cu by GPIO26–28, which reference the unbroken In2. This matches the commit claim.
  - The In1 slot (12.5 × 3.6 mm) is benign. JP4 is 1.4 mm from U6.1, so there is no stub when JP1 is used. The JP1 stub is 20.8 mm when JP4 is used, which is fine for CS.
  - TP3 and TP4 stubs are about 2 mm and about 0.2 pF; negligible at full speed.
  - Saved zone fills equal a fresh refill (`advscripts/fillcmp.py`), so the gerbers will not carry stale pours.
- **RP2350 §6.3.8 item by item:**
  - VREG_AVDD is filtered by 33 Ω + 4.7 µF (R6/C11), and C11 has its own GND via (135.63, 97.73).
  - The CIN/COUT/PGND island joins the plane only through 2 adjacent vias (134.90, 98.72 and 135.87, 98.71).
  - All regulator parts are on the top side.
  - FB is taken from the COUT pour, away from L1.
  - The second 4.7 µF (C5) is at the bottom-edge DVDD pin 10.
  - The layout is a proper rotation (not mirrored) of Figure 26.
  - LX shares only the In1 strip; In2 is solid, which shields the B.Cu RUN/GPIO27/28 under L1. In2 and B.Cu do not need cut-outs.
- **Parts against datasheets:**
  - ME6217: SOT-23-5 pinout, CE active high pulled to VSYS by 100 kΩ, CE ≤ VIN + 0.3 satisfied, C33M5G suffix.
  - W25Q128JVSIQ: SOIC-208, QE handled by the bootrom, no CS pull-up needed per the HW guide §3.1.
  - APS6404L-3SQR: 3.3 V SOP-8 and pinout.
  - DFLS130L: the land pattern matches the suggested PowerDI-123 (1.05/2.4/0.65 mm) and the cathode is the large pad (VSYS).
  - RClamp0521P: bidirectional, 0.25 pF, 5 V VRWM.
  - ABM8-272-T3: 12 MHz, CL 10 pF with 15 pF caps plus 1 kΩ XOUT resistor as on Pico 2; land 1.4 × 1.1 vs 1.4 × 1.2 is OK; pins 1/3 are the crystal.
  - USB-C: signal pin order and positions (A1/B12 at ±3.2, VBUS ±2.4, 0.5 pitch), CC1/CC2 each 5.1 kΩ, shell to GND.
  - K2-1808SN: from the drawing's circuit diagram, the internal pairs run along the 4.4 mm pad axis (pads 1–2 and 3–4). So Boot1 (1/2 = BOOT, 3/4 = GND) and Reset1 (2 = RUN, 3/4 = GND) switch correctly, and the land is close to 5.2/3.1 × 2.8/1.5. The diagram's orientation is inferred.
  - RM2 (datasheet Figure 6/7): the footprint matches (14.5 × 16.5, 1.5 pitch, 2.0 × 1.0 pads with 0.5 overhang, pad 8 at 2.75, pad 7 at 1.8), numbering is counter-clockwise and not mirrored, and Table 2 connections are right. The RF keep-out starts at x = 190.71; inner GND stops at 190.78 (0.07 mm, negligible) and the board ends at 191.35.
- **Serial and memory lines traced driver to receiver:**
  - QSPI SD0 → DI/SI, SD1 → DO/SO, SD2/SD3 → IO2/IO3, SCLK, SS → U4 CS#.
  - gSPI: 29 → SCLK; 24 → DI direct, DO via 470 Ω, nIRQ via 10 kΩ; 25 → JP2 → CS; 23 → JP3 → WL_ON + BT_ON.
  - USB D± through R2/R3, SWD pin order, crystal.
- **Power:**
  - D1 OR-ing.
  - The ADC_VREF network (200 Ω/1 Ω/4.7 µF) matches Pico 2.
  - 3V3 drop to the RM2 is 28 mV and 1V1 drop is 5 mV (pack).
  - A short on the 3V3 pad is limited by the ME6217's 350 mA limit and thermal shutdown.
- **Castellations and silk:**
  - Castellated pinout matches Pico for pads 1–20 and 45–64, with 17.78 mm row spacing.
  - Every back label matches the netlist and is correctly mirrored.
- **Sourcing:** jlcimport, global stock. All LCSC numbers resolve. Low-stock items: L1 C42411119 (1,689, accepted), X1 C20625731 (885), RP2350B (2,444).

## Could not verify

- JLC placement rotations and polarity (L1, LED, U1, X1, D1) under Auto Translate. This needs the JLC preview.
- 3D or body clearance for USB1/D1 and the R4 courtyard overlaps.
- Real USB-C shell leg dimensions (m14).
- The K2 internal pairing beyond the drawing (it is consistent with the v1 build).
- gSPI timing and ringing (m9), EP paste float (m4), hot-plug overshoot (m6). These are estimates; none were simulated or measured.
- RM2 antenna detuning from the nearby GND vias at x ≈ 190.0, which are inside the module footprint and outside the keep-out.
