# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.feature.FormatCmd import FormatCmd


class FormatGetReq(FormatCmd):
    def __init__(self):
        FormatCmd.__init__(self, GenericCmd.COMMANDS['FORMAT_GET'])

        self.__payload = 0x01

    @property
    def payload(self):
        return self.__payload

    @property
    def sdu(self):
        return [self.command, self.payload]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X' % ('payload', VDELIM, self.payload)

        return s
