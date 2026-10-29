# Pico Stretch 2: design review 2 (re-review after the review-1 fixes)

Board: `/Users/joshv/git/pico-stretch2`, working tree on top of commit 54e971f. The fixes from `scripts/review_fixes.py` are uncommitted; board and schematic were saved 2026-10-29 17:20. RP2350B dev board, 82.4 × 21.3 mm, 4 layers (JLC04161H-7628), KiCad 10.0.1, JLCPCB economic PCBA.

Scope: review only; no project file was changed. This report and `review2/` are the only new files. `production/` (11:46) is older than the board and was not used.

## Method

- **Analysis pack:** `review2/pack/`, built by kicad-board-review's `make_pack.sh` on a copy of the project, with zones refilled and DRC + schematic parity run. Inner copper is the stackup's 15.2 µm, as in review 1.
  - The pack config (`review2/pack/review_config.json`) is review 1's, plus: the USB pairs with a 90 Ω target, a 5 mm decoupling limit, and a thermal section (two corners, a loss for every candidate heat source).
  - `boarddump.py` now writes canonical layer names itself, so review 1's patched copy was not needed.
- **Like-for-like baseline:** a second pack of commit 54e971f (`git archive HEAD`), built with the same tools and config (`/tmp/psr2/headpack`, not kept in the repo). The before/after numbers come from it, cross-checked against `review/pack/`. Where `review/pack/` differs from the HEAD rebuild, the difference comes from the tool version and is noted.
- **Datasheets read** (local copies in `/tmp/psr2/ds`, not in the repo):
  - ESD5Z2.5T1G series (onsemi, Rev. 13), pp.1–3
  - ME6217 (Microne V02), pp.2, 4, 5
  - DFLS130L, p.2
  - RP2350 datasheet, errata D.2.3
  - RM2 datasheet §1.2
  - Samsung MLCC catalogue: it has no DC-bias curve for CL10A106KP8NNNC
  - JLCPCB rigid-PCB capabilities page (fetched 2026-10-29)
- **Board checks:**
  - `board_diff` from HEAD to now, and `partfields` (schematic vs board fields)
  - ERC item-by-item against HEAD
  - `board_lint` diff against HEAD
  - DRC on a copy without `pico-stretch2.kicad_dru`, to list every real courtyard overlap
  - `pour_check` on the USB and VREG windows
  - Pad-to-pad gap scans (`review2/scripts/padgaps.py`, `gaps.py`, `j4u5.py`)
  - Measurements of the In1 cut-out against the USB pair and the Fig. 27 items (`review2/scripts/usbref.py`, `cutdist.py`, `cutcover.py`)
  - Renders (`review2/renders/`), all looked at
- **Hot-plug transient:** a small ODE model (`review2/scripts/hotplug.py`) of cable L/R → VBUS → D1 → C37, with and without D4. The TVS is modelled piecewise-linear from its datasheet points.
- **Independent adversarial review:** `review2/pack/adversarial_review.md`. Each of its findings was re-checked against the files before being kept (see "Adversarial pass").

### Status (2026-10-29, `scripts/review_fixes.py`, rebuilt from 54e971f)

- **M1, fixed.**
  - C39 stays at (117.85, 103.08) but is rotated 90°. Its GND pad now faces D3's GND pad, and a 0.2 mm track joins it to D3's GND via.
    - Moving C39 down 0.1 mm was tried first. It closed the VSYS pour's neck to R11.1, and DRC then reported R11's VSYS piece unconnected.
  - C13 moved 0.05 mm up, to (142.325, 96.025), with its 1V1 track re-ended on the moved pad.
  - The board's closest different-net SMD pads are now U1.50–C13.2 at 0.177 mm and D3.2–C39.2 at 0.19 mm.
