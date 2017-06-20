#!/usr/bin/env python3

"""
Created on 20 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_core.data.json import JSONify

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
    sample = ndir.sample()

    print(JSONify.dumps(sample))
    sys.stdout.flush()

    time.sleep(1)
