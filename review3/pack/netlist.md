# pico-stretch2 netlist digest

Generated from `kicad-cli sch export netlist --format kicadxml`. 67 components, 93 nets.

Sections: 1. Bill by sheet  2. Multi-pin parts (pin -> net)  3. Two-pin parts (net -- net)  4. Power and ground nets  5. Signal nets  6. Single-node nets

## 1. Bill by sheet

### Sheet `/` (67 parts)

| Refs | Value | Footprint | LCSC | MPN |
|---|---|---|---|---|
| Boot1, Reset1 | K2-1808SN-A4SW | K2-1808SN-A4SW | C92589 | K2-1808SN-A4SW-01 |
| C1, C2, C3, C4 ... C36 (12) | 100nF | C_0402_1005Metric | C1525 | CL05B104KO5NNNC |
| C5, C10, C11, C12 | 4.7uF | C_0402_1005Metric | C23733 | CL05A475MP5NRNC |
| C17, C18 | 15pF | C_0402_1005Metric | C1548 | 0402CG150J500NT |
| C19 | 4.7uF | C_0402_1005Metric | C23733 |  |
| C21, C22, C23 | 100nF | C_0402_1005Metric | C1525 |  |
| C24 | CL10A475KO8NNNC | C_0603_1608Metric | C19666 | CL10A475KO8NNNC |
| C37, C40 | 10uF | C_0603_1608Metric | C19702 |  |
| C38, C39 | CL05B104KO5NNNC | C_0402_1005Metric | C1525 | CL05B104KO5NNNC |
| D1 | DFLS130L-7 | D_PowerDI-123 | C110493 | DFLS130L-7 |
| D2, D3 | RCLAMP0521P_TCT_C3029033 | RCLAMP0521P_TCT_C3029033 | C3029033 | RCLAMP0521P.TCT-MS |
| J2 | Conn_01x03_Pin | PinHeader_1x03_P2.54mm_Vertical |  |  |
| J4 | Conn_01x64_Castellated_Pads | Castellated_Pad_64 |  |  |
| JP1, JP2, JP3, JP4 | SolderJumper_2_Open | SolderJumper-2_P1.3mm_Open_Pad1.0x1.5mm |  |  |
| L1 | AOTA-B201610S3R3-101-T | AOTA-B201610S3R3-101-T | C42411119 | AOTA-B201610S3R3-101-T |
| PWR_LED1 | KT-0603R | KT-0603R | C2286 | KT-0603R |
| R1, R4 | 5.1kΩ | R_0402_1005Metric | C25905 |  |
| R2, R3 | 33Ω | R_0402_1005Metric | C25105 |  |
| R5, R14 | 1kΩ | R_0402_1005Metric | C11702 |  |
| R6 | 33Ω | R_0402_1005Metric | C25105 | 0402WGF330JTCE |
| R7 | 1Ω | R_0402_1005Metric | C25086 | 0402WGF100KTCE |
| R8 | 200Ω | R_0402_1005Metric | C25087 | 0402WGF2000TCE |
| R9, R10, R16 | 10kΩ | R_0402_1005Metric | C25744 |  |
| R11 | 100kΩ | R_0402_1005Metric | C25741 |  |
| R12 | 2kΩ | R_0402_1005Metric | C4109 |  |
| R15 | 470Ω | R_0402_1005Metric | C25117 |  |
| R28 | 1kΩ | R_0402_1005Metric | C11702 | 0402WGF1001TCE |
| TP1, TP2, TP3, TP4 | TestPoint | TestPoint_Pad_1.0x1.0mm |  |  |
| U1 | RP2350B_C42415655 | RP2350B_C42415655 | C42415655 | RP2350B |
| U3 | ME6217C33M5G | SOT-23-5 | C427602 | ME6217C33M5G |
| U4 | W25Q128JVSIQTR | SOIC-8_5.3x5.3mm_P1.27mm | C97521 | W25Q128JVSIQ |
| U5 (DNP) | RPI Radio Module 2 | rpi_rmc20452t |  |  |
| U6 (DNP) | APS6404L-3SQR | SOIC-8_3.9x4.9mm_P1.27mm | C5333729 |  |
| USB1 | TYPE-C_16PIN_2MD_073 | TYPE-C_16PIN_2MD_073 | C2765186 | TYPE-C 16PIN 2MD(073) |
| X1 | ABM8-272-T3_C20625731 | ABM8-272-T3_C20625731 | C20625731 | ABM8-272-T3 |

