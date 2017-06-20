#!/usr/bin/env python3

"""
Created on 20 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://raspberrypi.stackexchange.com/questions/450/how-can-i-connect-to-a-usb-serial-device
"""

import time

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

ndir = NDIR('/dev/ttyUSB0')
print(ndir)

datum = ndir.reset()
print(datum)

while True:
    temp = ndir.sample_temp()
    co2 = ndir.sample_co2(True)
    dc = ndir.sample_dc()

    print("%0.1f  %0.1f  %d" % (temp, co2, dc))

    time.sleep(1)