# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from abc import abstractmethod


class SerialPhyCommon:
    """
    serial phy common
    """

    # Word Lengths
    BITS_8 = 8
    BITS_7 = 7

    # Stop Bits
    STOP_BITS_1 = 1
    STOP_BITS_2 = 2

    # Parity
    PARITY_NONE = 'N'
    PARITY_ODD = 'O'
    PARITY_EVEN = 'E'
    PARITY_MARK = 'M'
    PARITY_SPACE = 'S'

    # Flow Control
    FLOW_NONE = 'none'
    FLOW_RTS_CTS = 'rtscts'
    FLOW_DTR_DSR = 'dtrdsr'
    FLOW_XON_XOFF = 'xonxoff'

    def __init__(self, device):
        """
        Constructor
        """
        self.drv = device

    def open(self):
        self.drv.open()

    @abstractmethod
    def is_open(self):
        pass

    def close(self):
        self.drv.close()

    @abstractmethod
    def flush(self):
        pass

    def write(self, data):
        return self.drv.write(data)

    def read(self, size=1):
        return self.drv.read(size)

    @abstractmethod
    def available(self):
        pass

    def get_serial_object(self):
        return self.drv

    @abstractmethod
    def set_baudrate(self, rate):
        pass

    @abstractmethod
    def set_flowcontrol(self, flow, xon=-1, xoff=-1):
        pass

    @abstractmethod
    def set_timeouts(self, rx, tx=0):
        pass

    @abstractmethod
    def set_data_bits(self, bits):
        pass

    @abstractmethod
    def set_stop_bits(self, bits):
        pass

    @abstractmethod
    def set_parity(self, parity):
        pass
