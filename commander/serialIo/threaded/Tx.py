# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from serial.serialutil import SerialException

from commander.serialIo.threaded.RtxBase import RtxBase


class Tx(RtxBase):
    """
    TX helper class
    """

    def __init__(self, serial, port):
        RtxBase.__init__(self, serial, port)
        self.data = b''
        self.__timeout = 0.0001

    def send(self, data):
        self.data += data
        self.runFlag.set()
        self.__timeout = 0.0001

    def run(self):
        import time
        while not self.threadStopFlag:
            if len(self.data) > 0:
                try:
                    number_of_bytes = self.serial.write(self.data)
                    if number_of_bytes != len(self.data):
                        print('error: send only %d bytes of %d' %
                              (number_of_bytes, len(self.data)))
                    self.data = b''
                except SerialException as ex:
                    self.serialPort.error(ex)
            else:
                self.__timeout = 1
            if not self.threadStopFlag:
                self.runFlag.clear()
                self.runFlag.wait()
            time.sleep(self.__timeout)

        if self.verbosity > 0x0f:
            print('tx stop')
