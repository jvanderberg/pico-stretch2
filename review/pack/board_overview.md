# Board overview

- Source: a zone-refilled copy of `pico-stretch2.kicad_pcb` at 8e0d15f
- Outline 82.4 x 21.3 mm, bbox (109.02, 90.86)-(191.41, 112.12). KiCad coordinates: mm, y grows downward.
- Copper layers (top to bottom): F.Cu 35 um at z=0.000 mm, In1.Cu 15 um at z=0.245 mm, In2.Cu 15 um at z=1.326 mm, B.Cu 35 um at z=1.551 mm
- Reference layer per layer (nearest copper, dielectric height): F.Cu -> In1.Cu 0.21 mm; In1.Cu -> F.Cu 0.21 mm, In2.Cu 1.06 mm; In2.Cu -> B.Cu 0.21 mm, In1.Cu 1.06 mm; B.Cu -> In2.Cu 0.21 mm
- 69 footprints (9 on the back), 873 track segments, 237 vias.
- Check with the fab what the copper really is: a file saying 35 um inside often ships as 0.5 oz (17.5 um).

## Copper per layer

| Layer | Track mm | Zone fills (net: mm^2, % of board, pieces) |
|---|---|---|
| F.Cu | 1392 | 3V3: 96, 5.5%, 4; GND: 21, 1.2%, 2; 1V1: 18, 1.0%, 2; VSYS: 12, 0.7%, 2; /VREG_LX: 3, 0.2%, 1 |
| In1.Cu | 14 | GND: 1390, 80.6%, 1 |
| In2.Cu | 0 | GND: 1400, 81.2%, 1 |
| B.Cu | 490 |  |

## Vias

0.4/0.2 mm: 88, 0.45/0.2 mm: 140, 0.63/0.3 mm: 9

By net (top 20): GND 177, 1V1 9, 3V3 5, RUN 4, GPIO24 3, VSYS 2, Net-(Boot1-Pad1) 2, Net-(U1-QSPI_SS) 2, USB2_D+ 2, 3V3_EN 2, GPIO47{slash}ADC7 2, QSPI_SD3 2, QSPI_SCLK 2, QSPI_SD0 2, QSPI_SD2 2, QSPI_SD1 2, SWCLK 1, SWDIO 1, GPIO29 1, Net-(JP2-A) 1

## Track widths (mm of track per width)

- F.Cu: 0.12 mm: 1172, 0.15 mm: 141, 0.16 mm: 12, 0.2 mm: 6, 0.254 mm: 40, 0.4 mm: 8, 0.5 mm: 12
- In1.Cu: 0.15 mm: 15
- In2.Cu: 
- B.Cu: 0.09 mm: 0, 0.12 mm: 147, 0.15 mm: 284, 0.2 mm: 3, 0.254 mm: 20, 0.4 mm: 32, 0.5 mm: 4

## Parts with more than 3 pads

| Ref | Value | Footprint | x | y | rot | side |
|---|---|---|---|---|---|---|
| Boot1 | K2-1808SN-A4SW | K2-1808SN-A4SW | 121.13 | 107.05 | 180 | F |
| J4 | Conn_01x64_Castellated_Pads | Castellated_Pad_64 | 110.80 | 92.60 | 0 | F |
| Reset1 | K2-1808SN-A4SW | K2-1808SN-A4SW | 171.58 | 101.80 | 0 | F |
| U1 | RP2350B_C42415655 | RP2350B_C42415655 | 142.26 | 102.20 | 90 | F |
| U3 | ME6217C33M5G | SOT-23-5 | 121.67 | 103.56 | 0 | F |
| U4 | W25Q128JVSIQTR | SOIC-8_5.3x5.3mm_P1.27mm | 129.30 | 104.04 | 0 | F |
| U5 | RPI Radio Module 2 | rpi_rmc20452t | 187.46 | 101.44 | -90 | F |
| U6 | APS6404L-3SQR | SOIC-8_3.9x4.9mm_P1.27mm | 128.07 | 98.33 | 0 | F |
| USB1 | TYPE-C_16PIN_2MD_073 | TYPE-C_16PIN_2MD_073 | 113.56 | 101.06 | -90 | F |
| X1 | ABM8-272-T3_C20625731 | ABM8-272-T3_C20625731 | 154.36 | 101.63 | 90 | F |