- **m1, m3 and m4: resolved by removing D4, by decision.** That means the schematic symbol and its power flags, the footprint and its GND track, the D4/USB1 courtyard pair, and the ESD5Z5_0T1G symbol from `EasyEDA.kicad_sym` (now back to HEAD). VBUS is back to review 1's state (review-1 m4 not done).
- **m2, fixed:** the Status text in `DESIGN_REVIEW.md` is corrected.
- **Verified on the rebuilt project:**
  - DRC: 8 items, all in the accepted baseline, 0 new; 0 unconnected; parity 0.
  - ERC: 162 items, 0 new.
  - `board_lint`: only the D4 silk item is gone.
  - `pour_check` on the USB and VREG windows: the same as before.
  - The 22 named courtyard pairs all match real overlaps.

---

## Blockers

None found. The board as drawn should power up, enumerate on USB, boot from flash and debug over SWD. DRC: 0 errors, 0 unconnected, parity 0.

## Major

### M1. Two different-net SMD pad pairs are closer than JLC's 0.15 mm pad-to-pad limit; one of them is new

| Pair | Nets | Gap | Status |
|---|---|---|---|
| D3.1 (117.25–117.85, 101.62–102.22) – C39.1 (117.54–118.16, 102.32–102.88) | GND – VSYS | **0.100 mm** | **new** (D3 and C39 placement in m2) |
| U1.50 (142.36–142.56, 96.96–97.63) – C13.2 (142.01–142.63, 96.28–96.83) | 3V3 – 1V1 | 0.127 mm | pre-existing (same at HEAD); not in review 1 |

- **Evidence:**
  - Measured on the filled board copy (`review2/scripts/padgaps.py`). These are the only two pairs on the board under 0.15 mm. The next closest is D3.2–C39.1 (D+ to VSYS) at 0.19 mm, and before this change the board's tightest pair was U1.50–C13.2.
  - JLCPCB capabilities, Traces: "SMD pad to pad clearance (different nets): 0.15 mm". Soldermask: "Soldermask bridge 0.10 mm", "Min. pad spacing 0.10 mm" (green, 1 oz).
  - `pad_to_mask_clearance` is 0, so the D3/C39 mask dam is exactly at JLC's minimum.
  - DRC passes because the board's `min_clearance` is 0.09 mm.
- **Consequence:**
  - Expect JLC's DFM check to flag both pairs. If the 0.10 mm dam is not held, the two openings merge.
  - A solder bridge at D3/C39 shorts VSYS to GND: the board is dead on first plug-in, and the USB port current-limits.
  - A bridge at U1.50/C13.2 puts 3.3 V on DVDD (1.1 V), which very likely destroys the RP2350.
  - Both pairs are 0402-class pads, so the bridge probability is low. The cost of a bridge is high, and both are cheap to fix.
- **Fix:**
  - **C39:** move it 0.10 mm down, to (117.85, 103.18). Measured after the move: D3.1–C39.1 0.20 mm, D3.2–C39.1 0.27 mm, C39.1–R4.2 0.22 mm, C39.2–C37.1 0.247 mm. Nothing else comes within 0.3 mm. Its 0.2 mm GND track to the via at (117.0, 103.9) follows.
  - **C13:** move it 0.05 mm up. Measured: U1.50–C13.2 0.177 mm; the nearest other copper is the GPIO40 track at 0.165 mm and the GPIO41 track at 0.176 mm. Re-attach its track ends.
  - Two footprint nudges and a DRC run. The courtyard exemptions stay valid.

---

## Minor

### m1. D4 hardly changes the hot-plug peak, which is what review-1 m4 was about

- **What:** D4 (ESD5Z5.0T1G, at 112.4, 95.0) has its cathode on VBUS (pad 1 = cathode, datasheet p.1) and its anode on the USB1 shell pad 13. That is correct.
  - Its clamp starts too high to limit cable ringing. The datasheet gives VBR ≥ 6.2 V at 1 mA, and VC 11.6 V typical at 5 A (8/20 µs), so it behaves like a ~6.6 V knee with about 1 Ω slope (ESD5Z table, p.3).
  - The ME6217 absolute maximum is VIN 7.0 V (p.2); operating max is 6.5 V (p.4).
