#!/usr/bin/env python3

"""
Created on 20 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://raspberrypi.stackexchange.com/questions/450/how-can-i-connect-to-a-usb-serial-device
"""

import sys
import time

from scs_core.data.json import JSONify
from scs_core.gas.ndir_datum import NDIRDatum

from scs_host.sys.host import Host

from scs_ndir.gas.ndir import NDIR


# --------------------------------------------------------------------------------------------------------------------

ndir = NDIR.find(Host.ndir_device())
print(ndir)

datum = ndir.reset()
print(datum)
print("-")

time.sleep(NDIR.RESET_QUARANTINE)


while True:
    temp = ndir.sample_temp()
    v = ndir.sample_dc()
    cnc = ndir.sample_co2(False)
    cnc_igl = ndir.sample_co2(True)

    sample = NDIRDatum(temp, v, cnc.cnc, cnc_igl.cnc)

    print(JSONify.dumps(sample))
    sys.stdout.flush()

    time.sleep(1)