## 2. Multi-pin parts (pin -> net)

### Boot1  K2-1808SN-A4SW  (K2-1808SN-A4SW, C92589, /)
```
    1 1_1                unspecified    Net-(Boot1-Pad1)
    2 2_2                unspecified    Net-(Boot1-Pad1)
    3 3_3                unspecified    GND
    4 4_4                unspecified    GND
```
### J2  Conn_01x03_Pin  (PinHeader_1x03_P2.54mm_Vertical, , /)
```
    1 Pin_1_1            passive        SWCLK
    2 Pin_2_2            passive        GND
    3 Pin_3_3            passive        SWDIO
```
### J4  Conn_01x64_Castellated_Pads  (Castellated_Pad_64, , /)
```
    1 Pin_1_1            passive        GPIO0
    2 Pin_2_2            passive        GPIO1
    3 Pin_3_3            passive        GND
    4 Pin_4_4            passive        GPIO2
    5 Pin_5_5            passive        GPIO3
    6 Pin_6_6            passive        GPIO4
    7 Pin_7_7            passive        GPIO5
    8 Pin_8_8            passive        GND
    9 Pin_9_9            passive        GPIO6
   10 Pin_10_10          passive        GPIO7
   11 Pin_11_11          passive        GPIO8
   12 Pin_12_12          passive        GPIO9
   13 Pin_13_13          passive        GND
   14 Pin_14_14          passive        GPIO10
   15 Pin_15_15          passive        GPIO11
   16 Pin_16_16          passive        GPIO12
   17 Pin_17_17          passive        GPIO13
   18 Pin_18_18          passive        GND
   19 Pin_19_19          passive        GPIO14
   20 Pin_20_20          passive        GPIO15
   21 Pin_21_21          passive        GPIO23
   22 Pin_22_22          passive        GPIO24
   23 Pin_23_23          passive        GPIO25
   24 Pin_24_24          passive        GPIO29
   25 Pin_25_25          passive        GPIO30
   26 Pin_26_26          passive        GPIO31
   27 Pin_27_27          passive        GPIO32
   28 Pin_28_28          passive        GPIO33
   29 Pin_29_29          passive        GPIO34
   30 Pin_30_30          passive        GPIO35
   31 Pin_31_31          passive        GND
   32 Pin_32_32          passive        GPIO36
   33 Pin_33_33          passive        GPIO37
   34 Pin_34_34          passive        GND
   35 Pin_35_35          passive        GPIO38
   36 Pin_36_36          passive        GPIO39
   37 Pin_37_37          passive        GPIO40/ADC0
   38 Pin_38_38          passive        GPIO41/ADC1
   39 Pin_39_39          passive        GPIO42/ADC2
   40 Pin_40_40          passive        GPIO43/ADC3
   41 Pin_41_41          passive        GPIO44/ADC4
   42 Pin_42_42          passive        GPIO45/ADC5
   43 Pin_43_43          passive        GPIO46/ADC6
   44 Pin_44_44          passive        GPIO47/ADC7
   45 Pin_45_45          passive        GPIO16
   46 Pin_46_46          passive        GPIO17
   47 Pin_47_47          passive        GND
   48 Pin_48_48          passive        GPIO18
   49 Pin_49_49          passive        GPIO19
   50 Pin_50_50          passive        GPIO20
   51 Pin_61_51          passive        GPIO21
   52 Pin_52_52          passive        GND
   53 Pin_53_53          passive        GPIO22
   54 Pin_54_54          passive        RUN
   55 Pin_55_55          passive        GPIO26
   56 Pin_56_56          passive        GPIO27
   57 Pin_57_57          passive        GND
   58 Pin_58_58          passive        GPIO28
   59 Pin_59_59          passive        ADC_VREF
   60 Pin_60_60          passive        3V3
   61 Pin_61_61          passive        3V3_EN
   62 Pin_62_62          passive        GND
   63 Pin_63_63          passive        VSYS
   64 Pin_64_64          passive        VBUS
```
### Reset1  K2-1808SN-A4SW  (K2-1808SN-A4SW, C92589, /)
```
    1 1_1                unspecified+no unconnected-(Reset1-Pad1)
    2 2_2                unspecified    RUN
    3 3_3                unspecified    GND
    4 4_4                unspecified    GND
```
### U1  RP2350B_C42415655  (RP2350B_C42415655, C42415655, /)
```
    1 GPIO4_1            unspecified    GPIO4
    2 GPIO5_2            unspecified    GPIO5
    3 GPIO6_3            unspecified    GPIO6
    4 GPIO7_4            unspecified    GPIO7
    5 IOVDD_5            unspecified    3V3
    6 GPIO8_6            unspecified    GPIO8
    7 GPIO9_7            unspecified    GPIO9
    8 GPIO10_8           unspecified    GPIO10
    9 GPIO11_9           unspecified    GPIO11
   10 DVDD_10            unspecified    1V1
   11 GPIO12_11          unspecified    GPIO12
   12 GPIO13_12          unspecified    GPIO13
   13 GPIO14_13          unspecified    GPIO14
   14 GPIO15_14          unspecified    GPIO15
   15 IOVDD_15           unspecified    3V3
   16 GPIO16_16          unspecified    GPIO16
   17 GPIO17_17          unspecified    GPIO17
   18 GPIO18_18          unspecified    GPIO18
   19 GPIO19_19          unspecified    GPIO19
   20 GPIO20_20          unspecified    GPIO20
   21 GPIO21_21          unspecified    GPIO21
   22 GPIO22_22          unspecified    GPIO22
   23 GPIO23_23          unspecified    GPIO23
   24 IOVDD_24           unspecified    3V3
   25 GPIO24_25          unspecified    GPIO24
   26 GPIO25_26          unspecified    GPIO25
   27 GPIO26_27          unspecified    GPIO26
   28 GPIO27_28          unspecified    GPIO27
   29 IOVDD_29           unspecified    3V3
   30 XIN_30             unspecified    Net-(U1-XIN)
   31 XOUT_31            unspecified    Net-(U1-XOUT)
   32 DVDD_32            unspecified    1V1
   33 SWCLK_33           unspecified    SWCLK
   34 SWDIO_34           unspecified    SWDIO
   35 RUN_35             unspecified    RUN
   36 GPIO28_36          unspecified    GPIO28
   37 GPIO29_37          unspecified    GPIO29
   38 GPIO30_38          unspecified    GPIO30
   39 GPIO31_39          unspecified    GPIO31
   40 GPIO32_40          unspecified    GPIO32
   41 IOVDD_41           unspecified    3V3
   42 GPIO33_42          unspecified    GPIO33
   43 GPIO34_43          unspecified    GPIO34
   44 GPIO35_44          unspecified    GPIO35
   45 GPIO36_45          unspecified    GPIO36
   46 GPIO37_46          unspecified    GPIO37
   47 GPIO38_47          unspecified    GPIO38
   48 GPIO39_48          unspecified    GPIO39
   49 GPIO40_ADC0_49     unspecified    GPIO40/ADC0
   50 IOVDD_50           unspecified    3V3
   51 DVDD_51            unspecified    1V1
   52 GPIO41_ADC1_52     unspecified    GPIO41/ADC1
   53 GPIO42_ADC2_53     unspecified    GPIO42/ADC2
   54 GPIO43_ADC3_54     unspecified    GPIO43/ADC3
   55 GPIO44_ADC4_55     unspecified    GPIO44/ADC4
   56 GPIO45_ADC5_56     unspecified    GPIO45/ADC5
   57 GPIO46_ADC6_57     unspecified    GPIO46/ADC6
   58 GPIO47_ADC7_58     unspecified    GPIO47/ADC7
   59 ADC_AVDD_59        unspecified    Net-(U1-ADC_AVDD)
   60 IOVDD_60           unspecified    3V3
   61 VREG_AVDD_61       unspecified    Net-(U1-VREG_AVDD)
   62 VREG_PGND_62       unspecified    GND
   63 VREG_LX_63         unspecified    /VREG_LX
   64 VREG_VIN_64        unspecified    3V3
   65 VREG_FB_65         unspecified    1V1
   66 USB_D-_66          unspecified    USB_D-
   67 USB_D+_67          unspecified    USB_D+
   68 USB_OTP_VDD_68     unspecified    3V3
   69 QSPI_IOVDD_69      unspecified    3V3
   70 QSPI_SD3_70        unspecified    QSPI_SD3
   71 QSPI_SCLK_71       unspecified    QSPI_SCLK
   72 QSPI_SD0_72        unspecified    QSPI_SD0
   73 QSPI_SD2_73        unspecified    QSPI_SD2
   74 QSPI_SD1_74        unspecified    QSPI_SD1
   75 QSPI_SS_75         unspecified    Net-(U1-QSPI_SS)
   76 IOVDD_76           unspecified    3V3
   77 GPIO0_77           unspecified    GPIO0
   78 GPIO1_78           unspecified    GPIO1
   79 GPIO2_79           unspecified    GPIO2
   80 GPIO3_80           unspecified    GPIO3
   81 GND_81             unspecified    GND
```
### U3  ME6217C33M5G  (SOT-23-5, C427602, /)
```
    1 VIN_1              unspecified    VSYS
    2 VSS_2              unspecified    GND
    3 CE_3               unspecified    3V3_EN
    4 NC_4               unspecified+no unconnected-(U3-NC-Pad4)
    5 VOUT_5             unspecified    3V3
```
### U4  W25Q128JVSIQTR  (SOIC-8_5.3x5.3mm_P1.27mm, C97521, /)
```
    1 CS#_1              unspecified    Net-(U1-QSPI_SS)
    2 DO_2               unspecified    QSPI_SD1
    3 IO2_3              unspecified    QSPI_SD2
    4 GND_4              unspecified    GND
    5 DI_5               unspecified    QSPI_SD0
    6 CLK_6              unspecified    QSPI_SCLK
    7 IO3_7              unspecified    QSPI_SD3
    8 VCC_8              unspecified    3V3
```
### U5  RPI Radio Module 2  (rpi_rmc20452t, , /)
```
    1 GND_1              power_in       GND
    2 NC_2               no_connect     unconnected-(U5-NC-Pad2)
    3 SCLK_3             input          GPIO29
    4 GND_4              power_in       GND
    5 DI_5               input          GPIO24
    6 DO_6               output         Net-(U5-DO)
    7 GND_7              power_in       GND
    8 GPIO0_8            no_connect     unconnected-(U5-GPIO0-Pad8)
    9 CS_9               input          Net-(JP2-A)
   10 nIRQ_10            output         Net-(U5-nIRQ)
   11 GND_11             power_in       GND
   12 WL_ON_12           input          Net-(JP3-B)
   13 BT_ON_13           input          Net-(JP3-B)
   14 VDDIO_14           power_in       3V3
   15 GND_15             power_in       GND
   16 VIN_16             power_in       3V3
   17 GPIO2_17           no_connect     unconnected-(U5-GPIO2-Pad17)
   18 GPIO1_18           no_connect     unconnected-(U5-GPIO1-Pad18)
   19 NC_19              no_connect     unconnected-(U5-NC-Pad19)
   20 NC_20              no_connect     unconnected-(U5-NC-Pad20)
   21 GND_21             power_in       GND
```
### U6  APS6404L-3SQR  (SOIC-8_3.9x4.9mm_P1.27mm, C5333729, /)
```
    1 ~{CE}_1            input          Net-(JP1-A)
    2 SO/SIO_2           output         QSPI_SD1
    3 SIO2_3             bidirectional  QSPI_SD2
    4 GND_4              power_in       GND
    5 SI/SIO_5           input          QSPI_SD0
    6 SCLK_6             output         QSPI_SCLK
    7 SIO3_7             bidirectional  QSPI_SD3
    8 VCC_8              power_in       3V3
```
### USB1  TYPE-C_16PIN_2MD_073  (TYPE-C_16PIN_2MD_073, C2765186, /)
```
    1 GND_1              unspecified    GND
    2 VBUS_2             unspecified    VBUS
    3 SBU2_3             unspecified+no unconnected-(USB1-SBU2-Pad3)
    4 CC1_4              unspecified    Net-(USB1-CC1)
    5 DN2_5              unspecified    USB2_D-
    6 DP1_6              unspecified    USB2_D+
    7 DN1_7              unspecified    USB2_D-
    8 DP2_8              unspecified    USB2_D+
    9 SBU1_9             unspecified+no unconnected-(USB1-SBU1-Pad9)
   10 CC2_10             unspecified    Net-(USB1-CC2)
   11 VBUS_11            unspecified    VBUS
   12 GND_12             unspecified    GND
   13 SHELL_13           unspecified    GND
   14 SHELL_14           unspecified    GND
```
### X1  ABM8-272-T3_C20625731  (ABM8-272-T3_C20625731, C20625731, /)
```
    1 1_1                input          Net-(U1-XIN)
    2 GND_2              input          GND
    3 3_3                input          Net-(C17-Pad1)
    4 GND_4              input          GND
```