- **Evidence:** ODE model (`review2/scripts/hotplug.py`): a 5 V step through cable R + L into VBUS, then D1 (DFLS130L, 0.21 V at 0.1 A, 0.31 V at 1 A, p.2) into the VSYS capacitance. C37 is a 10 µF 0603 at about 5 V bias, taken as 5 µF effective.

  | Cable (L, R) | VSYS peak, no D4 | VSYS peak, with D4 |
  |---|---|---|
  | 1.0 µH, 0.1 Ω | 7.26 V | 7.05 V |
  | 1.5 µH, 0.1 Ω | 7.58 V | 7.26 V |
  | 1.0 µH, 0.2 Ω | 6.42 V | 6.41 V |
  | 1.5 µH, 0.4 Ω | 5.74 V | 5.74 V |

  The ring is set by the cable inductance against C37. D4 only trims the worst cases, by 0.2–0.3 V. Higher cable resistance damps the ring far more than D4 does.
- **Consequence:**
  - With a short, low-resistance cable (or a hot-plugged bench supply with long leads), VSYS can still briefly exceed the ME6217's 7.0 V absolute maximum.
  - D4 still does its other job: ESD on VBUS. Its standoff is also fine against USB-C VBUS: 5.5 V max is below VBR min 6.2 V.
  - Adding the LDO's start-up current (0.35–0.6 A) to the model (adversarial pass) still leaves about 7.0–7.1 V with D4.
  - The exposure is narrower than review-1 m4 implied. A USB-C source on a C-to-C cable does not turn VBUS on until it has detected the attach on CC, so there is no hot-plug ring. The case is a legacy A-to-C cable or an always-live 5 V supply.
  - D4 sits about 9.8 mm of 0.25 mm track (about 3 nH) from USB1's VBUS pin, on the branch to castellated pad 64. That is fine for this ring (MHz) and for ESD (D1 and C37 absorb the charge).
  - This is a model with assumed cable values, not a measurement, and the same topology works on many hobby boards. That is why it is minor.
- **Fix, if wanted (model results at 1.5 µH, 0.1 Ω):**
  - **(a) Damping on VBUS:** 4.7 µF in series with 1 Ω (a 0402 1 Ω, C25086, is already on the BOM) gives **6.54 V**. This adds two parts beside D4.
    - 10 µF + 1 Ω would give 6.08 V, but it breaks the USB 2.0 limit of 10 µF at attach, because C37 (10 µF) already uses that budget.
    - Even 4.7 µF takes the board's nominal attach capacitance to about 15 µF. To stay strictly compliant, swap C37 for a 4.7 µF part (it still meets the ME6217's CIN ≥ 4.7 µF, p.5) and add the 4.7 µF + 1 Ω damper.
  - **(b) A stiffer TVS:** an SMF5.0A-class part (VC ≈ 9.2 V at 43 A, so ~0.06 Ω slope) gives 6.61 V, but needs a SOD-123FL land.
  - **(c) Document it:** "hot-plug from a short cable only to a powered-down board" is not practical. Prefer (a).

### m2. The In1 cut-out stops 0.335 mm from USB_D−, not 0.63 mm, and covers the 1V1 side only partly (correction to the review-1 Status text)

- **What:** the rule area is 132.5–137.3 × 97.45–100.15, with a step at x 134.75 from y 100.15 up to 99.85.
  - USB_D− runs at y 100.56 (0.15 mm wide) and turns down at (134.71, 100.56). The step corner (134.75, 100.15) is therefore **0.335 mm** from D− copper (`review2/scripts/cutdist.py`).
  - The 0.635 mm the Status quotes holds only for x 134.75–136.25. At HEAD the cut-out was 0.936 mm from D−.
  - Fig. 27 coverage, measured as the share of each F.Cu item still over In1 GND (HEAD → now):

    | Item | HEAD | Now |
    |---|---|---|
    | L1.1 (LX) | 0 % | 0 % |
    | L1.2 (1V1) | 98 % | **53 %** |
    | C10.1 (COUT) | 97 % | 14 % |
    | C12.1 (CIN) | 100 % | 20 % |
    | 1V1 pour | 88 % | 40 % |

  - The Status line "covers L1, … the 1V1 pad" overstates it: half of L1's 1V1 pad is still over the plane.
