import imp
from unit import Unit
import serial
import time
from os.path import exists
from flask import json
import crcmod

class Gateway:
    def __init__(self, file):
        self.file = file
        self.crc = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        if exists(file):
            with open(file, 'r') as f:
                units = json.load(f)
                self.units = units
        else:
            self.units = []
        self.usb = serial.Serial(port = '/dev/ttyUSB0', baudrate = 19200, parity = serial.PARITY_NONE, \
            stopbits = 1, bytesize = 8, timeout = 0)
        # self.modbus = serial.Serial()


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
        bytes = [0] * 8
        bytes[0] = address
        bytes[1] = 0x6
        bytes[2] = register & 0xff00 >> 8
        bytes[3] = register & 0xff
        bytes[4] = value & 0xff00 >> 8
        bytes[5] = value & 0xff
        crc = self.crc(bytes[0:6])
        bytes[6] = crc & 0xff
        bytes[7] = crc & 0xff00 >> 8
        self.modbus.write(bytes[0:8])

    def trigger(self, id, lock=True):
        unit = filter(lambda x: x.unit == id, self.units)
        if unit is not None and unit.selected:
            address = unit.address
            register = unit.register
            self.writeRegister(address, register, 0x100)

    def loop(self):
        while True:
            time.sleep(1)
            bytes = self.usb.read(100)
            print(' '.join('{:02X}'.format(a) for a in bytes))

            id = self.getReleaseDoorUnit(bytes)
            if id > 0:
                self.trigger(id)


    def isDoorReleaseCommand(self, bytes):
        # 55 AA 00 0C 00 02 01 00 01
        return bytes[0] == 0x55 and bytes[1] == 0xaa and bytes[2] == 0x0 and bytes[3] == 0xc and \
            bytes[4] == 0x0 and bytes[5] == 0x2 and bytes[6] == 0x1 and bytes[7] == 0x0 and bytes[8] == 0x1

    def getReleaseDoorUnit(self, bytes):
        if self.isDoorReleaseCommand(bytes):
            return bytes[9]
        else:
            return -1        



