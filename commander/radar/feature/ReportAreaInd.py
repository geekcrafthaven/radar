# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.feature.ReportCmd import ReportCmd


class ReportAreaInd(ReportCmd):
    def __init__(self, command):
        ReportCmd.__init__(self, command[0])

        payload = command[1]
        if len(payload) < 3:
            payload = [0] * (4-len(payload)) + payload

        self.__area_1 = payload[0]
        self.__area_2 = payload[1]
        self.__area_3 = payload[2]

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
        event_fields = {
            'AREA_1': self.__area_1,
            'AREA_2': self.__area_2,
            'AREA_3': self.__area_3,
        }
        return {self.str_command(self.command, GenericCmd.COMMANDS): event_fields}

    def __str__(self):
        from commander.radar.RadarParser import RadarParser
        if not RadarParser.report_enabled:
            return ''

        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('area 1', VDELIM, self.__area_1, self.__area_1 == 1)
        s += '\n'
        s += '%-20s%c %02X %s' % ('area 2', VDELIM, self.__area_2, self.__area_2 == 1)
        s += '\n'
        s += '%-20s%c %02X %s' % ('area 3', VDELIM, self.__area_3, self.__area_3 == 1)
        return s