- **Does the USB pair keep a solid reference? Yes.**
  - Both lines run 0 mm over void, before and after.
  - The nearest void edge to D− is unchanged at 0.014 mm. That is the antipad of the 1V1 via at (134.49, 100.18), which has been there since before the extension.
  - The pack's reference table is identical to HEAD: USB_D− has 0.5 mm over a ground edge at (134.71–134.81, 100.56), the same as `review/pack/emc.md`.
  - At 12 Mb/s this has no measurable effect.
- **Consequence:** documentation accuracy only. The cut-out remains a deliberate partial Fig. 27 (accepted limit).
  - The 1V1 via's centre (134.49, 100.18) lies 0.03 mm outside the rule area. Only its antipad merges with the cut-out.
  - Full coverage is not possible without moving the USB pair.
  - One more error in the same Status section (found in the adversarial pass): it says the front "40A0" uses a 0.7 × 0.6 font. The board has 0.8 × 0.55 (F.SilkS); the back label is 0.8 × 0.8. The 0.8 × 0.55 font itself is accepted.
- **Fix:** correct the Status text in `DESIGN_REVIEW.md`: 0.335 mm at the step corner; L1.2 about half covered and the 1V1 via not covered; the "40A0" font is 0.8 × 0.55. No layout change is needed.

### m3. Silkscreen: the front "VSYS" pad label sits on D4's pad edge

- **What:** the "VSYS" label bounding box (pcbnew) spans x 112.75–114.04. D4's pads end at x 112.75, and its body (1.2 × 0.8 mm, datasheet p.1) at about 112.8. `board_lint` reports it as a new SILK ON PART on D4.
- **Consequence:** cosmetic. JLC clips silk at the mask opening. Ink under the body edge of a 0.7 mm-high SOD-523 is a small tilt risk at most.
- **Fix:** move the "VSYS" text about 0.15 mm in +x, so it starts at about 112.9.

### m4. D4 is the one new polarised part that no placement preview has covered, and it has no polarity mark; reversed, it shorts VBUS

- **What:** D4 uses KiCad's `Diode_SMD:D_SOD-523` at −90°.
  - The rotation sign-off in JLC's preview predates D4.
  - The Fabrication Toolkit's `transformations.csv` (KiCad 10 plugin copy) has no `D_SOD-523` rule, so D4 goes out with no correction.
  - Its silkscreen was removed (accepted), so neither the bare board nor the assembled board shows its cathode.
- **Consequence:** a TVS placed backwards is a forward diode from VBUS to GND (VF 1.1 V max at 10 mA, p.3). On first plug-in, the host port current-limits, or D4 overheats (500 mW rating, p.2). The board is dead until D4 is reworked.
- **Fix:**
  - After regenerating `production/`, confirm in JLC's placement preview that D4's cathode band is on the pad toward the VBUS track (pad 1, at 112.4, 94.3). The README already says to "Check pin 1 of … the diodes"; D4 is the one that has not been checked.
  - Optionally add a `Rotation Offset` field or a transformations rule once the right value is known, and a small fab-layer or silk cathode dot where it fits.

---

## Before ordering (not findings)

- **Regenerate `production/`.** It dates from 11:46, before every fix.
  - With `EXCLUDE DNP: true` in `fabrication-toolkit-options.json`, U5 now drops out of the BOM and CPL.
  - The BOM should then show C9/C15 under C1525, R14 under C11702, C40 under C19702 (0603), and a new D4 line (C82044).
- **Re-check the placement preview** for the parts whose footprint or rotation changed since the previous preview:
  - **D4** (new, polarised; see m4): its cathode bar must sit at the pad on the VBUS track, at y 94.3.
  - **D3** (rotation 180 → 0). Its MSKSEMI RCLAMP0521P-MS part (C3029033) is listed as bidirectional, so its orientation does not matter electrically.
  - **C39** (−90) and **C40** (0402 → 0603, 180).
  - D3, D4 and C40 have no silk outline any more (accepted), so the preview is the only polarity check for D4.