## 3. Two-pin parts (pin1 net -- pin2 net)

```
C1     100nF            C_0402_1005Metric            1:3V3 -- 2:GND
C2     100nF            C_0402_1005Metric            1:1V1 -- 2:GND
C3     100nF            C_0402_1005Metric            1:3V3 -- 2:GND
C4     100nF            C_0402_1005Metric            1:3V3 -- 2:GND
C5     4.7uF            C_0402_1005Metric            1:1V1 -- 2:GND
C6     100nF            C_0402_1005Metric            1:3V3 -- 2:GND
C7     100nF            C_0402_1005Metric            1:3V3 -- 2:GND
C8     100nF            C_0402_1005Metric            1:GND -- 2:3V3
C9     100nF            C_0402_1005Metric            1:GND -- 2:3V3
C10    4.7uF            C_0402_1005Metric            1:1V1 -- 2:GND
C11    4.7uF            C_0402_1005Metric            1:Net-(U1-VREG_AVDD) -- 2:GND
C12    4.7uF            C_0402_1005Metric            1:3V3 -- 2:GND
C13    100nF            C_0402_1005Metric            1:GND -- 2:1V1
C15    100nF            C_0402_1005Metric            1:GND -- 2:RUN
C16    100nF            C_0402_1005Metric            1:3V3 -- 2:GND
C17    15pF             C_0402_1005Metric            1:Net-(C17-Pad1) -- 2:GND
C18    15pF             C_0402_1005Metric            1:GND -- 2:Net-(U1-XIN)
C19    4.7uF            C_0402_1005Metric            1:Net-(U1-ADC_AVDD) -- 2:GND
C21    100nF            C_0402_1005Metric            1:3V3 -- 2:GND
C22    100nF            C_0402_1005Metric            1:3V3 -- 2:GND
C23    100nF            C_0402_1005Metric            1:3V3 -- 2:GND
C24    CL10A475KO8NNNC  C_0603_1608Metric            1:GND -- 2:3V3
C36    100nF            C_0402_1005Metric            1:GND -- 2:3V3
C37    10uF             C_0603_1608Metric            1:VSYS -- 2:GND
C38    CL05B104KO5NNNC  C_0402_1005Metric            1:3V3 -- 2:GND
C39    CL05B104KO5NNNC  C_0402_1005Metric            1:VSYS -- 2:GND
C40    10uF             C_0603_1608Metric            1:GND -- 2:3V3
D1     DFLS130L-7       D_PowerDI-123                1:VSYS -- 2:VBUS
D2     RCLAMP0521P_TCT_ RCLAMP0521P_TCT_C3029033     1:GND -- 2:USB2_D-
D3     RCLAMP0521P_TCT_ RCLAMP0521P_TCT_C3029033     1:GND -- 2:USB2_D+
JP1    SolderJumper_2_O SolderJumper-2_P1.3mm_Open_P 1:Net-(JP1-A) -- 2:GPIO0
JP2    SolderJumper_2_O SolderJumper-2_P1.3mm_Open_P 1:Net-(JP2-A) -- 2:GPIO25
JP3    SolderJumper_2_O SolderJumper-2_P1.3mm_Open_P 1:GPIO23 -- 2:Net-(JP3-B)
JP4    SolderJumper_2_O SolderJumper-2_P1.3mm_Open_P 1:Net-(JP1-A) -- 2:GPIO47/ADC7
L1     AOTA-B201610S3R3 AOTA-B201610S3R3-101-T       1:/VREG_LX -- 2:1V1
PWR_LED1 KT-0603R         KT-0603R                     1:Net-(PWR_LED1-K) -- 2:3V3
R1     5.1kΩ            R_0402_1005Metric            1:GND -- 2:Net-(USB1-CC1)
R2     33Ω              R_0402_1005Metric            1:USB_D- -- 2:USB2_D-
R3     33Ω              R_0402_1005Metric            1:USB_D+ -- 2:USB2_D+
R4     5.1kΩ            R_0402_1005Metric            1:GND -- 2:Net-(USB1-CC2)
R5     1kΩ              R_0402_1005Metric            1:Net-(Boot1-Pad1) -- 2:Net-(U1-QSPI_SS)
R6     33Ω              R_0402_1005Metric            1:3V3 -- 2:Net-(U1-VREG_AVDD)
R7     1Ω               R_0402_1005Metric            1:Net-(U1-ADC_AVDD) -- 2:ADC_VREF
R8     200Ω             R_0402_1005Metric            1:ADC_VREF -- 2:3V3
R9     10kΩ             R_0402_1005Metric            1:Net-(JP2-A) -- 2:GND
R10    10kΩ             R_0402_1005Metric            1:Net-(JP3-B) -- 2:GND
R11    100kΩ            R_0402_1005Metric            1:VSYS -- 2:3V3_EN
R12    2kΩ              R_0402_1005Metric            1:Net-(PWR_LED1-K) -- 2:GND
R14    1kΩ              R_0402_1005Metric            1:Net-(JP1-A) -- 2:3V3
R15    470Ω             R_0402_1005Metric            1:Net-(U5-DO) -- 2:GPIO24
R16    10kΩ             R_0402_1005Metric            1:GPIO24 -- 2:Net-(U5-nIRQ)
R28    1kΩ              R_0402_1005Metric            1:Net-(C17-Pad1) -- 2:Net-(U1-XOUT)
TP1    TestPoint        TestPoint_Pad_1.0x1.0mm      1:1V1
TP2    TestPoint        TestPoint_Pad_1.0x1.0mm      1:3V3
TP3    TestPoint        TestPoint_Pad_1.0x1.0mm      1:USB2_D-
TP4    TestPoint        TestPoint_Pad_1.0x1.0mm      1:USB2_D+
```

