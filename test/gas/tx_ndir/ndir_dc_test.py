#!/usr/bin/env python3

"""
Created on 15 Mar 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.sys.host import Host

from scs_ndir.gas.tx_ndir.tx_ndir import TxNDIR


# --------------------------------------------------------------------------------------------------------------------

ndir = TxNDIR(Host.ndir_usb_device())
print(ndir)

datum = ndir.reset()
print(datum)
print("-")

time.sleep(TxNDIR.RESET_QUARANTINE)

dc = ndir.sample_dc()
print("dc: %s" % dc)