- **Extended parts:** there are now 10 (D4, C82044, is new). Each one adds JLC's extended-part fee.

---

## Fix-target before/after (review-1 fixes)

Before = commit 54e971f rebuilt with today's tools (`/tmp/psr2/headpack`), cross-checked against `review/pack/` (8e0d15f). After = `review2/pack/`.

| Review-1 item | Target measured | review/pack | HEAD rebuild | Now | Verdict |
|---|---|---|---|---|---|
| M1 | C9, C15 LCSC (schematic + board) | C14663 (0603 part) | C14663 | **C1525** CL05B104KO5NNNC 0402, Basic, 2.03 M stock; schematic = board (`partfields`: 0 mismatches) | fixed |
| m1 | In1 slot around the VREG | 5.5 × 1.9 mm | 5.5 × 1.9 mm | 5.5 × 3.1 mm (2 vias inside: 3V3, 1V1) | extended |
| m1 | L1.2 / C10.1 / C12.1 / 1V1 pour over In1 GND | – | 98 / 97 / 100 / 88 % | 53 / 14 / 20 / 40 % | partly (m2) |
| m1 | PGND vias (134.90, 98.72), (135.87, 98.71) on plane | yes | yes | yes | kept |
| m1 | USB_D± over void / nearest void edge | 0 / – | 0 mm / 0.014 mm | 0 mm / 0.014 mm | unchanged |
| m1 | Cut-out to USB_D− copper | – | 0.936 mm | 0.335 mm | see m2 |
| m2 | D3 connection to D+ | 2.0 mm B.Cu stub + 2 vias | same | 0.49 mm F.Cu stub, 0 vias | fixed |
| m2 | USB2_D+ vias / B.Cu length | 2 / 2.9 mm | 2 / 2.9 mm | 1 / 1.3 mm (TP4 spur only) | fixed |
| m2 | Clamp-path inductance (estimate) | ~1.5–2.5 nH | – | ~0.3–0.4 nH (0.49 mm at ~0.5 nH/mm, plus the via-in-pad to In1) | fixed |
| m3 | R14 value / LCSC | 10 kΩ C25744 | same | **1 kΩ C11702** (schematic = board) | fixed |
| m3 | CE# worst case (RPD 36 kΩ) | 2.58 V | 2.58 V | 3.21 V (≥ VIH 2.9 V) | fixed |
| m4 | VBUS protection | none | none | D4 ESD5Z5.0T1G, C82044 (Extended, 310 k stock) | added |
| m4 | VSYS hot-plug peak (model, 1.5 µH, 0.1 Ω) | – | 7.58 V | 7.26 V | weak (m1) |
| m8 | C40 part | 10 µF 0402 6.3 V (C15525) | same | 10 µF 0603 10 V (C19702, Basic, 3.04 M) | fixed |
| m8 | C40 pin-cap / ground-path / loop area | 1.30 mm / 2.80 mm / 2.2 mm² | same | 1.52 mm / 3.33 mm / 0.7 mm² | ≈ same; loop smaller |
| m9 | J4 33–36 ↔ U5 pad gap | 0.24 mm | 0.24 mm | **0.39 mm** | fixed |
| m9 | J4 29–32 ↔ U5 pad gap | 0.34 mm | 0.34 mm | 0.49 mm | fixed |
| m9 | J4 29–36 ring at the clipped tip | 0.35 mm | 0.35 mm | 0.20 mm (1.0 mm drill, 1.7 × 3.15 oval, offset −0.875) | OK, see below |
| m11 | U5 DNP / F.Paste on its pads | no / 21 pads | same | **DNP / none** (board and `Custom.pretty`) | fixed |
| m13 | Silk collisions JP2/"25", JP3/"23", "0"/JP1, pad 37 text | present | present | gone; "40A0" both sides (renders) | fixed (m3 is new) |

**Nothing else got worse.**

