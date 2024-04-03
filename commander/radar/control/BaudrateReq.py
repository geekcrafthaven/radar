# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.control.BaudrateCmd import BaudrateCmd


class BaudrateReq(BaudrateCmd):
    def __init__(self, _function):
        BaudrateCmd.__init__(self, GenericCmd.COMMANDS['BAUDRATE'])

        baudrate = _function.upper().strip()
        if GenericCmd.find_field(baudrate, BaudrateCmd.BAUDRATE):
            self.__baudrate = BaudrateCmd.BAUDRATE[baudrate]
        else:
            raise Exception('unknown function')

    @property
    def baudrate(self):
        return self.__baudrate

    @property
    def sdu(self):
        return [self.command, self.__baudrate]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '%-20s%c %02X %s\n' % ('baudrate', VDELIM, self.__baudrate,
                                    GenericCmd.str_field(self.__baudrate, BaudrateCmd.BAUDRATE))

        return s
