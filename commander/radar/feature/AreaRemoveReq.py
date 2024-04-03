# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.feature.AreaCmd import AreaCmd


class AreaRemoveReq(AreaCmd):
    def __init__(self, _identifier):
        AreaCmd.__init__(self, GenericCmd.COMMANDS['AREA_REMOVE'])

        self.__identifier = int(_identifier, 10) & 0x03

    @property
    def identifier(self):
        return self.__identifier

    @property
    def sdu(self):
        return [self.command, self.identifier]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %d' % ('identifier', VDELIM, self.identifier,
                                  self.identifier)

        return s
