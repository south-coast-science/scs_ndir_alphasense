"""
Created on 19 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://books.google.co.uk/books?id=RFLtu4fej00C&pg=PA381&lpg=PA381&dq=pic+make32+function&source=bl&ots=ntI5qBRdSe&sig=u9Ay-RgoGCHA4PRebslbGqmvZnE&hl=en&sa=X&ved=0ahUKEwjVg83DwszUAhVGJlAKHUGMArAQ6AEIQjAD#v=onepage&q=pic%20make32%20function&f=false
"""

import serial

from serial.serialutil import SerialException

from scs_core.gas.co2_datum import CO2Datum
from scs_core.gas.ndir_datum import NDIRDatum

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class NDIR(object):
    """
    Alphasense IRC-A1 NDIR CO2 Transmitter board
    """

    RESET_QUARANTINE =          8.0         # time between reset and stable readings

    ADDR_ZERO =                 10          # 16 bit int
    ADDR_SPAN =                 12          # 16 bit int

    ADDR_DEG_C_OFFSET =         14          # 16 bit int
    ADDR_DEG_C_GAIN =           16          # 16 bit int

    ADDR_DC_IN_OFFSET =         18          # 16 bit int
    ADDR_DC_IN_GAIN =           20          # 16 bit int

    ADDR_DAC_OFFSET =           22          # 16 bit int
    ADDR_DAC_GAIN =             24          # 16 bit int

    ADDR_RANGE =                26          # 8 bit int


    # ----------------------------------------------------------------------------------------------------------------

    __BAUD_RATE =               19200

    __SERIAL_TIMEOUT =          2.0
    __LOCK_TIMEOUT =            2.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__name__, NDIR.__LOCK_TIMEOUT)


    @classmethod
    def release_lock(cls):
        Lock.release(cls.__name__)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def find(cls, device):
        try:
            ndir = NDIR(device)
            ndir.__transact('')

            return ndir

        except SerialException:
            return None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device):
        """
        Constructor
        """
        self.__device = device


    # ----------------------------------------------------------------------------------------------------------------
    # reset...

    def reset(self):
        line = self.__transact('\r+++')
        datum = line.strip()

        return datum


    # ----------------------------------------------------------------------------------------------------------------
    # sampling...

    def sample(self):
        temp = self.sample_temp()
        v = self.sample_dc()
        cnc = self.sample_co2(False)
        cnc_igl = self.sample_co2(True)

        return NDIRDatum(temp, v, cnc.cnc, cnc_igl.cnc)


    def sample_co2(self, ideal_gas_law):
        line = self.__transact('G' if ideal_gas_law else 'N')
        cnc = float(line)

        datum = CO2Datum(cnc)

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

    def eeprom_read_int8(self, addr):
        val = int(self.__transact('E%02x' % addr))

        return val


    def eeprom_read_int16(self, addr):
        msb = int(self.__transact('E%02x' % addr))
        lsb = int(self.__transact('E%02x' % (addr + 1)))

        return (msb << 8) | lsb


    def eeprom_read_ieee32(self, addr):
        # TODO: implement eeprom_read_ieee32
        pass


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
