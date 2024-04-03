# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from serial.serialutil import SerialException
#from commander.hci.HciHandler import HciHandler
from commander.radar.RadarHandler import RadarHandler
from commander.serialIo.phy.SerialPhyCommon import SerialPhyCommon
from commander.serialIo.phy.SerialPhyPython import SerialPhyPython
from commander.serialIo.threaded.Rx import Rx
from commander.serialIo.threaded.Tx import Tx

import commander.termbase as output


class SerialPortThreaded:
    """
    serial port
    """

    INTERPRETER = {
        'hci': 0,
        'scpi': 1,
        'radar': 2
    }

    DEFAULT_BAUDRATE = 115200
    DEFAULT_BYTESIZE = SerialPhyCommon.BITS_8
    DEFAULT_PARITY = SerialPhyCommon.PARITY_NONE
    DEFAULT_STOPBITS = SerialPhyCommon.STOP_BITS_1
    DEFAULT_FLOWCONTROL = SerialPhyCommon.FLOW_NONE
    DEFAULT_TIMEOUT = None

    def __init__(self, _alias, _device, _parameter, _list=None):
        _interpreter = _parameter.interpreter
        assert _interpreter in SerialPortThreaded.INTERPRETER, "port %s, unknown interpreter % s" % (
            _alias, _interpreter)
        self.__interpreter = SerialPortThreaded.INTERPRETER[_interpreter]

        self.params = {}
        self.__parse_device_config(_device)

        if _device.device.isdigit():
            self.portnumber = int(_device.device)
            if self.portnumber < 255:
                self.ser = SerialPhyPython(self.portnumber)
        else:
            self.portnumber = _device.device
            self.ser = SerialPhyPython(self.portnumber)

        self.__handler = None
        if self.__interpreter == SerialPortThreaded.INTERPRETER['hci']:
            pass
            # self.__handler = HciHandler(self, _alias)
        elif self.__interpreter == SerialPortThreaded.INTERPRETER['scpi']:
            pass
            # dialect = _parameter.dialect
            # self.__handler = ScpiHandler(self, _alias, dialect)
        elif self.__interpreter == SerialPortThreaded.INTERPRETER['radar']:
            self.__handler = RadarHandler(self, _alias)

        assert self.__handler is not None, "port %s handler is none" % _alias

        self.tx = Tx(self.ser, self)
        self.rx = Rx(self.ser, self, self.__handler)
        self.threads = [self.rx, self.tx]

        self.list = _list

    @property
    def alias(self):
        return self.__handler.alias

    @property
    def interpreter(self):
        return self.__interpreter

    @property
    def handler(self):
        return self.__handler

    def start(self):
        try:
            if self.ser is not None:
                self.ser.open()
                if self.ser.is_open():
                    self.ser.set_baudrate(self.params['baudrate'])
                    self.ser.set_data_bits(self.params['bits'])
                    self.ser.set_flowcontrol(self.params['flowcontrol'])
                    self.ser.set_parity(self.params['parity'])
                    self.ser.set_stop_bits(self.params['stopbits'])
                    self.ser.set_timeouts(self.params['timeout'])

                    for t in self.threads:
                        t.start()
                    return True

        except SerialException as msg:
            print('serial port: start error:', msg)
        except Exception as msg:
            print('serial port: start error:', msg)

        return False

    def stop(self):
        try:
            for t in self.threads:
                t.stop()

            for t in self.threads:
                t.join()

            self.ser.close()
        except Exception as msg:
            print('serial port: stop error:', msg)

    def send(self, buf):
        self.tx.send(buf)

    def response(self):
        self.__handler.response()

    def get_phy(self):
        return self.ser

    def error(self, msg):
        if self.list is not None:
            self.list.remove(self.alias)
        self.stop()
        output.show_text('port %s exception: %s' %
                         (self.alias, msg))

    def __parse_device_config(self, _device):
        self.params['baudrate'] = int(_device.baudrate)

        if 'bits' in dir(_device):
            if int(_device.bits) == 7:
                self.params['bits'] = SerialPhyCommon.BITS_7
            elif int(_device.bits) == 8:
                self.params['bits'] = SerialPhyCommon.BITS_8
            else:
                self.params['bits'] = self.DEFAULT_BYTESIZE
        else:
            self.params['bits'] = self.DEFAULT_BYTESIZE

        if 'stopbits' in dir(_device):
            if int(_device.stopbits) == 1:
                self.params['stopbits'] = SerialPhyCommon.STOP_BITS_1
            elif int(_device.stopbits) == 2:
                self.params['stopbits'] = SerialPhyCommon.STOP_BITS_2
            else:
                self.params['stopbits'] = self.DEFAULT_STOPBITS
        else:
            self.params['stopbits'] = self.DEFAULT_STOPBITS

        if 'parity' in dir(_device):
            if _device.parity == 'none':
                self.params['parity'] = SerialPhyCommon.PARITY_NONE
            elif _device.parity == 'odd':
                self.params['parity'] = SerialPhyCommon.PARITY_ODD
            elif _device.parity == 'even':
                self.params['parity'] = SerialPhyCommon.PARITY_EVEN
            elif _device.parity == 'mark':
                self.params['parity'] = SerialPhyCommon.PARITY_MARK
            elif _device.parity == 'space':
                self.params['parity'] = SerialPhyCommon.PARITY_SPACE
            else:
                self.params['parity'] = self.DEFAULT_PARITY
        else:
            self.params['parity'] = self.DEFAULT_PARITY

        if 'flowcontrol' in dir(_device):
            if _device.flowcontrol == 'none':
                self.params['flowcontrol'] = SerialPhyCommon.FLOW_NONE
            elif _device.flowcontrol == 'rts-cts':
                self.params['flowcontrol'] = SerialPhyCommon.FLOW_RTS_CTS
            elif _device.flowcontrol == 'dtr-dsr':
                self.params['flowcontrol'] = SerialPhyCommon.FLOW_DTR_DSR
            elif _device.flowcontrol == 'xon-xoff':
                self.params['flowcontrol'] = SerialPhyCommon.FLOW_XON_XOFF
            else:
                self.params['flowcontrol'] = self.DEFAULT_FLOWCONTROL
        else:
            self.params['flowcontrol'] = self.DEFAULT_FLOWCONTROL

        self.params['timeout'] = self.DEFAULT_TIMEOUT
