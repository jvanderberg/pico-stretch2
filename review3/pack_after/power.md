# Power distribution and planes

Method: resistive-grid DC solve per net over the saved copper (zone fills, tracks, pads) on every layer, joined by via barrels (20 um plating) and plated pads. Copper at 20 C (+0.39 %/C). The source pad is 0 V; each sink draws its current; "drop" is the mean voltage over the sink pad. Hotspots: current per mm of copper width above 75 % of a rough IPC-2221 isolated-trace limit (outer 3.2 A/mm, inner 1.6 A/mm), pessimistic for planes. Component drops (fuses, FETs, shunts, connectors) are not included. Heat (these copper losses plus every part's) and temperatures: thermal.md.

## Coverage and warnings (read first)

- underived: U1 switches /VREG_LX but no power pin of it has a capacitor to ground: configure its hot loop by hand
- 43 net(s) that reach a connector fell through to "slow" (no reference, crosstalk or edge checks; a cable makes them antennas and ESD entry points): GPIO1 (J4), GPIO2 (J4), GPIO3 (J4), GPIO4 (J4), GPIO5 (J4), GPIO6 (J4), GPIO7 (J4), GPIO8 (J4), GPIO9 (J4), GPIO10 (J4), GPIO11 (J4), GPIO12 (J4), GPIO13 (J4), GPIO14 (J4), GPIO15 (J4), GPIO16 (J4), GPIO17 (J4), GPIO18 (J4), GPIO19 (J4), GPIO20 (J4) - classify each one (its interface speed from the chip's datasheet, or "slow_ext" on purpose)
- no ground copper (zones on ['GND']) on B.Cu

## Runs: inner_15.2um

| Run | What | Copper loss (W) | Worst drop (mV) | R_eff (mOhm) | Busiest via (A) | Hotspots over limit |
|---|---|---|---|---|---|---|
| vbus | USB-C VBUS pins to D1 anode and castellated VBUS pad, 0.9 A | 0.00 | 3.2 | 3.6 | 0.00 @ 110.8,92.6 | F.Cu 3.7 @ 116.8,98.6 |
| vsys | D1 cathode to LDO input, 0.9 A | 0.01 | 19.9 | 17.9 | 0.90 @ 119.3,102.1 | B.Cu 6.0 @ 119.0,101.8 |
| p3v3 | LDO out to RP2350 VREG_VIN, IOVDD, flash, RM2 and the 3V3 pad | 0.01 | 28.3 | 18.9 | 0.35 @ 176.2,104.0 | F.Cu 4.1 @ 124.8,101.8 |
| p1v1 | L1 output to RP2350 DVDD pins, 0.2 A | 0.00 | 4.2 | 14.0 | 0.20 @ 140.1,100.2 | - |
| gnd_return | Ground return from RP2350, RM2, LDO and 3V3 pad load to USB-C GND pins | 0.00 | -0.6 | 1.1 | 0.44 @ 115.9,97.9 | - |

- p3v3 per sink (mV): U1.64 11, U1.5 11, U1.15 11, U1.24 11, U1.29 11, U1.41 11, U1.50 11, U1.60 11, U1.76 11, U1.69 10, U4.8 9, U5.16 28, J4.60 13
- p1v1 per sink (mV): U1.10 4, U1.32 4, U1.51 4
- gnd_return per sink (mV): U1.81 -1, U1.62 -1, U5.15 -2, U3.2 -1, J4.62 -1

## Ground planes

- F.Cu: 21 mm^2 (1.2 % of board), 2 pieces. Largest piece: 0 slots. Longest: none
- In1.Cu: 1390 mm^2 (80.6 % of board), 1 pieces. Largest piece: 8 slots. Longest: track corridors 16 mm long, 0.36 mm mean width, 6 mm^2, spanning [127.4, 93.9, 139.6, 97.8]: tracks GPIO47{slash}ADC7; 2 vias (GPIO47{slash}ADC7); 5.5x3.1 mm slot at [131.8, 97.5, 137.3, 100.5]: 2 vias (3V3, 1V1); 2.1x0.7 mm slot at [151.3, 106.4, 153.1, 108.0]: small; 1.9x1.9 mm slot at [159.4, 98.0, 161.3, 99.9]: small; 1.9x1.9 mm slot at [159.4, 103.0, 161.3, 104.9]: small
- In2.Cu: 1402 mm^2 (81.3 % of board), 1 pieces. Largest piece: 6 slots. Longest: 2.1x0.7 mm slot at [151.3, 106.4, 153.1, 108.0]: small; 1.9x1.9 mm slot at [159.4, 98.0, 161.3, 99.9]: small; 1.9x1.9 mm slot at [159.4, 103.0, 161.3, 104.9]: small; 1.9x1.0 mm slot at [149.8, 105.1, 151.2, 106.7]: small; 1.2x1.2 mm slot at [114.3, 97.6, 115.5, 98.8]: small

- Weakly stitched ground pieces (<2 vias): 0. 
- Edge stitching: 93 ground vias within 3 mm of the edge; gaps over 10 mm: none
- Tracks on inner layer In1.Cu (each one cuts that plane): GPIO47{slash}ADC7 14 mm (qspi)
