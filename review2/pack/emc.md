# EMC and signal integrity (geometry heuristics)

Notes: Hammerstad microstrip over the nearest copper layer (zero thickness); inner layers treated the same way, so stripline Z0 is overstated; coupling k = 1/(1+(D/h)^2), D centre spacing, h height over the reference; saturated backward crosstalk ~ k/4

## Coverage and warnings (read first)

- underived: U1 switches /VREG_LX but no power pin of it has a capacitor to ground: configure its hot loop by hand
- 43 net(s) that reach a connector fell through to "slow" (no reference, crosstalk or edge checks; a cable makes them antennas and ESD entry points): GPIO1 (J4), GPIO2 (J4), GPIO3 (J4), GPIO4 (J4), GPIO5 (J4), GPIO6 (J4), GPIO7 (J4), GPIO8 (J4), GPIO9 (J4), GPIO10 (J4), GPIO11 (J4), GPIO12 (J4), GPIO13 (J4), GPIO14 (J4), GPIO15 (J4), GPIO16 (J4), GPIO17 (J4), GPIO18 (J4), GPIO19 (J4), GPIO20 (J4) - classify each one (its interface speed from the chip's datasheet, or "slow_ext" on purpose)
- diff pair USB_D+/USB_D- on F.Cu: same-layer copper 0.10 mm from the pair at [134.2, 100.86] (median 0.28 mm; it stops mattering beyond about 0.63 mm = max(2 w, 3 h)): the line is partly coplanar and its impedance is LOWER than the edge-coupled 133 ohm (grounded-coplanar estimate at that gap: Z0 70 ohm vs microstrip 82). Keep the pour back along the run (a keepout or a clearance rule) or design it as coplanar, and confirm with the fab's impedance calculator for this stackup
- diff pair USB_D+/USB_D- on F.Cu: Zdiff about 133 ohm vs target 90 (estimate: verify with the fab's calculator)
- diff pair USB2_D+/USB2_D- on F.Cu: same-layer copper 0.35 mm from the pair at [116.72, 100.31] (median 0.92 mm; it stops mattering beyond about 0.63 mm = max(2 w, 3 h)): the line is partly coplanar and its impedance is LOWER than the edge-coupled 144 ohm (grounded-coplanar estimate at that gap: Z0 80 ohm vs microstrip 80). Keep the pour back along the run (a keepout or a clearance rule) or design it as coplanar, and confirm with the fab's impedance calculator for this stackup
- diff pair USB2_D+/USB2_D- on F.Cu: Zdiff about 144 ohm vs target 90 (estimate: verify with the fab's calculator)
- diff pair USB2_D+/USB2_D- on B.Cu: same-layer copper 0.25 mm from the pair at [119.48, 101.3] (median 0.40 mm; it stops mattering beyond about 0.63 mm = max(2 w, 3 h)): the line is partly coplanar and its impedance is LOWER than the edge-coupled 144 ohm (grounded-coplanar estimate at that gap: Z0 70 ohm vs microstrip 72). Keep the pour back along the run (a keepout or a clearance rule) or design it as coplanar, and confirm with the fab's impedance calculator for this stackup
- diff pair USB2_D+/USB2_D- on B.Cu: Zdiff about 144 ohm vs target 90 (estimate: verify with the fab's calculator)
- hot loop U1 RP2350 VREG_VIN input (CIN) (cap C36): ground return: 100 % through one via (0.4/0.2 mm) at [137.09, 96.48] (path 1.6 mOhm)
- hot loop U1 RP2350 VREG output (COUT) (cap C13): ground return: 100 % through one via (0.4/0.2 mm) at [142.32, 95.59] (path 1.5 mOhm)
- hot loop U3 ME6217 LDO input (cap C37): ground return: 100 % through one via (0.4/0.2 mm) at [118.86, 104.67] (path 2.1 mOhm)
- hot loop U3 ME6217 LDO output (cap C38): ground return: 100 % through one via (0.4/0.2 mm) at [124.18, 101.77] (path 2.3 mOhm)
- same-net isolation NOT CHECKED: no "islands" in review_config.json. A single-point or quiet ground merged into the main pour is same-net copper, invisible to DRC and to the hot-loop table (1 switching IC(s) on this board); declare each island (net, layer, its pads, allowed joins) from the datasheet layout rules
- decoupling U6.8 (3V3): FAIL: no capacitor reachable on 3V3 copper from this pin (16 on the net)

## What was classified

- Routed nets per class: clock 3 (fast), power 6, qspi 9 (fast), sensitive 4 (fast), slow 48, spi 6 (fast), swd 2 (fast), switch 1 (fast), usb 4 (fast)
- Fell through to "slow" (no reference, crosstalk or edge checks), longest first: GPIO36 54 mm, GPIO37 54 mm, GPIO35 51 mm, GPIO38 48 mm, GPIO34 43 mm, GPIO39 43 mm, GPIO33 40 mm, GPIO40{slash}ADC0 40 mm, GPIO41{slash}ADC1 39 mm, GPIO31 37 mm, GPIO42{slash}ADC2 37 mm, GPIO32 36 mm, GPIO30 35 mm, GPIO43{slash}ADC3 34 mm, GPIO44{slash}ADC4 32 mm
- Switch nodes derived from the netlist: /VREG_LX (inductor L1.1 meets U1.63 with no capacitor to ground; class switch by rule 5)
- Switching ICs: U1 RP2350B_C42415655: buck or boost: inductor DC side on 1V1, hot loops config

## Fast nets off their reference plane, by severity

- Counts: high 4, medium 0, low 11

### High: Over nothing (void): a slot under the signal, fix first

| Net | Class | Layer | Ref | Length mm | Off ground (what, mm) | Spans |
|---|---|---|---|---|---|---|
| GPIO47{slash}ADC7 | qspi | In1.Cu | F.Cu | 14.5 | void 13.8 | 10.0 mm over void at [128.75, 94.05], coplanar ground 74 %; 2.5 mm over void at [127.8, 97.45], coplanar ground 100 %; 1.3 mm over void at [127.8, 95.0], coplanar ground 100 % |
| /VREG_LX | switch | F.Cu | In1.Cu | 2.8 | GND_edge 0.1, void 2.7 | 2.7 mm over void at [137.25, 99.2] |
| RUN | sensitive | F.Cu | In1.Cu | 24.8 | GND_edge 1.5, void 0.5 | 0.5 mm over void at [134.6, 94.2]; 0.6 mm over GND_edge at [147.4, 100.42]; 0.5 mm over GND_edge at [147.95, 100.42] |
| ADC_VREF | sensitive | F.Cu | In1.Cu | 14.5 | GND_edge 0.4, void 0.3 | 0.3 mm over void at [127.9, 95.43]; 0.2 mm over GND_edge at [128.1, 95.43]; 0.2 mm over GND_edge at [127.59, 95.43] |

### Medium: Over another net's plane: the return goes through that plane's decoupling - check a cap sits near each end

- none

### Low: Ground edge only, or another net's plane with ground pour on both sides on the same layer

| Net | Class | Layer | Ref | Length mm | Off ground (what, mm) | Spans |
|---|---|---|---|---|---|---|
| GPIO47{slash}ADC7 | qspi | F.Cu | In1.Cu | 25.9 | GND_edge 6.7 | 1.2 mm over GND_edge at [150.89, 93.61]; 1.1 mm over GND_edge at [143.29, 93.61]; 1.1 mm over GND_edge at [145.89, 93.61] |
| GPIO29 | spi | B.Cu | In2.Cu | 27.2 | GND_edge 4.3 | 1.1 mm over GND_edge at [177.36, 109.36]; 1.1 mm over GND_edge at [172.25, 109.36]; 1.0 mm over GND_edge at [179.77, 109.36] |
| GPIO29 | spi | F.Cu | In1.Cu | 34.0 | void 0.1, GND_edge 1.1 | 0.7 mm over GND_edge at [158.19, 98.3]; 0.3 mm over GND_edge at [147.39, 99.6] |
| Net-(U1-XOUT) | clock | F.Cu | In1.Cu | 3.3 | GND_edge 0.7 | 0.7 mm over GND_edge at [148.22, 102.03] |
| QSPI_SCLK | qspi | B.Cu | In2.Cu | 7.2 | GND_edge 0.7 | 0.7 mm over GND_edge at [130.98, 100.51] |
| QSPI_SD3 | qspi | B.Cu | In2.Cu | 7.2 | GND_edge 0.7 | 0.7 mm over GND_edge at [131.32, 102.48] |
| SWDIO | swd | F.Cu | In1.Cu | 17.0 | GND_edge 0.7 | 0.6 mm over GND_edge at [157.58, 100.05] |
| GPIO25 | spi | F.Cu | In1.Cu | 22.2 | GND_edge 0.7 | 0.7 mm over GND_edge at [147.57, 104.0] |
| QSPI_SD2 | qspi | F.Cu | In1.Cu | 14.3 | GND_edge 0.5 | 0.5 mm over GND_edge at [133.14, 106.45] |
| USB_D- | usb | F.Cu | In1.Cu | 17.3 | GND_edge 0.5 | 0.3 mm over GND_edge at [134.71, 100.56]; 0.2 mm over GND_edge at [134.81, 100.56] |
| SWCLK | swd | F.Cu | In1.Cu | 12.1 | GND_edge 0.4 | 0.2 mm over GND_edge at [147.51, 101.2] |

## Crosstalk (top 30 by coupled length x k)


| Net | Other | Layers | Kind | Coupled mm | Centre mm | k | NEXT est % | At |
|---|---|---|---|---|---|---|---|---|
| GPIO29 | GPIO30 | F.Cu/F.Cu | edge | 30.2 | 0.248 | 0.42 | 10.5 | [165.62, 106.78] |
| GPIO47{slash}ADC7 | GPIO46{slash}ADC6 | F.Cu/F.Cu | edge | 24.3 | 0.220 | 0.48 | 11.9 | [160.59, 93.61] |
| GPIO0 | GPIO1 | F.Cu/F.Cu | edge | 19.5 | 0.250 | 0.41 | 10.4 | [124.41, 107.25] |
| GPIO24 | GPIO25 | F.Cu/F.Cu | edge | 17.0 | 0.260 | 0.40 | 9.9 | [147.17, 104.4] |
| SWCLK | SWDIO | F.Cu/F.Cu | edge | 11.2 | 0.220 | 0.48 | 11.9 | [148.77, 100.28] |
| Net-(U1-QSPI_SS) | QSPI_SD1 | F.Cu/F.Cu | edge | 10.7 | 0.250 | 0.41 | 10.4 | [136.02, 103.98] |
| QSPI_SD2 | QSPI_SD1 | F.Cu/F.Cu | edge | 10.6 | 0.250 | 0.41 | 10.4 | [135.93, 103.35] |
| GPIO24 | GPIO23 | F.Cu/F.Cu | edge | 11.6 | 0.270 | 0.38 | 9.4 | [161.65, 107.89] |
| SWDIO | RUN | F.Cu/F.Cu | edge | 10.5 | 0.255 | 0.41 | 10.1 | [150.58, 98.65] |
| USB_D+ | USB_D- | F.Cu/F.Cu | edge | 15.4 | 0.350 | 0.27 | 6.6 | [124.21, 100.78] |
| Net-(U1-QSPI_SS) | GPIO0 | F.Cu/F.Cu | edge | 12.5 | 0.302 | 0.33 | 8.2 | [136.02, 103.98] |
| GPIO47{slash}ADC7 | GPIO45{slash}ADC5 | F.Cu/F.Cu | edge | 21.2 | 0.440 | 0.19 | 4.7 | [160.59, 93.61] |
| GPIO29 | RUN | F.Cu/F.Cu | edge | 9.2 | 0.268 | 0.38 | 9.5 | [150.39, 98.05] |
| GPIO24 | Net-(JP3-B) | B.Cu/B.Cu | edge | 13.2 | 0.425 | 0.20 | 4.9 | [164.12, 108.57] |
| RUN | GPIO28 | B.Cu/B.Cu | edge | 7.4 | 0.300 | 0.33 | 8.2 | [131.57, 94.78] |
| QSPI_SD0 | QSPI_SD2 | F.Cu/F.Cu | edge | 5.2 | 0.250 | 0.41 | 10.4 | [136.52, 103.1] |
| GPIO29 | GPIO31 | F.Cu/F.Cu | edge | 15.7 | 0.542 | 0.13 | 3.3 | [165.62, 106.78] |
| GPIO0 | GPIO2 | F.Cu/F.Cu | edge | 12.8 | 0.500 | 0.15 | 3.8 | [124.41, 107.25] |
| GPIO47{slash}ADC7 | GPIO44{slash}ADC4 | F.Cu/F.Cu | edge | 20.2 | 0.660 | 0.09 | 2.3 | [139.26, 94.54] |
| SWDIO | GPIO29 | F.Cu/F.Cu | edge | 13.0 | 0.558 | 0.12 | 3.1 | [150.58, 98.65] |
| SWCLK | RUN | F.Cu/F.Cu | edge | 9.5 | 0.475 | 0.16 | 4.1 | [148.77, 100.28] |
| QSPI_SCLK | QSPI_SD0 | F.Cu/F.Cu | edge | 3.7 | 0.250 | 0.41 | 10.4 | [137.35, 102.4] |
| Net-(U1-QSPI_SS) | GPIO1 | F.Cu/F.Cu | edge | 11.8 | 0.552 | 0.13 | 3.2 | [136.02, 103.98] |
| RUN | GPIO30 | F.Cu/F.Cu | edge | 8.8 | 0.527 | 0.14 | 3.4 | [149.09, 99.73] |
| QSPI_SD3 | QSPI_SCLK | B.Cu/B.Cu | edge | 3.9 | 0.340 | 0.28 | 6.9 | [131.32, 102.68] |
| RUN | GPIO35 | F.Cu/F.Cu | edge | 5.8 | 0.450 | 0.18 | 4.5 | [173.08, 100.0] |
| RUN | GPIO27 | B.Cu/B.Cu | edge | 4.2 | 0.377 | 0.24 | 5.9 | [131.57, 94.78] |
| Net-(U5-DO) | GPIO38 | F.Cu/F.Cu | edge | 3.5 | 0.340 | 0.28 | 6.9 | [178.27, 95.49] |
| GPIO25 | GPIO23 | F.Cu/F.Cu | edge | 6.9 | 0.530 | 0.14 | 3.4 | [150.04, 104.18] |
| GPIO29 | GPIO25 | F.Cu/F.Cu | edge | 8.2 | 0.588 | 0.11 | 2.8 | [165.62, 106.78] |

## Fast-net layer changes that switch reference, farthest from a ground via first

- GPIO47{slash}ADC7 (qspi) at [127.8, 97.45], layers ['In1.Cu', 'B.Cu'], nearest ground via 3.55 mm
- Net-(JP1-A) (qspi) at [125.59, 96.42], layers ['F.Cu', 'B.Cu'], nearest ground via 3.28 mm
- QSPI_SD0 (qspi) at [132.91, 105.95], layers ['F.Cu', 'B.Cu'], nearest ground via 2.83 mm
- Net-(JP2-A) (spi) at [181.43, 99.0], layers ['F.Cu', 'B.Cu'], nearest ground via 2.51 mm
- QSPI_SCLK (qspi) at [132.91, 104.68], layers ['F.Cu', 'B.Cu'], nearest ground via 2.42 mm
- QSPI_SD1 (qspi) at [125.71, 103.41], layers ['F.Cu', 'B.Cu'], nearest ground via 2.24 mm
- RUN (sensitive) at [130.86, 94.78], layers ['F.Cu', 'B.Cu'], nearest ground via 2.05 mm
- USB2_D+ (usb) at [119.48, 101.3], layers ['F.Cu', 'B.Cu'], nearest ground via 1.99 mm
- GPIO47{slash}ADC7 (qspi) at [139.26, 94.54], layers ['F.Cu', 'In1.Cu'], nearest ground via 1.67 mm
- QSPI_SD3 (qspi) at [132.89, 103.41], layers ['F.Cu', 'B.Cu'], nearest ground via 1.66 mm
- RUN (sensitive) at [157.76, 98.6], layers ['F.Cu', 'B.Cu'], nearest ground via 1.63 mm
- GPIO24 (spi) at [184.01, 96.11], layers ['F.Cu', 'B.Cu'], nearest ground via 1.51 mm
- SWCLK (swd) at [157.12, 100.33], layers ['F.Cu', 'B.Cu'], nearest ground via 1.30 mm
- QSPI_SD2 (qspi) at [125.71, 104.68], layers ['F.Cu', 'B.Cu'], nearest ground via 1.27 mm
- Net-(U1-QSPI_SS) (qspi) at [124.5, 106.23], layers ['F.Cu', 'B.Cu'], nearest ground via 1.21 mm
- RUN (sensitive) at [167.79, 100.25], layers ['F.Cu', 'B.Cu'], nearest ground via 0.96 mm
- GPIO29 (spi) at [187.01, 96.12], layers ['F.Cu', 'B.Cu'], nearest ground via 0.89 mm
- SWDIO (swd) at [157.12, 104.34], layers ['F.Cu', 'B.Cu'], nearest ground via 0.85 mm

## Fast nets within 1 mm of the board edge

- none

## Switching nodes (copper mm^2 per layer)

- /VREG_LX: {'F.Cu': 3.34}

## Hot loops: one row per loop

Source "derived" = taken from the netlist because no configured loop checked that IC: confirm it is a real hot loop in the datasheet layout section. The nearest capacitor is not necessarily the one the datasheet asks for at that pin: compare the value with its typical application.

Electrical columns: a 1 A DC solve from the IC pins to the nearest capacitor (ground return / supply side): path resistance, share of the current that leaves the component layer through vias, share in the busiest via. A short loop whose return dives through one via is not a short loop. Neither column can see a same-net merge (a single-point or quiet ground joined to the main pour is legal copper): that is the "Same-net isolation" table below.

| IC | Loop | Source | Status | Nearest cap (value, pin-cap mm, area mm^2) | Smallest cap (value, mm) | Gnd return (mOhm, via %, top via %) | Supply side (mOhm, via %, top via %) | Flags |
|---|---|---|---|---|---|---|---|---|
| U1 | RP2350 VREG_VIN input (CIN) | config | ok | C36 100nF, 0.91, 1.9 | C36 100nF, 0.91 | 1.55, 100 %, 100 % | 1.30, 0 %, 0 % | ground return: 100 % through one via (0.4/0.2 mm) at [137.09, 96.48] (path 1.6 mOhm) |
| U1 | RP2350 VREG output (COUT) | config | ok | C13 100nF, 0.79, 3.9 | C13 100nF, 0.79 | 1.52, 100 %, 100 % | 1.05, 0 %, 0 % | ground return: 100 % through one via (0.4/0.2 mm) at [142.32, 95.59] (path 1.5 mOhm) |
| U3 | ME6217 LDO input | config | ok | C37 10uF, 1.75, 2.1 | C37 10uF, 1.75 | 2.13, 100 %, 100 % | 0.46, 0 %, 0 % | ground return: 100 % through one via (0.4/0.2 mm) at [118.86, 104.67] (path 2.1 mOhm) |
| U3 | ME6217 LDO output | config | ok | C38 CL05B104KO5NNNC, 1.38, 1.0 | C16 100nF, 10.83 | 2.26, 100 %, 100 % | 0.38, 0 %, 0 % | ground return: 100 % through one via (0.4/0.2 mm) at [124.18, 101.77] (path 2.3 mOhm) |

### Every capacitor in each loop (IC pin -> cap -> IC ground)

| IC | Loop | Cap | Value | Pin-cap mm | Gnd-cap mm | Loop area mm^2 |
|---|---|---|---|---|---|---|
| U1 | RP2350 VREG output (COUT) | C13 | 100nF | 0.79 | 5.92 | 3.9 |
| U1 | RP2350 VREG output (COUT) | C5 | 4.7uF | 1.02 | 6.63 | 2.5 |
| U1 | RP2350 VREG output (COUT) | C2 | 100nF | 1.25 | 7.15 | 0.2 |
| U1 | RP2350 VREG output (COUT) | C10 | 4.7uF | 2.47 | 2.45 | 2.6 |
| U1 | RP2350 VREG_VIN input (CIN) | C36 | 100nF | 0.91 | 2.34 | 1.9 |
| U1 | RP2350 VREG_VIN input (CIN) | C1 | 100nF | 0.95 | 7.16 | 0.3 |
| U1 | RP2350 VREG_VIN input (CIN) | C7 | 100nF | 1.00 | 7.37 | 2.4 |
| U1 | RP2350 VREG_VIN input (CIN) | C8 | 100nF | 1.04 | 6.62 | 4.5 |
| U1 | RP2350 VREG_VIN input (CIN) | C9 | 100nF | 1.08 | 3.43 | 2.8 |
| U1 | RP2350 VREG_VIN input (CIN) | C6 | 100nF | 1.18 | 7.08 | 0.5 |
| U1 | RP2350 VREG_VIN input (CIN) | C12 | 4.7uF | 1.49 | 1.48 | 1.3 |
| U1 | RP2350 VREG_VIN input (CIN) | C22 | 100nF | 1.83 | 8.05 | 7.2 |
| U1 | RP2350 VREG_VIN input (CIN) | C3 | 100nF | 2.05 | 8.04 | 1.9 |
| U1 | RP2350 VREG_VIN input (CIN) | C4 | 100nF | 2.94 | 4.94 | 3.1 |
| U1 | RP2350 VREG_VIN input (CIN) | C16 | 100nF | 5.63 | 5.70 | 4.5 |
| U1 | RP2350 VREG_VIN input (CIN) | C38 | CL05B104KO5NNNC | 13.22 | 13.50 | 24.8 |
| U3 | ME6217 LDO input | C37 | 10uF | 1.75 | 2.01 | 2.1 |
| U3 | ME6217 LDO input | C39 | CL05B104KO5NNNC | 2.68 | 2.68 | 2.6 |
| U3 | ME6217 LDO output | C38 | CL05B104KO5NNNC | 1.38 | 4.06 | 1.0 |
| U3 | ME6217 LDO output | C40 | 10uF | 1.52 | 3.33 | 0.7 |
| U3 | ME6217 LDO output | C16 | 100nF | 10.83 | 13.77 | 7.2 |
| U3 | ME6217 LDO output | C4 | 100nF | 11.64 | 13.91 | 11.3 |
| U3 | ME6217 LDO output | C12 | 4.7uF | 13.38 | 16.08 | 5.0 |
| U3 | ME6217 LDO output | C9 | 100nF | 13.50 | 14.91 | 4.3 |
| U3 | ME6217 LDO output | C8 | 100nF | 13.65 | 15.20 | 14.3 |

## Same-net isolation: declared islands (filled copper)

Each island declared in review_config.json "islands" (a single-point or quiet ground, a local pour) on the filled copper: one piece, no other pad of its net in it, and no more joins to other layers than allowed. DRC and the hot-loop table cannot see a same-net merge; without declarations this check did not run.

- **NOT CHECKED**: no islands declared (see coverage)

## Decoupling: nearest capacitor per IC supply pin, by copper path

Path along the net's own copper from the pin to the nearest capacitor between that net and ground: track length, length across a filled plane or pour, via hops, and an inductance estimate (path along the net's copper (tracks, vias, straight lines across filled pieces); inductance from microstrip per-length L on each track and the via barrels; plane spreading and the capacitor's own mounting are not included). Flag: more than 5.0 mm of track, or the capacitor's ground pad far from a ground via. Pins with no capacitor on their net: U1.63 (/VREG_LX): no capacitor between it and ground; U3.3 (3V3_EN): no capacitor between it and ground; USB1.2 (VBUS): no capacitor between it and ground; USB1.11 (VBUS): no capacitor between it and ground.

| IC | Pin | Net | Plane? | Nearest cap | Path mm (track / plane / vias) | Est. nH | Caps within limit | Cap gnd via mm | Status |
|---|---|---|---|---|---|---|---|---|---|
| U6 | 8 VCC | 3V3 | yes | -  | - | - | - of - | - | FAIL: no capacitor reachable on 3V3 copper from this pin (16 on the net) |
| U1 | 65 VREG_FB | 1V1 | yes | C10 4.7uF | 2.9 (2.2 / 0.7 / 0) | 0.95 | 1 of 4 | 0.0 | ok |
| U1 | 32 DVDD | 1V1 | yes | C2 100nF | 1.3 (1.3 / 0.0 / 0) | 0.48 | 1 of 4 | 0.0 | ok |
| U1 | 29 IOVDD | 3V3 | yes | C6 100nF | 1.2 (1.2 / 0.0 / 0) | 0.48 | 3 of 16 | 0.0 | ok |
| U1 | 24 IOVDD | 3V3 | yes | C7 100nF | 1.1 (1.1 / 0.0 / 0) | 0.41 | 3 of 16 | 0.0 | ok |
| U1 | 10 DVDD | 1V1 | yes | C5 4.7uF | 1.1 (1.1 / 0.0 / 0) | 0.42 | 1 of 4 | 0.0 | ok |
| U1 | 76 IOVDD | 3V3 | yes | C8 100nF | 1.1 (1.1 / 0.0 / 0) | 0.44 | 4 of 16 | 0.0 | ok |
| U1 | 41 IOVDD | 3V3 | yes | C22 100nF | 1.9 (1.0 / 0.8 / 0) | 0.40 | 1 of 16 | 0.0 | ok |
| U1 | 61 VREG_AVDD | Net-(U1-VREG_AVDD) | no | C11 4.7uF | 1.0 (1.0 / 0.0 / 0) | 0.51 | 1 of 1 | 0.0 | ok |
| U1 | 15 IOVDD | 3V3 | yes | C3 100nF | 3.9 (1.0 / 3.0 / 0) | 0.38 | 3 of 16 | 0.0 | ok |
| U1 | 50 IOVDD | 3V3 | yes | C36 100nF | 5.0 (1.0 / 4.0 / 0) | 0.38 | 1 of 16 | 0.0 | ok |
| U1 | 60 IOVDD | 3V3 | yes | C36 100nF | 1.0 (1.0 / 0.0 / 0) | 0.38 | 2 of 16 | 0.0 | ok |
| U1 | 5 IOVDD | 3V3 | yes | C1 100nF | 1.0 (1.0 / 0.0 / 0) | 0.37 | 2 of 16 | 0.0 | ok |
| U1 | 51 DVDD | 1V1 | yes | C13 100nF | 0.8 (0.8 / 0.0 / 0) | 0.45 | 1 of 4 | 0.0 | ok |
| U1 | 64 VREG_VIN | 3V3 | yes | C9 100nF | 2.2 (0.0 / 2.2 / 0) | 0.00 | 3 of 16 | 0.18 | ok |
| U1 | 68 USB_OTP_VDD | 3V3 | yes | C9 100nF | 1.1 (0.0 / 1.1 / 0) | 0.00 | 3 of 16 | 0.18 | ok |
| U1 | 69 QSPI_IOVDD | 3V3 | yes | C9 100nF | 1.1 (0.0 / 1.1 / 0) | 0.00 | 3 of 16 | 0.18 | ok |
| U3 | 1 VIN | VSYS | yes | C37 10uF | 1.8 (0.0 / 1.8 / 0) | 0.00 | 2 of 2 | 0.0 | ok |
| U3 | 5 VOUT | 3V3 | yes | C38 CL05B104KO5NNNC | 1.4 (0.0 / 1.4 / 0) | 0.00 | 2 of 16 | 0.0 | ok |
| U4 | 8 VCC | 3V3 | yes | C4 100nF | 1.6 (0.0 / 1.6 / 0) | 0.00 | 2 of 16 | 0.0 | ok |
| U5 | 14 VDDIO | 3V3 | yes | C24 CL10A475KO8NNNC | 2.6 (0.0 / 2.6 / 0) | 0.00 | 3 of 16 | 0.0 | ok |
| U5 | 16 VIN | 3V3 | yes | C24 CL10A475KO8NNNC | 6.2 (0.0 / 6.2 / 0) | 0.00 | 0 of 16 | 0.0 | ok |

## Fast-net inventory

| Net | Class | Pins | Length mm | Per layer | Vias | Z0 (layer@width: ohm) |
|---|---|---|---|---|---|---|
| /VREG_LX | switch | L1.1 U1.63 | 2.8 | {'F.Cu': 2.8} | 0 | {'F.Cu@0.2': 72.3} |
| ADC_VREF | sensitive | J4.59 R7.2 R8.1 | 14.5 | {'F.Cu': 14.5} | 0 | {'F.Cu@0.15': 82.3} |
| GPIO0 | qspi | J4.1 JP1.2 U1.77 | 32.1 | {'F.Cu': 29.9, 'B.Cu': 2.2} | 0 | {'F.Cu@0.12': 90.1, 'F.Cu@0.15': 82.3, 'B.Cu@0.15': 82.3} |
| GPIO24 | spi | J4.22 R15.2 R16.1 U1.25 U5.5 | 57.3 | {'F.Cu': 20.9, 'B.Cu': 36.5} | 3 | {'F.Cu@0.12': 90.1, 'F.Cu@0.15': 82.3, 'B.Cu@0.15': 82.3, 'B.Cu@0.09': 100.4} |
| GPIO25 | spi | J4.23 JP2.2 U1.26 | 27.6 | {'F.Cu': 22.2, 'B.Cu': 5.4} | 0 | {'F.Cu@0.12': 90.1, 'B.Cu@0.15': 82.3} |
| GPIO29 | spi | J4.24 U1.37 U5.3 | 61.2 | {'F.Cu': 34.0, 'B.Cu': 27.2} | 1 | {'F.Cu@0.15': 82.3, 'F.Cu@0.12': 90.1, 'B.Cu@0.15': 82.3} |
| GPIO47{slash}ADC7 | qspi |  | 41.9 | {'F.Cu': 25.9, 'B.Cu': 1.5, 'In1.Cu': 14.5} | 2 | {'F.Cu@0.12': 90.1, 'B.Cu@0.15': 82.3, 'In1.Cu@0.15': 82.3} |
| Net-(C17-Pad1) | clock | C17.1 R28.1 X1.3 | 3.4 | {'F.Cu': 3.4} | 0 | {'F.Cu@0.15': 82.3} |
| Net-(JP1-A) | qspi | JP1.1 JP4.1 R14.1 U6.1 | 23.9 | {'F.Cu': 1.7, 'B.Cu': 22.2} | 1 | {'F.Cu@0.15': 82.3, 'B.Cu@0.15': 82.3} |
| Net-(JP2-A) | spi | JP2.1 R9.1 U5.9 | 24.1 | {'F.Cu': 3.9, 'B.Cu': 20.2} | 1 | {'F.Cu@0.15': 82.3, 'F.Cu@0.254': 64.3, 'B.Cu@0.15': 82.3, 'B.Cu@0.12': 90.1} |
| Net-(U1-ADC_AVDD) | sensitive | C19.1 R7.1 U1.59 | 4.9 | {'F.Cu': 4.9} | 0 | {'F.Cu@0.15': 82.3} |
| Net-(U1-QSPI_SS) | qspi | R5.2 U1.75 U4.1 | 22.2 | {'F.Cu': 19.8, 'B.Cu': 2.4} | 2 | {'F.Cu@0.12': 90.1, 'F.Cu@0.15': 82.3, 'B.Cu@0.15': 82.3} |
| Net-(U1-VREG_AVDD) | sensitive | C11.1 R6.2 U1.61 | 3.7 | {'F.Cu': 3.7} | 0 | {'F.Cu@0.15': 82.3} |
| Net-(U1-XIN) | clock | C18.2 U1.30 X1.1 | 8.8 | {'F.Cu': 8.8} | 0 | {'F.Cu@0.254': 64.3, 'F.Cu@0.15': 82.3, 'F.Cu@0.12': 90.1} |
| Net-(U1-XOUT) | clock | R28.2 U1.31 | 3.3 | {'F.Cu': 3.3} | 0 | {'F.Cu@0.15': 82.3} |
| Net-(U5-DO) | spi | R15.1 U5.6 | 5.5 | {'F.Cu': 5.5} | 0 | {'F.Cu@0.15': 82.3} |
| Net-(U5-nIRQ) | spi | R16.2 U5.10 | 8.5 | {'F.Cu': 8.5} | 0 | {'F.Cu@0.15': 82.3} |
| QSPI_SCLK | qspi | U1.71 U4.6 U6.6 | 12.6 | {'F.Cu': 5.4, 'B.Cu': 7.2} | 2 | {'F.Cu@0.12': 90.1, 'F.Cu@0.15': 82.3, 'B.Cu@0.15': 82.3} |
| QSPI_SD0 | qspi | U1.72 U4.5 U6.5 | 13.4 | {'F.Cu': 6.2, 'B.Cu': 7.2} | 2 | {'F.Cu@0.12': 90.1, 'F.Cu@0.15': 82.3, 'B.Cu@0.15': 82.3} |
| QSPI_SD1 | qspi | U1.74 U4.2 U6.2 | 24.2 | {'F.Cu': 17.8, 'B.Cu': 6.4} | 2 | {'F.Cu@0.12': 90.1, 'B.Cu@0.15': 82.3} |
| QSPI_SD2 | qspi | U1.73 U4.3 U6.3 | 21.9 | {'F.Cu': 14.3, 'B.Cu': 7.6} | 2 | {'F.Cu@0.12': 90.1, 'B.Cu@0.15': 82.3} |
| QSPI_SD3 | qspi | U1.70 U4.7 U6.7 | 12.2 | {'F.Cu': 5.0, 'B.Cu': 7.2} | 2 | {'F.Cu@0.15': 82.3, 'B.Cu@0.15': 82.3} |
| RUN | sensitive | C15.2 J4.54 Reset1.2 U1.35 | 55.4 | {'F.Cu': 24.8, 'B.Cu': 30.6} | 4 | {'F.Cu@0.12': 90.1, 'F.Cu@0.15': 82.3, 'B.Cu@0.12': 90.1, 'B.Cu@0.15': 82.3} |
| SWCLK | swd | J2.1 U1.33 | 15.9 | {'F.Cu': 12.1, 'B.Cu': 3.8} | 1 | {'F.Cu@0.12': 90.1, 'B.Cu@0.12': 90.1} |
| SWDIO | swd | J2.3 U1.34 | 20.3 | {'F.Cu': 17.0, 'B.Cu': 3.4} | 1 | {'F.Cu@0.12': 90.1, 'B.Cu@0.12': 90.1} |
| USB2_D+ | usb | D3.2 R3.2 TP4.1 USB1.6 USB1.8 | 8.0 | {'F.Cu': 6.7, 'B.Cu': 1.3} | 1 | {'F.Cu@0.16': 80.0, 'B.Cu@0.2': 72.3} |
| USB2_D- | usb | D2.2 R2.2 TP3.1 USB1.5 USB1.7 | 9.2 | {'F.Cu': 7.0, 'B.Cu': 2.2} | 1 | {'F.Cu@0.15': 82.3, 'F.Cu@0.16': 80.0, 'B.Cu@0.2': 72.3} |
| USB_D+ | usb | R3.1 U1.67 | 17.4 | {'F.Cu': 17.4} | 0 | {'F.Cu@0.15': 82.3} |
| USB_D- | usb | R2.1 U1.66 | 17.3 | {'F.Cu': 17.3} | 0 | {'F.Cu@0.15': 82.3} |

## Differential pairs

Zdiff: edge-coupled microstrip estimate from the measured width and gap (an estimate: confirm with the fab's impedance calculator for the exact stackup). Pour gap: from the pair's edge to the nearest other same-layer copper; below about max(2 w, 3 h) the line is partly coplanar and its impedance is lower.

- USB_D+ / USB_D-: lengths [17.42, 17.29] mm, skew 0.13 mm, target 90 ohm
  - F.Cu: w 0.150, gap 0.200, h 0.210 mm, coupled 17.9 mm: Z0 82, Zdiff 133 ohm; pour gap min 0.1 / median 0.28 mm - **same-layer copper 0.10 mm from the pair at [134.2, 100.86] (median 0.28 mm; it stops mattering beyond about 0.63 mm = max(2 w, 3 h)): the line is partly coplanar and its impedance is LOWER than the edge-coupled 133 ohm (grounded-coplanar estimate at that gap: Z0 70 ohm vs microstrip 82). Keep the pour back along the run (a keepout or a clearance rule) or design it as coplanar, and confirm with the fab's impedance calculator for this stackup**
- USB2_D+ / USB2_D-: lengths [8.01, 9.22] mm, skew 1.21 mm, target 90 ohm
  - F.Cu: w 0.160, gap 0.340, h 0.210 mm, coupled 7.2 mm: Z0 80, Zdiff 144 ohm; pour gap min 0.345 / median 0.918 mm - **same-layer copper 0.35 mm from the pair at [116.72, 100.31] (median 0.92 mm; it stops mattering beyond about 0.63 mm = max(2 w, 3 h)): the line is partly coplanar and its impedance is LOWER than the edge-coupled 144 ohm (grounded-coplanar estimate at that gap: Z0 80 ohm vs microstrip 80). Keep the pour back along the run (a keepout or a clearance rule) or design it as coplanar, and confirm with the fab's impedance calculator for this stackup**
  - B.Cu: w 0.200, gap 1.141, h 0.210 mm, coupled 0.4 mm: Z0 72, Zdiff 144 ohm; pour gap min 0.25 / median 0.396 mm - **same-layer copper 0.25 mm from the pair at [119.48, 101.3] (median 0.40 mm; it stops mattering beyond about 0.63 mm = max(2 w, 3 h)): the line is partly coplanar and its impedance is LOWER than the edge-coupled 144 ohm (grounded-coplanar estimate at that gap: Z0 70 ohm vs microstrip 72). Keep the pour back along the run (a keepout or a clearance rule) or design it as coplanar, and confirm with the fab's impedance calculator for this stackup**