| Measure | HEAD | Now |
|---|---|---|
| Power-run drops: vbus | 3.2 mV | 3.2 mV |
| Power-run drops: vsys | 19.9 mV | 19.9 mV |
| Power-run drops: 3V3 | 28.4 mV | 28.4 mV |
| Power-run drops: 1V1 | 5.0 mV | 5.0 mV |
| Ground return | −0.6 mV | −0.6 mV |
| Planes: In1 | 80.6 %, 1 piece | 80.6 %, 1 piece |
| Planes: In2 | 81.2 %, 1 piece | 81.3 %, 1 piece |
| Edge stitching | 93 vias, no gap > 10 mm | 93 vias, no gap > 10 mm |
| Weak ground pieces | 0 | 0 |
| Inner-layer tracks | GPIO47 link only | GPIO47 link only |
| EMC reference spans (high / medium / low) | 4 / 0 / 11 | 4 / 0 / 11, same rows |
| Crosstalk table | – | identical |
| `pour_check`, USB and VREG windows | – | identical |
| ERC | 162 items | 162 items, identical item set |

- `review/pack` showed 19.6 mV on vsys; the HEAD rebuild with today's scripts gives 19.9 mV, so that difference comes from the tool version, not the board.
- VBUS current-density hotspot: 4.3 A/mm in `review/pack`, 3.7 A/mm in the HEAD rebuild and now. Again a tool-version difference.

## Checked and found fine

- **DRC (copy, refilled):** 0 errors, 0 unconnected, parity 0. The 9 warnings are all accepted items: 8 `lib_footprint_mismatch` (J2, C40, C37, R3, D4, D3, USB1, C39) and U3's silk clipped by C40's 3V3 pad.
- **ERC:** 162 items, the same set as HEAD item for item. D4 added nothing.
- **Change scope (`board_diff` HEAD → now):** only the intended changes:
  - fields on C9, C15, C40 and R14
  - D3, C39 and C40 moved; D4 added
  - J4 pads; U5 DNP
  - the copper listed under m2/m8 and D4
  - the cut-out polygon and three silk texts

  The C9/C15 Description field was copied from C1 with blank values ("Capacitance: Tolerance:…"), as C1 already has. Cosmetic.
- **BOM fields for C9, C15, R14, C40 and D4:** schematic and board are identical (`partfields`: 0 mismatches).
  - C9/C15 = C1525 CL05B104KO5NNNC 0402.
  - R14 = C11702 1 kΩ 0402.
  - C40 = C19702 CL10A106KP8NNNC 10 µF 10 V X5R 0603 (Basic, 3.04 M).
  - D4 = C82044 ESD5Z5.0T1G SOD-523 (Extended, 310,048).
  - The 28 `partfields` "problems" are blank Datasheet/LCSC on J2, J4, TP1–4 and U5, the same at HEAD (hand-fitted or not placed).
- **Courtyard exemptions:** with the rule file removed, DRC lists exactly 23 overlapping pairs, and they are exactly the 23 pairs the rule names. No named pair is stale, and no overlap is unnamed. The rule is pair-by-pair, not a blanket.
- **J4 clip vs JLC:** JLCPCB capabilities, PTH annular ring, multilayer 1 oz: "Recommended 0.20 mm or above; absolute minimum 0.15 mm". The clipped tip ring is 0.20 mm (outer copper is 35 µm = 1 oz), so it meets the recommended value. The ring at the sides of the hole is 0.35 mm.
- **D4 circuit:**
  - Pad 1 (cathode) on VBUS, pad 2 on GND.
  - The 0.3 mm GND track runs to USB1 shell pad 13, which sits in solid In1/In2 GND (`review2/renders/usb_in1.png`).
  - D4 is about 10 mm of track from the USB1 VBUS pin. For ESD that hardly matters: D1 and C37 (10 µF) absorb an IEC ESD charge (about 1.2 µC → about 0.12 V).
