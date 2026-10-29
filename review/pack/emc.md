# EMC and signal integrity (geometry heuristics)

Notes: Hammerstad microstrip over the nearest copper layer (zero thickness); inner layers treated the same way, so stripline Z0 is overstated; coupling k = 1/(1+(D/h)^2), D centre spacing, h height over the reference; saturated backward crosstalk ~ k/4

## Fast nets off their reference plane

| Net | Class | Layer | Ref | Length mm | Off ground (what, mm) | Longest spans |
|---|---|---|---|---|---|---|
| /VREG_LX | switch | F.Cu | In1.Cu | 2.8 | GND_edge 0.1, void 2.7 | 2.7 mm over void at [137.25, 99.2] |
| ADC_VREF | sensitive | F.Cu | In1.Cu | 14.5 | GND_edge 0.4, void 0.3 | 0.3 mm over void at [127.9, 95.43]; 0.2 mm over GND_edge at [128.1, 95.43]; 0.2 mm over GND_edge at [127.59, 95.43] |
| GPIO24 | spi | B.Cu | In2.Cu | 36.5 | void 0.1 |  |
| GPIO25 | spi | F.Cu | In1.Cu | 22.2 | GND_edge 0.7 | 0.7 mm over GND_edge at [147.57, 104.0] |
| GPIO29 | spi | F.Cu | In1.Cu | 34.0 | void 0.1, GND_edge 1.1 | 0.7 mm over GND_edge at [158.19, 98.3]; 0.3 mm over GND_edge at [147.39, 99.6] |
| GPIO29 | spi | B.Cu | In2.Cu | 27.2 | GND_edge 4.3 | 1.1 mm over GND_edge at [177.36, 109.36]; 1.1 mm over GND_edge at [172.25, 109.36]; 1.0 mm over GND_edge at [179.77, 109.36] |
| GPIO47{slash}ADC7 | qspi | F.Cu | In1.Cu | 25.9 | GND_edge 6.7 | 1.2 mm over GND_edge at [150.89, 93.61]; 1.1 mm over GND_edge at [143.29, 93.61]; 1.1 mm over GND_edge at [145.89, 93.61] |
| GPIO47{slash}ADC7 | qspi | B.Cu | In2.Cu | 1.5 | GND_edge 0.1 |  |
| GPIO47{slash}ADC7 | qspi | In1.Cu | F.Cu | 14.5 | void 13.8 | 10.0 mm over void at [128.75, 94.05]; 2.5 mm over void at [127.8, 97.45]; 1.3 mm over void at [127.8, 95.0] |
| Net-(U1-XOUT) | clock | F.Cu | In1.Cu | 3.3 | GND_edge 0.7 | 0.7 mm over GND_edge at [148.22, 102.03] |
| QSPI_SCLK | qspi | F.Cu | In1.Cu | 5.4 | GND_edge 0.1 |  |
| QSPI_SCLK | qspi | B.Cu | In2.Cu | 7.2 | GND_edge 0.7 | 0.7 mm over GND_edge at [130.98, 100.51] |
| QSPI_SD2 | qspi | F.Cu | In1.Cu | 14.3 | GND_edge 0.5 | 0.5 mm over GND_edge at [133.14, 106.45] |
| QSPI_SD2 | qspi | B.Cu | In2.Cu | 7.6 | GND_edge 0.1 |  |
| QSPI_SD3 | qspi | B.Cu | In2.Cu | 7.2 | GND_edge 0.7 | 0.7 mm over GND_edge at [131.32, 102.48] |
| RUN | sensitive | F.Cu | In1.Cu | 24.8 | GND_edge 1.5, void 0.5 | 0.6 mm over GND_edge at [147.4, 100.42]; 0.5 mm over void at [134.6, 94.2]; 0.5 mm over GND_edge at [147.95, 100.42] |
| RUN | sensitive | B.Cu | In2.Cu | 30.6 | void 0.1 |  |
| SWCLK | swd | F.Cu | In1.Cu | 12.1 | GND_edge 0.4 | 0.2 mm over GND_edge at [147.51, 101.2] |
| SWDIO | swd | F.Cu | In1.Cu | 17.0 | GND_edge 0.7 | 0.6 mm over GND_edge at [157.58, 100.05] |
| USB2_D+ | usb | F.Cu | In1.Cu | 6.2 | GND_edge 0.1 |  |
| USB_D- | usb | F.Cu | In1.Cu | 17.3 | GND_edge 0.5 | 0.3 mm over GND_edge at [134.71, 100.56]; 0.2 mm over GND_edge at [134.81, 100.56] |

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

## Hot loops (IC pin -> cap -> IC ground)

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
| U1 | RP2350 VREG_VIN input (CIN) | C40 | CL05A106MQ5NUNC | 14.09 | 15.27 | 18.1 |
| U3 | ME6217 LDO input | C37 | 10uF | 1.75 | 2.01 | 2.1 |
| U3 | ME6217 LDO input | C39 | CL05B104KO5NNNC | 2.10 | 3.37 | 1.7 |
| U3 | ME6217 LDO output | C40 | CL05A106MQ5NUNC | 1.30 | 2.80 | 2.2 |
| U3 | ME6217 LDO output | C38 | CL05B104KO5NNNC | 1.38 | 4.06 | 1.0 |
| U3 | ME6217 LDO output | C16 | 100nF | 10.83 | 13.77 | 7.2 |
| U3 | ME6217 LDO output | C4 | 100nF | 11.64 | 13.91 | 11.3 |
| U3 | ME6217 LDO output | C12 | 4.7uF | 13.38 | 16.08 | 5.0 |
| U3 | ME6217 LDO output | C9 | 100nF | 13.50 | 14.91 | 4.3 |
| U3 | ME6217 LDO output | C8 | 100nF | 13.65 | 15.20 | 14.3 |

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
| USB2_D+ | usb | D3.2 R3.2 TP4.1 USB1.6 USB1.8 | 9.1 | {'F.Cu': 6.2, 'B.Cu': 2.9} | 2 | {'F.Cu@0.16': 80.0, 'B.Cu@0.15': 82.3, 'B.Cu@0.2': 72.3} |
| USB2_D- | usb | D2.2 R2.2 TP3.1 USB1.5 USB1.7 | 9.2 | {'F.Cu': 7.0, 'B.Cu': 2.2} | 1 | {'F.Cu@0.15': 82.3, 'F.Cu@0.16': 80.0, 'B.Cu@0.2': 72.3} |
| USB_D+ | usb | R3.1 U1.67 | 17.4 | {'F.Cu': 17.4} | 0 | {'F.Cu@0.15': 82.3} |
| USB_D- | usb | R2.1 U1.66 | 17.3 | {'F.Cu': 17.3} | 0 | {'F.Cu@0.15': 82.3} |

## Differential pairs

- USB_D+ / USB_D-: lengths [17.42, 17.29] mm, skew 0.13 mm
- USB2_D+ / USB2_D-: lengths [9.09, 9.22] mm, skew 0.13 mm
