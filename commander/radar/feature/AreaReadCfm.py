# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.feature.Area import Area
from commander.radar.feature.AreaCmd import AreaCmd


class AreaReadCfm(AreaCmd):
    def __init__(self, command):
        AreaCmd.__init__(self, command[0])

        payload = command[1]
        if len(payload) < 30:
            payload = [0x00] * (30-len(payload)) + payload

        self.__area_1 = Area()
        self.__area_2 = Area()
        self.__area_3 = Area()

        self.__area_1.deserialize(payload[:10])
        self.__area_2.deserialize(payload[10:20])
        self.__area_3.deserialize(payload[20:30])

    @property
    def area_1(self):
        return self.__area_1

    @property
    def area_2(self):
        return self.__area_2

    @property
    def area_3(self):
        return self.__area_3

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command): {
                'AREA_1': str(self.area_1),
                'AREA_2': str(self.area_1),
                'AREA_3': str(self.area_1),
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s\n' % ('command', VDELIM, self.command,
                                    self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += str(self.__area_1)
        s += '\n'
        s += str(self.__area_2)
        s += '\n'
        s += str(self.__area_3)

        return s
