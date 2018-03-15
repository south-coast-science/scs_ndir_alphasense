"""
Created on 19 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Alphasense IRC-A1 NDIR CO2 Transmitter
810-0001-07 Rev. 2
"""

import serial
import struct
import time

from scs_core.gas.ndir import NDIR
from scs_core.gas.ndir_datum import NDIRDatum
from scs_core.gas.ndir_version import NDIRVersion, NDIRTag

from scs_host.lock.lock import Lock


# --------------------------------------------------------------------------------------------------------------------

class TxNDIR(NDIR):
    """
    """

    ID =                        'Alphasense IRC-A1 NDIR CO2 Transmitter'

    TAG_DEVICE =                810
    TAG_API =                   1
    TAG_PATCH =                 7

    SAMPLE_INTERVAL =           1.0         # seconds between sampling

    RESET_QUARANTINE =          8.0         # time between reset and stable readings

    ADDR_TIME_TO_SAMPLE =        0          # 8 bit int         5mS steps
    ADDR_TIME_AFTER_SAMPLE =     1          # 8 bit int

    ADDR_COEFF_B =               2          # IEEE 32 bit float
    ADDR_COEFF_C =               6          # IEEE 32 bit float

    ADDR_ZERO =                 10          # 16 bit int
    ADDR_SPAN =                 12          # 16 bit int

    ADDR_DEG_C_OFFSET =         14          # 16 bit int
    ADDR_DEG_C_GAIN =           16          # 16 bit int

    ADDR_DC_IN_OFFSET =         18          # 16 bit int
    ADDR_DC_IN_GAIN =           20          # 16 bit int

    ADDR_DAC_OFFSET =           22          # 16 bit int
    ADDR_DAC_GAIN =             24          # 16 bit int

    ADDR_RANGE =                26          # 8 bit int

    ADDR_THERM_A =              27          # IEEE 32 bit float
    ADDR_THERM_B =              31          # IEEE 32 bit float
    ADDR_THERM_C =              35          # IEEE 32 bit float
    ADDR_THERM_D =              39          # IEEE 32 bit float

    ADDR_ALPHA =                43          # IEEE 32 bit float
    ADDR_BETA =                 47          # IEEE 32 bit float

    ADDR_T_CAL =                51          # IEEE 32 bit float


    # ----------------------------------------------------------------------------------------------------------------

    __BAUD_RATE =               19200

    __SERIAL_TIMEOUT =           2.0
    __LOCK_TIMEOUT =            10.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def null_datum(cls):
        return NDIRDatum(None, None, None)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def obtain_lock(cls):
        Lock.acquire(cls.__name__, TxNDIR.__LOCK_TIMEOUT)


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
    # NDIR implementation...

    def power_on(self):
        pass


    def power_off(self):
        pass


    def sample(self):
        temp = self.sample_temp()
        cnc = self.sample_co2(False)
        cnc_igl = self.sample_co2(True)

        return NDIRDatum(temp, cnc, cnc_igl)


    def version(self):
        return NDIRVersion(self.ID, NDIRTag(self.TAG_DEVICE, self.TAG_API, self.TAG_PATCH))


    def sample_interval(self):
        return self.SAMPLE_INTERVAL


    # ----------------------------------------------------------------------------------------------------------------
    # reset...

    def reset(self):
        lines = self.__transact('\r+++')
        datum = lines[0].strip()

        return datum


    # ----------------------------------------------------------------------------------------------------------------
    # low-level commands...

    def sample_co2(self, ideal_gas_law):
        lines = self.__transact('G' if ideal_gas_law else 'N')
        cnc = float(lines[0])

        return cnc


    def sample_temp(self):
        lines = self.__transact('T')
        datum = float(lines[0])

        return datum


    def sample_dc(self):
        lines = self.__transact('V')
        datum = int(lines[0])

        return datum


    def calibrate(self):
        self.__transact('D0')
        time.sleep(0.5)

        self.__transact('D1')
        time.sleep(0.5)


    # ----------------------------------------------------------------------------------------------------------------
    # EEPROM write...

    def eeprom_write_int8(self, addr, val8):
        val = val8 & 0xff

        self.__transact('W%02x%02x' % (addr, val))


    def eeprom_write_int16(self, addr, val16):
        msb = (val16 & 0xff00) >> 8
        lsb = (val16 & 0x00ff)

        self.__transact('W%02x%02x' % (addr, msb), 'W%02x%02x' % ((addr + 1), lsb))


    def eeprom_write_ieee32(self, addr, val32):
        vals = struct.unpack('BBBB', struct.pack('f', val32))

        self.__transact('W%02x%02x' % (addr, vals[0]), 'W%02x%02x' % ((addr + 1), vals[1]),
                        'W%02x%02x' % ((addr + 2), vals[2]), 'W%02x%02x' % ((addr + 3), vals[3]))


    # ----------------------------------------------------------------------------------------------------------------
    # EEPROM read...

    def eeprom_read_int8(self, addr):
        lines = self.__transact('E%02x' % addr)
        val = int(lines[0])

        return val


    def eeprom_read_int16(self, addr):
        lines = self.__transact('E%02x' % addr, 'E%02x' % (addr + 1))
        vals = [int(line) for line in lines]

        return (vals[0] << 8) | vals[1]


    def eeprom_read_ieee32(self, addr):
        lines = self.__transact('E%02x' % addr, 'E%02x' % (addr + 1), 'E%02x' % (addr + 2), 'E%02x' % (addr + 3))
        vals = [int(line) for line in lines]

        packed = struct.unpack('f', struct.pack('BBBB', *vals))

        return packed[0]


    # ----------------------------------------------------------------------------------------------------------------

    def __transact(self, *commands):
        ser = None

        TxNDIR.obtain_lock()

        try:
            #  TODO: use HostSerial instead?
            ser = serial.Serial(self.__device, TxNDIR.__BAUD_RATE, timeout=TxNDIR.__SERIAL_TIMEOUT)

            lines = []

            for command in commands:
                message = command + '\r'
                ser.write(message.encode("ascii"))

                lines.append(ser.readline().decode("ascii"))
                # print("lines: %s" % lines)

            return lines

        finally:
            if ser:
                ser.close()

            TxNDIR.release_lock()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TxNDIR:{device:%s}" % self.__device
