#!/usr/bin/env python3

"""
Created on 20 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

ndir = NDIR.find(Host.ndir_device())
print(ndir)
print("-")

val = ndir.eeprom_read_int8(NDIR.ADDR_TIME_TO_SAMPLE)
print("   TIME_TO_SAMPLE:         0x%02x  %6d" % (val, val))

val = ndir.eeprom_read_int8(NDIR.ADDR_TIME_AFTER_SAMPLE)
print("TIME_AFTER_SAMPLE:         0x%02x  %6d" % (val, val))
print("-")


val = ndir.eeprom_read_ieee32(NDIR.ADDR_COEFF_B)
print("          COEFF_B:           %10.6f" % val)

val = ndir.eeprom_read_ieee32(NDIR.ADDR_COEFF_C)
print("          COEFF_C:           %10.6f" % val)
print("-")


val = ndir.eeprom_read_int16(NDIR.ADDR_ZERO)
print("             ZERO:       0x%04x  %6d" % (val, val))

val = ndir.eeprom_read_int16(NDIR.ADDR_SPAN)
print("             SPAN:       0x%04x  %6d" % (val, val))
print("-")


val = ndir.eeprom_read_int16(NDIR.ADDR_DEG_C_OFFSET)
print("     DEG_C_OFFSET:       0x%04x  %6d" % (val, val))

val = ndir.eeprom_read_int16(NDIR.ADDR_DEG_C_GAIN)
print("       DEG_C_GAIN:       0x%04x  %6d" % (val, val))
print("-")


val = ndir.eeprom_read_int16(NDIR.ADDR_DC_IN_OFFSET)
print("     DC_IN_OFFSET:       0x%04x  %6d" % (val, val))

val = ndir.eeprom_read_int16(NDIR.ADDR_DC_IN_GAIN)
print("       DC_IN_GAIN:       0x%04x  %6d" % (val, val))
print("-")


val = ndir.eeprom_read_int16(NDIR.ADDR_DAC_OFFSET)
print("       DAC_OFFSET:       0x%04x  %6d" % (val, val))

val = ndir.eeprom_read_int16(NDIR.ADDR_DAC_GAIN)
print("         DAC_GAIN:       0x%04x  %6d" % (val, val))
print("-")


val = ndir.eeprom_read_int8(NDIR.ADDR_RANGE)
print("            RANGE:         0x%02x  %6d" % (val, val))
print("-")


val = ndir.eeprom_read_ieee32(NDIR.ADDR_THERM_A)
print("          THERM_A:           %10.6f" % val)

val = ndir.eeprom_read_ieee32(NDIR.ADDR_THERM_B)
print("          THERM_B:           %10.6f" % val)

val = ndir.eeprom_read_ieee32(NDIR.ADDR_THERM_C)
print("          THERM_C:           %10.6f" % val)

val = ndir.eeprom_read_ieee32(NDIR.ADDR_THERM_D)
print("          THERM_D:           %10.6f" % val)
print("-")


val = ndir.eeprom_read_ieee32(NDIR.ADDR_ALPHA)
print("            ALPHA:           %10.6f" % val)

val = ndir.eeprom_read_ieee32(NDIR.ADDR_BETA)
print("             BETA:           %10.6f" % val)

val = ndir.eeprom_read_ieee32(NDIR.ADDR_T_CAL)
print("            T_CAL:           %10.6f" % val)
print("=")


ndir.eeprom_write_int8(NDIR.ADDR_TIME_TO_SAMPLE, 9)
val = ndir.eeprom_read_int8(NDIR.ADDR_TIME_TO_SAMPLE)
print("   TIME_TO_SAMPLE:         0x%02x  %6d" % (val, val))

ndir.eeprom_write_int8(NDIR.ADDR_TIME_TO_SAMPLE, 10)
val = ndir.eeprom_read_int8(NDIR.ADDR_TIME_TO_SAMPLE)
print("   TIME_TO_SAMPLE:         0x%02x  %6d" % (val, val))
print("-")


ndir.eeprom_write_int16(NDIR.ADDR_SPAN, 5647)
val = ndir.eeprom_read_int16(NDIR.ADDR_SPAN)
print("             SPAN:       0x%04x  %6d" % (val, val))

ndir.eeprom_write_int16(NDIR.ADDR_SPAN, 4536)
val = ndir.eeprom_read_int16(NDIR.ADDR_SPAN)
print("             SPAN:       0x%04x  %6d" % (val, val))
print("-")


ndir.eeprom_write_ieee32(NDIR.ADDR_COEFF_C, 2.225941)
val = ndir.eeprom_read_ieee32(NDIR.ADDR_COEFF_C)
print("          COEFF_C:           %10.6f" % val)

ndir.eeprom_write_ieee32(NDIR.ADDR_COEFF_C, 1.114830)
val = ndir.eeprom_read_ieee32(NDIR.ADDR_COEFF_C)
print("          COEFF_C:           %10.6f" % val)
print("-")

