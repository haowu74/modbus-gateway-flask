import imp
import threading
from unit import Unit
import serial
import serial.rs485
import RPi.GPIO as GPIO
import time
from os.path import exists
from flask import json
import crcmod

class Gateway:
    def __init__(self, file):
        print('init gateway')
        self.file = file
        self.delay_timer = [threading.Timer(0, None)] * 200
        self.crc = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
        if exists(file):
            with open(file, 'r') as f:
                units = json.load(f)
                self.units = units
        else:
            self.units = []
        GPIO.setmode(GPIO.BOARD)
        self.usb = serial.Serial(port='/dev/ttyUSB0',baudrate=19200,parity=serial.PARITY_NONE, stopbits = 1, bytesize = 8, timeout = 0)
        GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.output(7, 1)
        self.modbus = serial.rs485.RS485(port='/dev/ttyS0',baudrate=0)
        self.modbus = serial.rs485.RS485(port='/dev/ttyS0',baudrate=9600,parity=serial.PARITY_EVEN)

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

    def operateRelay(self, address, register, command):
        msg = [0] * 8
        msg[0] = address
        msg[1] = 0x6
        msg[2] = (register & 0xff00) >> 8
        msg[3] = register & 0xff
        msg[4] = command
        msg[5] = 0
        crc = self.crc(bytearray(msg[0:6]))
        msg[6] = crc & 0xff
        msg[7] = (crc & 0xff00) >> 8
        print('Modbus: '+' '.join('{:02X}'.format(a) for a in msg))
        self.modbus.write(bytes(msg[0:8]))

    def writeRegister(self, id, address, register, delay):
        self.delay_timer[id].cancel()
        self.operateRelay(address, register, 1)
        self.delay_timer[id] = threading.Timer(delay, lambda: self.operateRelay(address, register, 2))
        self.delay_timer[id].start()

    def trigger(self, id, lock=True):
        #print(self.units)
        if len(self.units) >0:
            units = list(filter(lambda x: int(x['id'].split('/')[0]) == id, self.units))
            if units is not None and len(units) > 0 and units[0]['selected']:
                address = int(units[0]['address'])
                register = int(units[0]['register'])
                delay = int(units[0]['delay'])
                self.writeRegister(id, address, register, delay)

    def loop(self, islocked):
        while True:
            time.sleep(1)
            bytes = self.usb.read(100)
            if len(bytes) > 0:
                print(' '.join('{:02X}'.format(a) for a in bytes))
            if len(bytes) >= 9:
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