## 4. Power and ground nets

```
3V3  [38 nodes]  C x16, J x1, PWR x1, R x3, TP x1, U x16
    IC pins: PWR_LED1.2(A_2), U1.15(IOVDD_15), U1.24(IOVDD_24), U1.29(IOVDD_29), U1.41(IOVDD_41), U1.5(IOVDD_5), U1.50(IOVDD_50), U1.60(IOVDD_60), U1.64(VREG_VIN_64), U1.68(USB_OTP_VDD_68), U1.69(QSPI_IOVDD_69), U1.76(IOVDD_76), U3.5(VOUT_5), U4.8(VCC_8), U5.14(VDDIO_14), U5.16(VIN_16), U6.8(VCC_8)
3V3_EN  [3]  J4.61(Pin_61_61), R11.2, U3.3(CE_3)
GND  [66 nodes]  B x2, C x27, D x2, J x11, R x7, U x11, USB x4, X x2
    IC pins: Boot1.3(3_3), Boot1.4(4_4), Reset1.3(3_3), Reset1.4(4_4), U1.62(VREG_PGND_62), U1.81(GND_81), U3.2(VSS_2), U4.4(GND_4), U5.1(GND_1), U5.11(GND_11), U5.15(GND_15), U5.21(GND_21), U5.4(GND_4), U5.7(GND_7), U6.4(GND_4), USB1.1(GND_1), USB1.12(GND_12), USB1.13(SHELL_13), USB1.14(SHELL_14), X1.2(GND_2), X1.4(GND_4)
Net-(U1-ADC_AVDD)  [3]  C19.1, R7.1, U1.59(ADC_AVDD_59)
Net-(U1-VREG_AVDD)  [3]  C11.1(1_1), R6.2(2_2), U1.61(VREG_AVDD_61)
VBUS  [4]  D1.2(2_2), J4.64(Pin_64_64), USB1.11(VBUS_11), USB1.2(VBUS_2)
VSYS  [6]  C37.1, C39.1(1_1), D1.1(1_1), J4.63(Pin_63_63), R11.1, U3.1(VIN_1)
```