- **D3 in line:** the D+ stub is 0.49 mm on F.Cu, and the GND pad holds the existing via. D3.1 to the D+ track is 0.11 mm, above JLC's 0.09 mm trace/space. The TP4 B.Cu spur hangs off R3's via-in-pad.
  - USB2 pair skew reads 1.21 mm now (it was 0.13 mm). That is because the B.Cu stub to D3 is gone and the D+ total length is shorter. At full speed it is about 7 ps, irrelevant.
- **C40 and the LDO:**
  - 10 µF 0603 10 V meets the ME6217 output capacitor requirement of ≥ 4.7 µF with ESR ≤ 0.5 Ω (Precautions 3, p.5).
  - The 3V3 track from C40 to U3.5 is 0.3 mm wide, 1.25 mm long, at least 0.65 mm from U3.1 (VSYS) and 0.23 mm from USB_D+.
  - The pad gaps around C40 are all ≥ 0.229 mm.
- **R14 = 1 kΩ:** with JP1/JP4 open (the default), Net-(JP1-A) has no load. With one closed, CS idles at 3.21 V worst case, and only 3.3 mA flows while CS is driven low. With JP4 closed, castellated pad 44 carries the 1 kΩ pull-up, which the README already covers ("the jumper you close takes that pin away").
- **U5:** DNP in schematic and board, no F.Paste on the board or in `Custom.pretty`.
- **Silkscreen** (`review2/renders/silk_*.png`): "40A0" on both sides; JP2/JP3 references horizontal above their boxes, clear of the logo and pad labels; the back "0" clear of JP1's box. The front "41A1" and the 0.8 × 0.55 "40A0" font are accepted.
- **Heat** (`review2/pack/thermal.md`, ambient 35 °C, h = 5/7/10 W/m²K): 13 of 13 candidates have an entry, 0 UNKNOWN.

  | Corner | Total loss | Board average | U3 board temperature | U5 |
  |---|---|---|---|---|
  | typical (80 mA on 3V3) | 0.24 W | 45 °C | 55 °C | – |
  | radio_tx, sustained | 1.65 W (U5 0.85, U3 0.58, U1 0.12, D1 0.10) | 103 °C | 134 °C (nominal h) | 130 °C |

  - Sustained full-rate transmit is not viable, which matches the accepted "bursty transmit" decision in the README.
  - The bare-board time constant is about 230 s, so bursts of seconds do not reach these temperatures.
  - Junction temperatures are not estimated: the ME6217 datasheet gives no SOT-23-5 thermal data.
  - The rework changed U3's VSYS pour from 8.1 to 6.7 mm² (C39 now sits in it). U3's board temperature moved by under 1 K.
- **Decoupling** (`emc.md`): every IC supply pin has a capacitor within 5 mm of copper path.
  - IOVDD 15 and 50 are accepted (m12).
  - The "U6.8: no capacitor reachable" line is a tool artefact. U6.8 sits in the 3V3 pour with C16 about 1.5 mm away (`review2/renders/u6_fcu.png`); the same line appears at HEAD.
- **Sourcing** (global stock, jlcimport-cli 2026-10-29): 23 of 26 LCSC numbers resolve with stock.
  - The lowest are X1 ABM8-272-T3 (845), RP2350B (2,442) and R7 C25086 1 Ω (2,911, Extended; not named in review 1).
  - L1 now shows 30,000.
  - C25105, C25117 and C25744 did not return a row from the CLI today. They are unchanged since review 1, which resolved them.
  - LCSC lists C42415655 as stepping A4. RP2350-E14 affects A2 only and is fixed by the A3 bootrom (datasheet errata D.2.3). That is relevant to the accepted m15 note, not a finding.

## Adversarial pass

An independent reviewer (`review2/pack/adversarial_review.md`) worked from the pack, the project, the datasheets and the HEAD pack. Here is what happened to each of its findings after I checked it against the files:

