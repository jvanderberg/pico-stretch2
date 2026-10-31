# Heat: sources, board temperature, thermal vias and stitching

Method: losses per part per corner from `review_config.json` "thermal" (heat.py: I^2 R, converter efficiency, linear drop, given figures, copper loss from the power runs). Temperatures from a steady-state layered solve on this board's copper (thermal_model.py: every copper layer at 0.30 mm cells with nets kept apart, k_cu 385 W/mK, FR4 k 0.30 W/mK between layers, via barrels 20 um plating, each part's heat on its pads, copper loss along each run's copper), cooled from both faces at an effective film coefficient h (convection + radiation) to ambient 35 C. No enclosure air model, no airflow, no heat through wires, cells or mounting: h is the dominant uncertainty, so every temperature is shown at low h = 5 W/m^2K / nominal h = 7 W/m^2K / high h = 10 W/m^2K.

## Coverage and warnings (read first)

- underived: U1 switches /VREG_LX but no power pin of it has a capacitor to ground: configure its hot loop by hand
- 43 net(s) that reach a connector fell through to "slow" (no reference, crosstalk or edge checks; a cable makes them antennas and ESD entry points): GPIO1 (J4), GPIO2 (J4), GPIO3 (J4), GPIO4 (J4), GPIO5 (J4), GPIO6 (J4), GPIO7 (J4), GPIO8 (J4), GPIO9 (J4), GPIO10 (J4), GPIO11 (J4), GPIO12 (J4), GPIO13 (J4), GPIO14 (J4), GPIO15 (J4), GPIO16 (J4), GPIO17 (J4), GPIO18 (J4), GPIO19 (J4), GPIO20 (J4) - classify each one (its interface speed from the chip's datasheet, or "slow_ext" on purpose)
- thermal source D4 is not on the board: its loss is not placed anywhere
- board_T_max_C not set: 105 C ASSUMED as the board limit (FR4 and solder mask in continuous use; check the laminate's Tg / MOT)
- U3 dissipates 0.58 W at some corner but has no psi_jb / theta_jc in thermal.parts: its junction temperature is not estimated (board temperature only) - take them from its datasheet's thermal table
- U5 dissipates 0.85 W at some corner but has no psi_jb / theta_jc in thermal.parts: its junction temperature is not estimated (board temperature only) - take them from its datasheet's thermal table
- U1: heat placed on its thermal pad 81 (thermal.parts.U1.pads overrides)

- Candidate heat sources (by structure: ICs, FETs, inductors, fuses, diodes, beads, resistors <= 1 ohm, parts on power-run ends): 12; with a thermal entry: 12.
- Model: 274 x 70 cells per layer, 76724 nodes, 370 vias / plated holes joining layers, solved in 2.9 s.

## Findings, ranked

- **high**: corner radio_tx at h nominal: board average 103 C, peak 135 C (F.Cu near U3; board limit 105 C). Over their limit: no part
- **medium**: U3 at radio_tx: 31 K above the board average (0.58 W): heat trapped near the part - see its pours and pads
- **medium**: U5 at radio_tx: 26 K above the board average (0.85 W): heat trapped near the part - see its pours and pads
- **medium**: pour VSYS on F.Cu under U3 (6.8 mm^2): one via only; 9 K between this pour and the layer below (solved, radio_tx, h nominal)
- **medium**: pour 3V3 on F.Cu under U5 (21.6 mm^2): one via only; 4 K between this pour and the layer below (solved, radio_tx, h nominal)

## Heat sources per corner

### typical: USB 5 V, RP2350 running, radio idle or not fitted, 3V3 pin unloaded: about 80 mA on 3V3

Total known: **0.24 W** (conduction 0.00 W, conversion 0.24 W). By group: conversion 0.24 W. UNKNOWN: 0.

| Part | What | Kind | Loss (W) | Inputs | Basis |
|---|---|---|---|---|---|
| U3 | ME6217 LDO | linear | 0.116 | (4.75 - 3.30) V x 0.080 A | VSYS = 5.0 V - D1 VF (0.21 V @0.1 A, 0.31 V @1 A, DFLS130L datasheet) |
| U1 | RP2350B incl. core regulator | fixed | 0.100 | given 0.1 W | estimate: ~30 mA core at 1.1 V via VREG plus IO; not measured |

- Below the 0.05 W listing threshold: D1 0.017 W, U5 0.004 W
- Negligible by decision: U4 (W25Q128 read current ~15 mA (0.05 W) at most); U6 (PSRAM DNP; when fitted a few mA average); L1 (core current ~30-70 mA through a 3.3 uH inductor, I^2 DCR in the mW range); D2 (ESD clamp, off in normal use); D3 (ESD clamp, off in normal use); D4 (VBUS TVS, off below 6.2 V (VBR min)); J4 (castellated pads, no load current through the board in these corners); USB1 (contact resistance x 0.4 A^2, a few mW); R7 (1 ohm ADC_AVDD filter, microamps)

### radio_tx: USB 5 V, RM2 transmitting continuously (271 mA, RM2 datasheet 1.2) plus MCU and flash: 0.40 A on 3V3 (README limits this to bursts)

Total known: **1.65 W** (conduction 0.00 W, conversion 1.65 W). By group: conversion 1.65 W. UNKNOWN: 0.

| Part | What | Kind | Loss (W) | Inputs | Basis |
|---|---|---|---|---|---|
| U5 | RM2 radio module (hand fitted) | fixed | 0.850 | given 0.85 W | 3.3 V x 271 mA Tx MCS7 @16 dBm minus ~40 mW radiated (RM2 datasheet 1.2); PM1 1.19 mA idle |
| U3 | ME6217 LDO | linear | 0.580 | (4.75 - 3.30) V x 0.400 A | VSYS = 5.0 V - D1 VF (0.21 V @0.1 A, 0.31 V @1 A, DFLS130L datasheet) |
| U1 | RP2350B incl. core regulator | fixed | 0.120 | given 0.12 W | estimate: ~30 mA core at 1.1 V via VREG plus IO; not measured |
| D1 | VBUS OR-ing Schottky | fixed | 0.100 | given 0.1 W | VF x I, DFLS130L VF 0.21 V @ 0.1 A, ~0.25 V @ 0.4 A |
- Negligible by decision: U4 (W25Q128 read current ~15 mA (0.05 W) at most); U6 (PSRAM DNP; when fitted a few mA average); L1 (core current ~30-70 mA through a 3.3 uH inductor, I^2 DCR in the mW range); D2 (ESD clamp, off in normal use); D3 (ESD clamp, off in normal use); D4 (VBUS TVS, off below 6.2 V (VBR min)); J4 (castellated pads, no load current through the board in these corners); USB1 (contact resistance x 0.4 A^2, a few mW); R7 (1 ohm ADC_AVDD filter, microamps)

### Per part, every corner (W)

| Part | typical | radio_tx |
|---|---|---|
| U5 | 0.004 | 0.850 |
| U3 | 0.116 | 0.580 |
| U1 | 0.100 | 0.120 |
| D1 | 0.017 | 0.100 |

## Board temperature

Board average = P / (A x (h_top + h_bottom)) with A = 1725 mm^2 (one face): where every watt must go. The solver's mean face rise must equal it (energy balance); the peak above it is what spreading does not remove. A peak close to the average means the board is nearly isothermal (more copper or vias will not help much: only area, airflow or less loss will); a peak far above it means heat is trapped near its source. Board limit: 105 C. Time constant of the bare board (FR4 + copper, parts add to it): 325 s at h low, 232 s at h nominal, 162 s at h high - a corner that lasts much less than that does not reach these temperatures, one that lasts longer does.

| Corner | h (W/m^2K) | Heat placed (W) | Board average rise (P/2Ah) | Solver mean rise | Peak rise | Peak at | Peak T (C) |
|---|---|---|---|---|---|---|---|
| typical | low 5 | 0.24 | 13.7 K | 13.7 K | 25.1 K | F.Cu (121.0, 104.3) near U3 | 60.1 |
| typical | nominal 7 | 0.24 | 9.8 K | 9.8 K | 20.4 K | F.Cu (121.0, 104.3) near U3 | 55.4 |
| typical | high 10 | 0.24 | 6.9 K | 6.9 K | 16.6 K | F.Cu (121.0, 104.3) near U3 | 51.6 |
| radio_tx | low 5 | 1.65 | 95.7 K | 95.6 K | 126.9 K | F.Cu (121.0, 104.3) near U3 | 161.9 |
| radio_tx | nominal 7 | 1.65 | 68.3 K | 68.3 K | 99.8 K | F.Cu (121.0, 104.3) near U3 | 134.8 |
| radio_tx | high 10 | 1.65 | 47.8 K | 47.8 K | 79.5 K | F.Cu (121.0, 104.3) near U3 | 114.5 |

## Parts: board temperature at the pads and junction estimate

T board = ambient + the mean rise over the part's pads. Tj = T board + P x psi_JB (datasheet), or pad + P x theta_JC where the case is the soldered pad; otherwise only the board temperature is known (say so, do not guess a junction).

| Part | Corner | Loss (W) | T board / Tj at h low | T board / Tj at h nominal | T board / Tj at h high | Junction method | Limit |
|---|---|---|---|---|---|---|---|
| U5 RPI Radio Module 2 | radio_tx | 0.850 | 158 / - | 130 / - | 107 / - | no psi_JB / theta_JC given: board temperature only | - |
| U3 ME6217C33M5G | typical | 0.116 | 60 / - | 55 / - | 52 / - | no psi_JB / theta_JC given: board temperature only | - |
| U3 ME6217C33M5G | radio_tx | 0.580 | 161 / - | 134 / - | 114 / - | no psi_JB / theta_JC given: board temperature only | - |
| U1 RP2350B_C42415655 | typical | 0.100 | 54 / - | 50 / - | 46 / - | no psi_JB / theta_JC given: board temperature only | - |
| U1 RP2350B_C42415655 | radio_tx | 0.120 | 122 / - | 95 / - | 76 / - | no psi_JB / theta_JC given: board temperature only | - |
| D1 DFLS130L-7 | radio_tx | 0.100 | 141 / - | 113 / - | 93 / - | no psi_JB / theta_JC given: board temperature only | - |

## Exposed pads and thermal vias

Every pad of 1 mm^2 or more that is at least twice its footprint's median pad (exposed pads, FET drain tabs). Vias count when they are in the pad or beside it within 1.0 mm of its edge (thermal.via_beside_mm): the router refuses open vias in pads, so vias beside the pad are the default and via-in-pad (filled and capped, or tented) is a decision. The finding is judged on the solved temperature step from the pad to the next layer at the part's worst corner; the via count from the datasheet pattern or a rule of thumb is shown for reference. Via conductance is the barrel (k_cu x pi x drill x plating / span) to the nearest layer where the via lands on its own net; dT vias is the drop if all of the part's worst-corner loss went through them (an upper bound).

| Part | Pad | Net | Area mm^2 | In pad / beside | Reference count | R vias (K/W) | Solved step to next layer | dT vias at max loss | Part max W | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| U1 RP2350B_C42415655 | 81 | GND | 11.6 | 9 / 0 | 9 | 3.6 | 0.9 K | 0.4 K | 0.12 | ok |

## Pours under hot parts (stitching for heat)

For every part at or above 0.25 W at some corner, each pour (zone fill) its pads sit on: the same-net vias on the pour that join it to another layer (plated pad holes of the net counted with them and named; tracks leaving the pour are not part of it), the FR4 under it, and from the solve at the part's worst corner (h nominal) the temperature step from the pour to the layer below and the heat that crosses it (through vias / in total). A pour that only FR4 drains, with a step of many kelvin, is where stitching vias - to a plane of the same net - lower the part's temperature.

| Part | Net | Layer | Corner | Pour mm^2 | Vias | G vias / G FR4 (W/K) | Step to layer below (K) | Heat down: vias / total (W) | Under it (next layer) | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| U3 | VSYS | F.Cu | radio_tx | 6.8 | 1 | 0.021 / 0.010 | 8.8 | 0.03 / 0.12 | GND 95% | **medium**: one via only; 9 K between this pour and the layer below (solved, radio_tx, h nominal) |
| U5 | 3V3 | F.Cu | radio_tx | 21.6 | 1 | 0.021 / 0.031 | 3.5 | 0.01 / 0.12 | GND 98% | **medium**: one via only; 4 K between this pour and the layer below (solved, radio_tx, h nominal) |
| U3 | 3V3 | F.Cu | radio_tx | 67.3 | 2 | 0.041 / 0.096 | 0.5 | 0.00 / 0.05 | GND 98% | ok |

## Ground stitching

- Ground vias: 176 (10.20 per cm^2 of board). Per 10 mm square (rows top to bottom, -1 = outside the board): 12 6 11 6 8 5 13 10 1 / 13 11 9 17 21 6 15 9 2 / 0 0 0 0 0 0 0 1 0
- Edge: 93 ground vias or plated ground holes within 3 mm of the edge on a 206 mm perimeter; gaps over 10 mm: none
- Weakly stitched ground pieces (fewer than 2 vias): 0.

## What-if: ground stitching vias every 3.0 mm

- no free spot on the outer ground pour at this pitch

## Limits

- See `analysis-limits.md` (heat). Steady state only; no enclosure air or wall model, no airflow, no heat through wires, cells, connectors or mounting screws; parts' bodies and their own convection are not modelled (heat enters the board at the pads); copper resistance is not iterated with temperature; h is uniform over each face.
