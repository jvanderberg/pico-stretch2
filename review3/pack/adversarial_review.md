# Adversarial review 3: vias (pico-stretch2 @ 1d4354a)

Scope: the committed board (`pico-stretch2.kicad_pcb`, `.kicad_pro` and `.kicad_dru` are unchanged from HEAD 1d4354a; the pack's `proj/` copy is byte-identical). Review only. All tool runs were on copies in `/tmp/psr3/adv/`:

- `scripts/via_geom.py` gives per-via pads, overhang, hole-to-hole, per-layer clearance, plane coverage and edge distance (output in `via_geom.json`).
- `pcb_vias.py` (pcbnew) gives flashing, tenting, net class and design-setting defaults.
- `court.py` lists vias under component courtyards.
- `viacalc.py` holds the barrel R, dT, Onderdonk and inductance models.
- `check.sh` was run on the baseline (`chk_base/`) and on a copy with every 0.4/0.2 via resized to 0.45/0.2 (`chk_045/`).

JLC sources (fetched 2026-10-31):

- https://jlcpcb.com/capabilities/pcb-capabilities (saved text in `/tmp/psr3/adv/dl1/cap.txt`)
- https://jlcpcb.com/news/free-via-in-pad-6-20-layer-pcbs-pofv
- https://jlcpcb.com/help/article/In-what-cases-will-there-be-charged-extra
- https://jlcpcb.com/blog/via-aspect-ratio-critical-pcb-reliability

## Via inventory (235)

| Class (dia/drill) | Count | In a pad | Not in a pad | Nets |
|---|---|---|---|---|
| 0.40/0.20 | **87** | 42 | 45 | GND 53; QSPI_SD0..3, SCLK, QSPI_SS 12; 1V1 4; VSYS 2; 3V3 2; RUN 2; 3V3_EN 2; Boot1 2; GPIO47 2; USB2_D+/- 2; SWCLK, SWDIO, GPIO24, JP1-A 1 each |
| 0.45/0.20 | 139 | 27 | 112 | GND 114; 1V1 5; 3V3 3; RUN 2; GPIO24 2; GPIO16-22, 26-29, JP2-A, JP3-B 1 each |
| 0.63/0.30 | 9 | 9 (U1 EP) | 0 | GND |

- **Via types:** all are through vias (F.Cu to B.Cu). All flash pads on In1/In2: no unused-pad removal.
- **Tenting:** every via is tented on both sides (board `tenting front/back yes`, no per-via override). Neither mask Gerber has a via aperture.
- **Via-in-pad:** 78 vias sit in pads: 69 in SMD pads plus 9 in the U1 EP, matching `board_lint`'s 69 "VIA IN PAD". 36 of them are in 0402 R/C pads. No via sits in a pad narrower than the via, and none sits in a U1 signal pad.
- **Board thickness:** the stackup sums to 1.606 mm, so the aspect ratio is 8.0:1 for 0.2 mm holes and 5.3:1 for 0.3 mm holes.

---

## Blockers

None. Every via meets JLC's manufacturing limits. The board would be built as drawn.

## Major

### M1. 87 vias, and every via the router places by default, are in JLC's surcharge class (0.2 mm hole, under 0.45 mm diameter). DRC cannot see it.

- **What:** 87 vias are 0.40/0.20 (table above). They include both VSYS vias (120.15, 97.99) and (119.33, 102.12), the QSPI fan-out at U4/U6, and 21 GND vias in 0402 pads (for example C36 at 137.09, 96.48 and C10/C12 at 134.90/135.87, 98.72).
- **The cause:**
  - The `Default` net class in `pico-stretch2.kicad_pro` is `via_diameter 0.4, via_drill 0.2`. pcbnew reports the current via as `0.4 0.2`.
  - The `Diff` class leaves its via unset (`-1e-06`), so USB vias inherit 0.4/0.2.
  - With "use net class sizes", the router places 0.4/0.2 every time. The predefined 0.45/0.2 and 0.63/0.3 entries in `via_dimensions` are only used when someone picks them by hand.
- **Evidence (JLC capabilities page, "Min. Via hole size/diameter"):**
  - Note ③ says: "0.1mm or 0.15mm hole size with any size via diameter, and 0.2mm or 0.25mm hole size with via diameter less than 0.45mm, will cost more. Please select corresponding via size option when placing order."
  - JLC's extra-charge article says: "if the option of via is selected correctly, the cost will be added when quoting" and "If it is not selected according to the Gerber file, the cost will be charged as a supplement when reviewing."
  - The 139 vias at 0.45/0.20 sit exactly at the free threshold. The 0.63/0.30 vias are free.
- **Why DRC passes it:**
  - The rules are `min_via_diameter 0.4`, `min_through_hole_diameter 0.2` and `min_via_annular_width 0.1`.
  - There is no custom via rule in `pico-stretch2.kicad_dru`, which holds only the courtyard pairs.
  - So DRC accepts 0.4/0.2, and `drc.md` (8 accepted warnings) gives no hint of the price class.
- **Consequence:**
  - Every order either pays the small-via option at quote time, or gets held at engineering review for a supplement.
  - Every via added later (for example by the pending rework) lands in the same class.
  - It is not a functional defect. The amount is not on the page and I could not verify it (see below).
  - A secondary reason, not verified: JLC's note ① prefers the diameter 0.15 mm larger than the hole. With ±0.075 mm hole position tolerance and an unknown drill oversize, 0.45 mm keeps 0.025 mm more ring than 0.40 mm.
- **Fix (verified on a copy):** resize all 87 vias to 0.45/0.20.
  - `chk_045` result: DRC 0 errors, 0 unconnected, parity 0. The same 8 warnings remain (7 `lib_footprint_mismatch`, 1 `silk_over_copper`), so nothing new.
  - It is clean because `min_hole_clearance 0.25` already holds every other-net copper 0.25 mm from each hole. A 0.45 pad then still keeps 0.125 mm of copper clearance, above the 0.1 net-class clearance.
  - In-pad fit after resizing:
    - The worst 0402 case is C13.1: its 0.03 mm margin becomes 0.005 mm inside the pad.
    - C9.1 overhangs already (m2) and goes from 0.07 to 0.095 mm. Recentre it as part of m2.
  - Also make new vias right by default:
    - set `Default` via to 0.45/0.2;
    - set `min_via_diameter` to 0.45. Every via drill here is 0.2 or 0.3, and the 0.3 vias are 0.63, so a global 0.45 minimum is safe. A hole-size-conditioned custom rule also works, but check the via property names in the KiCad 10 rule editor first.
  - Cost: one scripted edit plus a refill. Nothing moves.

## Minor

### m1. The U1 EP vias (0.63/0.30) are outside JLC's literal size range for "Epoxy Filled & Capped"

- **What:** the 9 GND vias in U1 pad 81 (141.17–143.46, 101.22–103.25) are the vias that the accepted via-in-pad decision most depends on. They sit under a 100 % paste window (accepted m7).
- **Evidence (JLC's own pages disagree):**
  - The capabilities page, Epoxy Filled & Capped, item ③: "Compatible with via diameters from 0.15 to 0.55 mm."
  - In the same page's own wording, "via diameter" means the copper pad: "Min. Via hole size/diameter 0.15/0.25mm", and "Via diameter should be 0.1mm … larger than Via hole size". Read that way, 0.63 is out of range.
  - The POFV page gives "Via hole size: 0.2 to 0.5 mm" instead, and the 0.30 hole is inside that.
- **Consequence:** if JLC's CAM leaves these 9 out of the fill, they get nine open 0.3 mm barrels under a full-coverage EP paste print. Solder wicks to the back, the EP joint voids, and the fine-pitch QFN tilts. That is a yield risk on the one part that matters most. I could not confirm which reading JLC applies.
- **Fix:**
  - Change the footprint's EP vias to 0.55/0.30. The ring becomes 0.125 mm, still above the 0.05/0.075 via minimum, and this fits every reading.
  - The thermal barrel is unchanged, because the drill and plating are the same: about 35 K/W per via to In1, 3.9 K/W for nine, 0.5 K at 0.12 W.
  - Or write "fill all vias including 0.63 mm" in the order remark and get JLC to confirm.
  - Cost: a footprint edit and re-export, or one line in the order.

### m2. Tented vias abut pad mask openings with less than JLC's 0.09 mm, and one via overhangs its pad

Mask is 1:1 (`pad_to_mask_clearance 0`). JLC (Soldermask Expansion): "Keep at least 0.09 mm clearance between soldermask openings and neighboring traces." Measured from via copper to the pad edge:

| Via (net, size) | Pad | Gap |
|---|---|---|
| (147.755, 100.007) GPIO28 0.45 | U1.36, at the toe of a 0.4 mm-pitch QFN pad | **0.030** |
| (147.870, 101.603) 1V1 0.45 | C2.1 (0402) | **0.028** |
| (134.493, 100.178) 1V1 0.45 | L1.2 | 0.038 |
| (146.528, 100.402) RUN 0.45 | U1.35, heel side under the body | 0.082 |
| (135.310, 101.740) GND 0.40, in the pad | C9.1 | via overhangs the pad edge by **0.070** (12 % of its copper outside the pad) |

- **Consequence:**
  - Mask registration of a few hundredths of a mm exposes a crescent of the (capped) via next to the opening, and solder flows onto it.
  - On U1.36, the 0.45 mm via is wider than the 0.2 mm pad. It steals solder from the toe fillet of a pad that is already short (accepted m7), and it exposes copper 0.17 mm from the toes of pins 35/37.
  - On C2 (0402), wetting becomes one-sided, which raises tombstoning risk.
  - These are all same-net, so there is no short.
  - DRC cannot see this: `solder_mask_to_copper_clearance 0.005` only covers other-net copper, and `board_lint` flags only via centres inside pads.
- **Fix:** move each via 0.07–0.1 mm away from its pad and shorten the stub. Recentre C9's via in its pad, about 0.07 mm toward the pad centre (-y, from y 101.74 to about 101.67). The resulting DRC must be checked. Cost: 5 via nudges.

### m3. The DRC rules do not enforce JLC's via-to-plated-hole spacing; hole_to_hole is only a warning

- **What:** `min_hole_to_hole 0.25`, and the project sets `hole_to_hole` severity to **warning**.
- **JLC's limits:**
  - capabilities page: "Pad Hole-to-Hole Spacing 0.45mm";
  - POFV page: filled vias "Should be placed more than 0.45 mm from regular PTHs or NPTHs".
- **Today:** the closest via to a plated hole is 0.600 mm edge to edge (GND via 162.80, 92.60 to the J4.44 castellated hole). Via-to-via is at least 0.375 mm (GPIO21/22 at 150.21, 105.99 / 150.11, 105.42), above JLC's 0.2. So the board is fine now.
- **Risk:** a new GND stitching via next to a castellated hole could be placed at 0.25 mm and pass DRC as a warning.
- **Fix:** add `(rule "via to PTH" (condition "A.Type == 'Via' && B.Type == 'Pad' && B.Pad_Type == 'Through-hole'") (constraint hole_to_hole (min 0.45mm)))` and set `hole_to_hole` to error. Cost: 2 lines.

---

## Problems with the analysis pack

1. **The U1 regulator hot loops are the wrong capacitors.**
   - emc.md's "RP2350 VREG_VIN input (CIN)" loop uses C36, the 100 nF on IOVDD pin 60. Its "VREG output (COUT)" loop uses C13, the 100 nF on DVDD pin 51.
   - The regulator's real CIN is C12 (VREG_VIN pin 64 to VREG_PGND pin 62), and its COUT is C10.
   - Both close on F.Cu through the GND_VREG island (PGND pin 62, C12.2 and C10.2). That island joins the plane through the two 0.4/0.2 vias at (134.90, 98.72) and (135.87, 98.71).
   - The warning "U1 switches /VREG_LX but no power pin of it has a capacitor to ground" is also false: pin 64 has C12.
   - The pack's loops come from `review_config.json` keying only on `in_net`.
   - The two ME6217 "hot loops" (C37, C38) are LDO decoupling, not switching loops.
2. **The "100 % through one via" flags (C36, C13, C37, C38) are not quantified, and with numbers they are not actionable.**
   - The depth from F.Cu to In1 is z = 0.245 mm (0.2104 prepreg).
   - The partial self-inductance of that barrel (r ≈ 0.109 mm) is **0.044 nH**. It is the same for a 0.40 or a 0.45 pad, because the drill sets it.
   - For comparison, a microstrip over In1 (Hammerstad, εr 4.4) is 0.53 / 0.43 / 0.39 nH/mm at 0.12 / 0.2 / 0.254 mm width, and an 0402 body ESL is a few tenths of a nH.
   - A second via would save about 0.02 nH, a few percent of the loop.
   - The "path 1.6 mOhm" DC figure says nothing about high-frequency decoupling.
3. **Plating assumption:** `fem.py` uses `T_PLATE = 20e-6`, but JLC's page says "Average Hole Plating Thickness 18μm". The barrel is modelled as π·d·t, not π·(d+t)·t. The two errors nearly cancel (0.0126 vs 0.0123 mm², 2 %), but the stated source is wrong. thermal.md also states 20 µm.
4. **No fabrication-class check on vias.**
   - `board_overview.md` lists the classes but not the JLC price class (M1), the via-in-pad count (78), or vias abutting mask openings (m2).
   - `drc.md` passing gives false comfort, because the project rules are looser than JLC's free tier.
5. **The VBUS run.**
   - Its title says "to D1 anode and castellated VBUS pad", but the only sink is `D1:2`, so pass-through to J4:64 is not solved.
   - Its "Busiest via 0.00 @ 110.8,92.6" is a J4 castellated hole: VBUS has zero vias.
   - The VSYS run's 0.9 A exceeds what the LDO can draw, which is fine as a pessimistic case.
6. **The thermal "one via only" findings are not actionable as written.**
   - They flag the VSYS pour under U3 (via 119.33, 102.12) and the 3V3 pour under U5 (via 176.25, 103.96).
   - The suggested remedy is "stitching vias to a plane of the same net", but there is no VSYS or 3V3 plane. Those vias land on B.Cu tracks.
   - U3's real via path to the planes is its single GND via in pin 2 (120.532, 103.558). From the barrel alone that is about 51 K/W to In1. It only matters in the continuous-Tx corner, which is excluded by the accepted bursty-Tx decision.
7. **Edge stitching wording and threshold.**
   - power.md says "93 ground vias within 3 mm of the edge". It is 71 vias plus 22 plated GND holes (J4 has two plated holes per GND position, plus the USB1 shell).
   - The 10 mm gap threshold is not tied to frequency. At the RM2 end (x ≈ 190) there is an **8.45 mm** gap (y 96.16–104.61), against λ/10 ≈ 5.8 mm in FR4 at 2.4 GHz.
   - I did not judge this to be a board problem (see "could not verify").
8. Smaller items:
   - The emc layer-change list puts GPIO47's In1↔B.Cu via (127.8, 97.45) first, but both of that via's references are GND (In2), so it is not a reference switch.
   - The list does not say which signal vias pass through the In1/In2 cavity without a GND via within about 1 mm.

## Checked and found fine

- **JLC limits:**
  - min via 0.15/0.25: all vias are 0.2/0.4 or larger.
  - via ring "0.1mm (0.15mm preferred) larger" than the hole: rings are 0.10 / 0.125 / 0.165 mm.
  - aspect ratio 8:1 against JLC's "Do not exceed 10:1".
  - via hole-to-hole 0.2: minimum 0.375.
  - "Via hole to Track 0.2mm" and "Inner layer via hole to copper clearance 0.2mm": every via's hole-to-other-net copper is at least **0.250 mm** on all four layers (`min_hole_clearance 0.25`).
  - copper to routed edge ≥ 0.2: the closest via copper is 0.855 mm from the edge (project rule: 0.5).
- **Inner antipads:** non-GND vias clear the In1/In2 GND fill by exactly 0.25 mm from the hole (0.7 mm antipad). Inner non-functional pads are 0.4–0.45 mm with 0.125–0.15 mm copper gap.
  - Merged antipads form the small slots the pack reports at the GPIO16–22 fan-out (150–153, 105–108). Only each net's own B.Cu track crosses its own antipad.
- **Plane connection:** all 176 GND vias are fully covered by both the In1 and In2 GND fills (solid connection, coverage 1.00). No GND via sits in the VREG_LX cut-out.
- **Via-in-pad geometry:** no via is in a pad narrower than itself, none overlaps an other-net pad, and none is in a U1 signal pad. Except C9.1 (m2), every in-pad via is fully inside its pad. The tightest are R16.1 at 0.005 mm and R10.1 at 0.015 mm. Paste over capped vias is the accepted decision.
- **Power-net vias** (JLC 18 µm plating, 1.6 mm barrel, own model; `power.py` ad hoc VSYS run on a copy):
  - **Resistance:** 2.23 mΩ for a 0.2 mm drill, 1.53 mΩ for 0.3 mm. A run that loaded both U3 and J4:63 (0.5 A each) found no VSYS via above 0.50 A; the J4:63 current reaches the pad through the castellated barrels. I did not re-solve VSYS at 0.9 A.

    | Via | Current | Drop | Barrel dT |
    |---|---|---|---|
    | VSYS, two in series (pack run) | 0.9 A | 2.0 mV | 0.075 K |
    | 3V3 RM2 feed (146.98, 106.69) and (176.25, 103.96) | 0.35 A each | 0.8 mV | – |
    | 1V1 (140.06, 100.19) and (134.49, 100.18) | 0.2 A | 0.45 mV | – |
    | GND USB1.1 / USB1.12 | 0.44 A | 1 mV | – |

  - **Barrel heating:** for a barrel with both ends held at board temperature, dT = I²ρL²/(8kA²). That gives under 0.1 K at 0.9 A, and 0.84 K at a hypothetical 3 A.
  - **Fusing:** the Onderdonk adiabatic limit for a 0.2 mm barrel is 3.5 A for 1 s. The barrel ends are heat-sunk, so the 0.25 mm tracks limit current long before the vias do.
  - **Verdict:** nothing here makes accepted m5 worse.
- **U1 EP thermal vias:** about 3.9 K/W for nine to In1 (pack: 3.6 K/W at 20 µm), 0.5 K at 0.12 W.
- **Return vias at layer changes:**
  - Worst QSPI/SPI F↔B transitions have the nearest GND via 2.2–3.6 mm away.
  - The two-via loop across the 1.08 mm In1–In2 core is L = (μ0·h/π)·ln(s/r) ≈ 1.5 nH at 3.3 mm, against 0.9 nH at 0.8 mm.
  - QSPI rise times are about 1 ns, so this is acceptable and was accepted in earlier reviews. A GND via beside U4/U6's via-in-pad rows would be a cheap improvement, not a defect.
- **Vias under bodies:** the non-GND vias under U1, U4, U6 and U5 are tented and will be capped. None sits under a metal-bottomed part.
- **Production Gerbers:** the drill file has 226 vias at 0.20 mm plus 9 at 0.30, and copper has 0.40/0.45/0.63 apertures. This matches the board.
- **Edge stitching:** apart from the RM2 end, the largest gap along the long edges is 4.95 mm, at x 157.85 top and 157.79 bottom.

## Could not verify

- **The size of JLC's small-via charge** for 0.2/0.4 on a 4-layer board with "Epoxy Filled & Capped" selected. The cost table is an image, and the quote form is JavaScript. I also could not verify whether that option changes which via option the order needs. Confirm on the live quote with both options.
- **Which reading JLC's CAM applies** to "via diameters from 0.15 to 0.55 mm" (m1).
- **JLC's drill oversize for a 0.20 mm finished via**, and so the real ring after the ±0.075 mm position tolerance.
- **Whether the RM2 datasheet asks for host-board GND stitching under the module.** The 8.45 mm gap at x ≈ 190 was measured but not judged.
- **Inner copper thickness:** the file says 15.2 µm, and JLC's page says "Finished copper weight of inner layer is 0.5oz by default". This does not affect the via results.
