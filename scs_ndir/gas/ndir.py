"""
Created on 19 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import serial

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class NDIR(object):
    """
    Alphasense IRC-A1 NDIR CO2 Transmitter board
    """

    RESET_QUARANTINE =          8.0         # time between reset and stable readings


    # ----------------------------------------------------------------------------------------------------------------

    __BAUD_RATE =               19200
    __SERIAL_TIMEOUT =          2.0
    __LOCK_TIMEOUT =            1.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__name__, NDIR.__LOCK_TIMEOUT)


    @classmethod
    def release_lock(cls):
        Lock.release(cls.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device):
        """
        Constructor
        """
        self.__device = device


    # ----------------------------------------------------------------------------------------------------------------
    # sampling...

    def reset(self):
        line = self.__transact('\r+++')
        datum = line.strip()

        return datum


    def sample_co2(self, corrected):
        line = self.__transact('G' if corrected else 'N')
        datum = float(line)

        return datum


    def sample_temp(self):
        line = self.__transact('T')
        datum = float(line)

        return datum


    def sample_dc(self):
        line = self.__transact('V')
        datum = int(line)

        return datum


    # ----------------------------------------------------------------------------------------------------------------
    # EEPROM...

    # TODO: implement specific EEPROM parameters


    # ----------------------------------------------------------------------------------------------------------------

    def __transact(self, command):
        NDIR.obtain_lock()

        ser = None

        try:
            ser = serial.Serial(self.__device, NDIR.__BAUD_RATE, timeout=NDIR.__SERIAL_TIMEOUT)

            message = command + '\r'
            ser.write(message.encode())
            line = ser.readline()

            return line.decode()

        finally:
            if ser:
                ser.close()

            NDIR.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "NDIR:{device:%s}" % self.__device
