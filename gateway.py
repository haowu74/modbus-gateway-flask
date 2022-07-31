import imp
from unit import Unit
import serial
import time
from os.path import exists
from flask import json

class Gateway:
    def __init__(self, file):
        self.file = file
        if exists(file):
            with open(file, 'r') as f:
                units = json.load(f)
                self.units = units
        else:
            self.units = []
        self.usb = serial.Serial(port = '/dev/ttyUSB0', baudrate = 19200, parity = serial.PARITY_NONE, stopbits = 1, bytesize = 8, timeout = 0)


    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit_id):
        self.unit = list(filter(lambda x: x.unit != unit_id, self.units))

    def load_from_file(self, file):
        pass

    def save_to_file(self, file):
        pass

    def clear(self):
        self.units.clear()

    def writeRegister(self, address, register, value):
        pass

    def trigger(self, unit, lock=True):
        pass

    def loop(self):
        while True:
            time.sleep(1)
            bytes = self.usb.read(100)
            
            print(' '.join('{:02X}'.format(a) for a in bytes))

    def isLock(self, bytes):
        pass

    def isUnlock(self, bytes):
        pass

