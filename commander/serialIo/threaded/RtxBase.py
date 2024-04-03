# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import threading


class RtxBase(threading.Thread):
    """
    RTX base class
    """

    def __init__(self, serial, port):
        threading.Thread.__init__(self)

        self.serial = serial
        self.threadStopFlag = False
        self.runFlag = threading.Event()
        self.serialPort = port

        from commander.config import verbosity
        self.verbosity = verbosity()

    def stop(self):
        self.threadStopFlag = True
        self.runFlag.set()
