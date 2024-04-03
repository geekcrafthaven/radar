# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.utilities.PrettyPrint import SLINE, wd


class Host:
    DEFAULT_VERBOSITY = 0

    def __init__(self):
        self.address = 0x20
        self.control = 0x01  # legacy

        self.verbosity = self.DEFAULT_VERBOSITY

        from commander.config import verbosity
        self.verbosity = verbosity()

    def serialize(self, data):
        command = data[0]
        payload = data[1:]

        if self.verbosity >= 0x0f:
            print(SLINE * wd)
            print('tx RADAR: %02X %s' %
                  (command, ''.join('%02X' % byte for byte in payload)))

        sdu = [command] + payload

        return self.control, sdu

    def deserialize(self, ctrl, sdu):
        if ctrl != self.control:
            print('deserialize: wrong control')

        command = sdu[0]
        payload = sdu[1:]

        if self.verbosity >= 0x0f:
            print(SLINE * wd)
            print('rx RADAR: %02X %s' %
                  (command, ''.join('%02X' % byte for byte in payload)))

        return [command, payload]
