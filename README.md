# CAN-control

## Overview

This is a series of scripts used for detecting anomalies in CAN bus control messages via Machine Learning algorihms. 

It can be used as an PoC implementation of an IDS which detects threats and attacks in automotive vehicles.

## Supported formats
The collection of scripts currently supports the analysis of logs created with CANoe and saved as ASCII output.

CANoe ASCII log format:
>0.221438 1  201             Rx   d 8 BD 18 BD 18 FF FF FF FF  Length = 229894 BitCount = 119 ID = 513

>0.224030 1  2EB             Rx   d 8 EA F7 12 11 11 51 F1 FF  Length = 221894 BitCount = 115 ID = 747

>0.226454 1  A5              Rx   d 8 81 FA FF F7 7F 00 00 C1  Length = 233894 BitCount = 121 ID = 165

>0.226696 1  D9              Rx   d 8 CD FA 00 10 00 F0 7F C0  Length = 233894 BitCount = 121 ID = 217

## Contact

For more information, please feel free to contact me via e-mail (bachfischer.matthias@googlemail.com) 