## 5. Signal nets

```
1V1  [10]  C2.1(1_1), C5.1(1_1), C10.1(1_1), C13.2(2_2), L1.2(2_2), TP1.1(1_1), U1.10(DVDD_10), U1.32(DVDD_32), U1.51(DVDD_51), U1.65(VREG_FB_65)
/VREG_LX  [2]  L1.1(1_1), U1.63(VREG_LX_63)
ADC_VREF  [3]  J4.59(Pin_59_59), R7.2, R8.1
GPIO0  [3]  J4.1(Pin_1_1), JP1.2(B_2), U1.77(GPIO0_77)
GPIO1  [2]  J4.2(Pin_2_2), U1.78(GPIO1_78)
GPIO2  [2]  J4.4(Pin_4_4), U1.79(GPIO2_79)
GPIO3  [2]  J4.5(Pin_5_5), U1.80(GPIO3_80)
GPIO4  [2]  J4.6(Pin_6_6), U1.1(GPIO4_1)
GPIO5  [2]  J4.7(Pin_7_7), U1.2(GPIO5_2)
GPIO6  [2]  J4.9(Pin_9_9), U1.3(GPIO6_3)
GPIO7  [2]  J4.10(Pin_10_10), U1.4(GPIO7_4)
GPIO8  [2]  J4.11(Pin_11_11), U1.6(GPIO8_6)
GPIO9  [2]  J4.12(Pin_12_12), U1.7(GPIO9_7)
GPIO10  [2]  J4.14(Pin_14_14), U1.8(GPIO10_8)
GPIO11  [2]  J4.15(Pin_15_15), U1.9(GPIO11_9)
GPIO12  [2]  J4.16(Pin_16_16), U1.11(GPIO12_11)
GPIO13  [2]  J4.17(Pin_17_17), U1.12(GPIO13_12)
GPIO14  [2]  J4.19(Pin_19_19), U1.13(GPIO14_13)
GPIO15  [2]  J4.20(Pin_20_20), U1.14(GPIO15_14)
GPIO16  [2]  J4.45(Pin_45_45), U1.16(GPIO16_16)
GPIO17  [2]  J4.46(Pin_46_46), U1.17(GPIO17_17)
GPIO18  [2]  J4.48(Pin_48_48), U1.18(GPIO18_18)
GPIO19  [2]  J4.49(Pin_49_49), U1.19(GPIO19_19)
GPIO20  [2]  J4.50(Pin_50_50), U1.20(GPIO20_20)
GPIO21  [2]  J4.51(Pin_61_51), U1.21(GPIO21_21)
GPIO22  [2]  J4.53(Pin_53_53), U1.22(GPIO22_22)
GPIO23  [3]  J4.21(Pin_21_21), JP3.1(A_1), U1.23(GPIO23_23)
GPIO24  [5]  J4.22(Pin_22_22), R15.2, R16.1, U1.25(GPIO24_25), U5.5(DI_5)
GPIO25  [3]  J4.23(Pin_23_23), JP2.2(B_2), U1.26(GPIO25_26)
GPIO26  [2]  J4.55(Pin_55_55), U1.27(GPIO26_27)
GPIO27  [2]  J4.56(Pin_56_56), U1.28(GPIO27_28)
GPIO28  [2]  J4.58(Pin_58_58), U1.36(GPIO28_36)
GPIO29  [3]  J4.24(Pin_24_24), U1.37(GPIO29_37), U5.3(SCLK_3)
GPIO30  [2]  J4.25(Pin_25_25), U1.38(GPIO30_38)
GPIO31  [2]  J4.26(Pin_26_26), U1.39(GPIO31_39)
GPIO32  [2]  J4.27(Pin_27_27), U1.40(GPIO32_40)
GPIO33  [2]  J4.28(Pin_28_28), U1.42(GPIO33_42)
GPIO34  [2]  J4.29(Pin_29_29), U1.43(GPIO34_43)
GPIO35  [2]  J4.30(Pin_30_30), U1.44(GPIO35_44)
GPIO36  [2]  J4.32(Pin_32_32), U1.45(GPIO36_45)
GPIO37  [2]  J4.33(Pin_33_33), U1.46(GPIO37_46)
GPIO38  [2]  J4.35(Pin_35_35), U1.47(GPIO38_47)
GPIO39  [2]  J4.36(Pin_36_36), U1.48(GPIO39_48)
GPIO40/ADC0  [2]  J4.37(Pin_37_37), U1.49(GPIO40_ADC0_49)
GPIO41/ADC1  [2]  J4.38(Pin_38_38), U1.52(GPIO41_ADC1_52)
GPIO42/ADC2  [2]  J4.39(Pin_39_39), U1.53(GPIO42_ADC2_53)
GPIO43/ADC3  [2]  J4.40(Pin_40_40), U1.54(GPIO43_ADC3_54)
GPIO44/ADC4  [2]  J4.41(Pin_41_41), U1.55(GPIO44_ADC4_55)
GPIO45/ADC5  [2]  J4.42(Pin_42_42), U1.56(GPIO45_ADC5_56)
GPIO46/ADC6  [2]  J4.43(Pin_43_43), U1.57(GPIO46_ADC6_57)
GPIO47/ADC7  [3]  J4.44(Pin_44_44), JP4.2(B_2), U1.58(GPIO47_ADC7_58)
Net-(Boot1-Pad1)  [3]  Boot1.1(1_1), Boot1.2(2_2), R5.1
Net-(C17-Pad1)  [3]  C17.1(1_1), R28.1, X1.3(3_3)
Net-(JP1-A)  [4]  JP1.1(A_1), JP4.1(A_1), R14.1, U6.1(~{CE}_1)
Net-(JP2-A)  [3]  JP2.1(A_1), R9.1, U5.9(CS_9)
Net-(JP3-B)  [4]  JP3.2(B_2), R10.1, U5.12(WL_ON_12), U5.13(BT_ON_13)
Net-(PWR_LED1-K)  [2]  PWR_LED1.1(K_1), R12.1
Net-(U1-QSPI_SS)  [3]  R5.2, U1.75(QSPI_SS_75), U4.1(CS#_1)
Net-(U1-XIN)  [3]  C18.2(2_2), U1.30(XIN_30), X1.1(1_1)
Net-(U1-XOUT)  [2]  R28.2, U1.31(XOUT_31)
Net-(U5-DO)  [2]  R15.1, U5.6(DO_6)
Net-(U5-nIRQ)  [2]  R16.2, U5.10(nIRQ_10)
Net-(USB1-CC1)  [2]  R1.2, USB1.4(CC1_4)
Net-(USB1-CC2)  [2]  R4.2, USB1.10(CC2_10)
QSPI_SCLK  [3]  U1.71(QSPI_SCLK_71), U4.6(CLK_6), U6.6(SCLK_6)
QSPI_SD0  [3]  U1.72(QSPI_SD0_72), U4.5(DI_5), U6.5(SI/SIO_5)
QSPI_SD1  [3]  U1.74(QSPI_SD1_74), U4.2(DO_2), U6.2(SO/SIO_2)
QSPI_SD2  [3]  U1.73(QSPI_SD2_73), U4.3(IO2_3), U6.3(SIO2_3)
QSPI_SD3  [3]  U1.70(QSPI_SD3_70), U4.7(IO3_7), U6.7(SIO3_7)
RUN  [4]  C15.2(2_2), J4.54(Pin_54_54), Reset1.2(2_2), U1.35(RUN_35)
SWCLK  [2]  J2.1(Pin_1_1), U1.33(SWCLK_33)
SWDIO  [2]  J2.3(Pin_3_3), U1.34(SWDIO_34)
USB2_D+  [5]  D3.2, R3.2, TP4.1(1_1), USB1.6(DP1_6), USB1.8(DP2_8)
USB2_D-  [5]  D2.2, R2.2, TP3.1(1_1), USB1.5(DN2_5), USB1.7(DN1_7)
USB_D+  [2]  R3.1, U1.67(USB_D+_67)
USB_D-  [2]  R2.1, U1.66(USB_D-_66)
```

