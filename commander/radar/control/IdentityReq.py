# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.control.IdentityCmd import IdentityCmd


class IdentityReq(IdentityCmd):
    def __init__(self):
        IdentityCmd.__init__(self, GenericCmd.COMMANDS['IDENTITY'])

        self.__payload = 0x01

    @property
    def sdu(self):
        return [self.command, self.payload]

    @property
    def payload(self):
        return self.__payload

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X' % ('payload', VDELIM, self.payload)

        return s
