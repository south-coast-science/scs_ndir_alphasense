#!/usr/bin/env python3

"""
Created on 20 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://raspberrypi.stackexchange.com/questions/450/how-can-i-connect-to-a-usb-serial-device
"""

import sys

from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

ndir = NDIR.find(Host.ndir_device())
print(ndir)
print("-")

val = ndir.eeprom_read_int16(NDIR.ADDR_ZERO)
print("        ADDR_ZERO: 0x%04x  %6d" % (val, val))
sys.stdout.flush()
print("-")

val = ndir.eeprom_read_int16(NDIR.ADDR_SPAN)
print("        ADDR_SPAN: 0x%04x  %6d" % (val, val))
sys.stdout.flush()
print("-")

val = ndir.eeprom_read_int16(NDIR.ADDR_DEG_C_OFFSET)
print("ADDR_DEG_C_OFFSET: 0x%04x  %6d" % (val, val))
sys.stdout.flush()

val = ndir.eeprom_read_int16(NDIR.ADDR_DEG_C_GAIN)
print("  ADDR_DEG_C_GAIN: 0x%04x  %6d" % (val, val))
sys.stdout.flush()
print("-")

val = ndir.eeprom_read_int16(NDIR.ADDR_DC_IN_OFFSET)
print("ADDR_DC_IN_OFFSET: 0x%04x  %6d" % (val, val))
sys.stdout.flush()

val = ndir.eeprom_read_int16(NDIR.ADDR_DC_IN_GAIN)
print("  ADDR_DC_IN_GAIN: 0x%04x  %6d" % (val, val))
sys.stdout.flush()
print("-")

val = ndir.eeprom_read_int16(NDIR.ADDR_DAC_OFFSET)
print("  ADDR_DAC_OFFSET: 0x%04x  %6d" % (val, val))
sys.stdout.flush()

val = ndir.eeprom_read_int16(NDIR.ADDR_DAC_GAIN)
print("    ADDR_DAC_GAIN: 0x%04x  %6d" % (val, val))
sys.stdout.flush()
print("-")

val = ndir.eeprom_read_int8(NDIR.ADDR_RANGE)
print("       ADDR_RANGE: 0x%02x    %6d" % (val, val))
sys.stdout.flush()
print("-")
