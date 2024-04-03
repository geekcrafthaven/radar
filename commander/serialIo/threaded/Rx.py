# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from serial.serialutil import SerialException

from commander.serialIo.threaded.RtxBase import RtxBase


class Rx(RtxBase):
    """
    RX helper class
    """
    DELAY_MIN = 0.10
    DELAY_MAX = 0.25

    def __init__(self, serial, port, _handler):
        RtxBase.__init__(self, serial, port)
        self.__handler = _handler
        self.__delay = Rx.DELAY_MIN

    def run(self):
        while not self.threadStopFlag:
            import time
            self.__handler.enter()

            try:
                while self.serial.available() > 0:
                    data = self.serial.read(self.serial.available())
                    self.__handler.perform(data)

                self.__handler.perform()

                self.__delay = Rx.DELAY_MIN

            except SerialException as ex:
                self.serialPort.error(ex)

            self.__handler.exit()
            time.sleep(self.__delay)

        if self.verbosity > 0x0f:
            print('rx stop')