## 6. Single-node / unconnected nets

```
unconnected-(Reset1-Pad1)  [1]  Reset1.1(1_1)
unconnected-(U3-NC-Pad4)  [1]  U3.4(NC_4)
unconnected-(U5-GPIO0-Pad8)  [1]  U5.8(GPIO0_8)
unconnected-(U5-GPIO1-Pad18)  [1]  U5.18(GPIO1_18)
unconnected-(U5-GPIO2-Pad17)  [1]  U5.17(GPIO2_17)
unconnected-(U5-NC-Pad2)  [1]  U5.2(NC_2)
unconnected-(U5-NC-Pad19)  [1]  U5.19(NC_19)
unconnected-(U5-NC-Pad20)  [1]  U5.20(NC_20)
unconnected-(USB1-SBU1-Pad9)  [1]  USB1.9(SBU1_9)
unconnected-(USB1-SBU2-Pad3)  [1]  USB1.3(SBU2_3)
```

## 7. Pin audits (confirm each against the datasheet)

### Power/ground pins on an unconnected or single-node net

- none

### Enable / select / reset pins tied to a rail

- U3.3 CE (no bar in the symbol - check the datasheet polarity) tied to 3V3_EN

### Data direction (DI/DO, TX/RX, MOSI/MISO, numbered data lines)

- none flagged - still trace every serial/memory/UART line driver to receiver against both datasheets

### Control lines between ICs with no pull (reset-state decision needed)

- Net-(U1-QSPI_SS) joins U1.75 QSPI_SS, U4.1 CS#: no pull resistor to a rail - write its level on each side at power-up, with either chip in reset, unprogrammed and unpowered (both datasheets' pin default states), or add a pull to the safe level

### BOM parts with no datasheet link

- 6 of 61: J2, J4, TP1, TP2, TP3, TP4 - the link exists upstream (LCSC number, imported symbol); find the stage that dropped it (kicad-pcb-workflow partfields.py) and read each part's datasheet

### LED series resistor power

- none found (set "rail_voltages" in review_config.json for rails whose name has no voltage)
