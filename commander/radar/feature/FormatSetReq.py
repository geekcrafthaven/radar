# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.feature.FormatCmd import FormatCmd


class FormatSetReq(FormatCmd):
    def __init__(self, _mode):
        FormatCmd.__init__(self, GenericCmd.COMMANDS['FORMAT_SET'])

        self.__mode = int(_mode, 10) & 0x03

    @property
    def mode(self):
        return self.__mode

    @property
    def sdu(self):
        return [self.command, self.mode]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('mode', VDELIM, self.mode,
                                  GenericCmd.str_field(self.mode, FormatCmd.MODE))

        return s
