#!/usr/bin/env python3

"""
Created on 19 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://raspberrypi.stackexchange.com/questions/450/how-can-i-connect-to-a-usb-serial-device
"""

import serial
import time


# --------------------------------------------------------------------------------------------------------------------

ser = None

try:
    ser = serial.Serial('/dev/ttyUSB0', 19200)
    print(ser)

    ser.write(b'\r')                            # clear serial channel

    ser.write(b'+++\r')                         # cmd: reset NDIR
    print(ser.readline())                       # read message

    while True:
        ser.write(b'N\r')                       # cmd: send ppm
        line =  ser.readline()                  # read message

        datum = float(line.decode().strip())
        print(datum)

        time.sleep(2)

finally:
    if ser:
        ser.close()