- **Kept:**

  | Reviewer's claim | Reviewer's rank | Where it went |
  |---|---|---|
  | D3/C39 0.10 mm | Major | M1 |
  | U1.50/C13 0.127 mm | Minor | merged into M1 (same failure mode, same fix) |
  | D4 hardly clamps the hot-plug ring | Minor | m1 |
  | Review-1 Status text is wrong in three places | Minor | m2 |

  New from the reviewer and verified:
  - Adding LDO start-up current to the model still gives 7.0–7.1 V.
  - The 10 µF damper breaks the USB 10 µF attach limit, so m1's fix was changed to 4.7 µF.
  - C-to-C sources don't hot-plug VBUS.
  - The "40A0" font in the Status text is wrong.
  - There is no `D_SOD-523` rule in `transformations.csv` (now m4).
- **Re-ranked:** "production/ is stale" (reviewer: Major). The owner already knows `production/` is stale and has not regenerated it yet, so it is under "Before ordering". The D4 polarity part of it became m4.
- **Pack problems the reviewer raised, all checked:**
  - The U6.8 "no capacitor reachable" FAIL is an artefact.
  - U5.16 is marked "ok" at 6.2 mm of path against the table's 5 mm limit. Plane path is not counted against the limit. C24 is the RM2's local bulk capacitor; the RM2 also has its own decoupling inside the module.
  - The U3 output hot-loop row now names C38 (100 nF, 1.38 mm), because it is nearer than C40 (1.52 mm). Both are listed in the capacitor table.
  - The USB2 "skew" of 1.21 mm includes the test-pad spurs, so it is not a real skew.
  None of these hides a problem.
- **Disagreed:** the reviewer could not get a stock figure for C82044. `jlcimport-cli` returns 310,048 (Extended), global stock, 2026-10-29.

## Limits of this analysis

- **Models, not measurements:**
  - The hot-plug numbers (m1) come from an ODE with assumed cable L/R and a two-point piecewise TVS model, with C37 at 5 µF effective. The C37 DC-bias value is not checked against Samsung's curve: neither the LCSC catalogue nor Samsung's product page gives one.
  - The C40 bias derating is likewise unverified.
- **Thermal:** steady state, bare board in still air, h 5–10 W/m²K. No carrier board, enclosure or airflow. U1's loss is an estimate. There are no junction estimates (no psi_JB / theta_JC for U3 or U5).
- **DC only for power; geometry heuristics for EMC.** No AC impedance, RF or ESD simulation.
- **USB impedance:** the pack's "Zdiff 133/144 Ω vs 90" warning is an edge-coupled estimate. It does not matter at full speed, and the fab calculator was not run.
- **Not verified:**
  - JLC's DFM verdict on M1 (only the published limits)
  - JLC's placement preview of D4, D3, C39 and C40 (production is stale)
  - 3D clearances
  - gerber content
- **Design checks are not qualification.** Electrical, thermal and reflow behaviour on real hardware still need a built board.

## Files

- `review2/pack/`: the pack. Reports: `netlist.md`, `board_overview.md`, `power.md`, `emc.md`, `thermal.md`, `drc.md`, `adversarial_review.md`. Config: `review_config.json`. JSON: `board.json`, `emc.json`, `decoupling.json`, `thermal.json`, `planes.json`, `islands.json`, `power_runs_inner_15.2um.json`, `drc.json`, `erc.json`, `net.xml`.
- `review2/renders/`: `usb_fcu.png`, `usb_bcu.png`, `usb_in1.png`, `in1_vreg.png`, `vreg_fcu.png`, `u6_fcu.png`, `u1_p50_c13.png`, `silk_f_40A0.png`, `silk_b_40A0.png`, `silk_b_jp23.png`, `silk_b_jp1_0.png`, `silk_f_usb.png`.
- `review2/make_pack.log`: the pack build log.
- The pack's refilled project copy (`review2/pack/proj/`, 40 MB) was deleted after the review. Re-run `make_pack.sh` to recreate it.
- `review2/scripts/`: the measurement scripts used above (`padgaps.py`, `gaps.py`, `shift.py`, `j4u5.py`, `usbref.py`, `cutdist.py`, `cutcover.py`, `hotplug.py`). Each takes a pack's `board.json` as its argument. Run them with the kicad-skills analysis venv.
- Datasheets and the HEAD baseline pack are in `/tmp/psr2/` and are not kept.
