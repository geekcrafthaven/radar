# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from serial import Serial
from commander.serialIo.phy.SerialPhyCommon import SerialPhyCommon

import commander.termbase as output


class SerialPhyPython(SerialPhyCommon):
    """
    simple serial io
    """

    def __init__(self, device):
        """
        Constructor
        """

        ser_dev = Serial()
        SerialPhyCommon.__init__(self, ser_dev)
        self.drv.port = device

    def available(self):
        try:
            return self.drv.inWaiting()
        except Exception as message:
            output.show_error('error: check data on serial port: %s' % message)

            return False

    def is_open(self):
        return self.drv.is_open

    def flush(self):
        return self.drv.flush()

    def set_baudrate(self, rate):
        self.drv.baudrate = rate

    def set_flowcontrol(self, flow, xon=-1, xoff=-1):
        if flow == SerialPhyCommon.FLOW_NONE:
            self.drv.xonxoff = False
            self.drv.rtscts = False
            self.drv.dtrdrs = False
        elif flow == SerialPhyCommon.FLOW_RTS_CTS:
            self.drv.xonxoff = False
            self.drv.rtscts = True
            self.drv.dtrdrs = False
        elif flow == SerialPhyCommon.FLOW_DTR_DSR:
            self.drv.xonxoff = False
            self.drv.rtscts = False
            self.drv.dtrdrs = True
        elif flow == SerialPhyCommon.FLOW_XON_XOFF:
            self.drv.xonxoff = True
            self.drv.rtscts = False
            self.drv.dtrdrs = False

    def set_timeouts(self, rx, tx=None):
        self.drv.timeout = rx

    def set_data_bits(self, bits):
        if bits == SerialPhyCommon.BITS_7:
            self.drv.bytesize = 7
        elif bits == SerialPhyCommon.BITS_8:
            self.drv.bytesize = 8

    def set_stop_bits(self, bits):
        if bits == SerialPhyCommon.STOP_BITS_1:
            self.drv.stopbits = 1
        elif bits == SerialPhyCommon.STOP_BITS_2:
            self.drv.stopbits = 2

    def set_parity(self, parity):
        if parity == SerialPhyCommon.PARITY_NONE:
            self.drv.parity = 'N'
        elif parity == SerialPhyCommon.PARITY_EVEN:
            self.drv.parity = 'E'
        elif parity == SerialPhyCommon.PARITY_ODD:
            self.drv.parity = 'O'
        elif parity == SerialPhyCommon.PARITY_MARK:
            self.drv.parity = 'M'
        elif parity == SerialPhyCommon.PARITY_SPACE:
            self.drv.parity = 'S'

    @staticmethod
    def list_devices():
        import os

        if os.name == 'nt':  # sys.platform == 'win32':
            from serial.tools.list_ports_windows import comports
        elif os.name == 'posix':
            from serial.tools.list_ports_posix import comports
        return comports()
