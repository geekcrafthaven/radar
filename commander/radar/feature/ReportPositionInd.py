# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.feature.ReportCmd import ReportCmd
from commander.utilities.ints import b2i


class ReportPositionInd(ReportCmd):
    def __init__(self, command):
        ReportCmd.__init__(self, command[0])

        payload = command[1]
        if len(payload) < 4:
            payload = [0] * (4-len(payload)) + payload

        self.__first_x = payload[0]
        self.__first_y = payload[1]
        self.__second_x = payload[2]
        self.__second_y = payload[3]

    @property
    def first(self):
        return (self.__first_x, self.__first_y)

    @property
    def second(self):
        return (self.__second_x, self.__second_y)

    @GenericCmd.fields.getter
    def fields(self):
        event_fields = {
            'FIRST_X': self.__first_x,
            'FIRST_Y': self.__first_y,
            'SECOND_X': self.__second_x,
            'SECOND_Y': self.__second_y,
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

        first_x =  b2i(self.__first_x)
        first_y =  b2i(self.__first_y)
        second_x = b2i(self.__second_x)
        second_y = b2i(self.__second_y)

        s += '%-20s%c %02X, %02x (%4.2f,%4.2f)' % ('first', VDELIM, self.__first_x, self.__first_y,
                                                   first_x, first_y)
        s += '\n'
        s += '%-20s%c %02X, %02x (%4.2f,%4.2f)' % ('second', VDELIM, self.__second_x, self.__second_y,
                                                   second_x, second_y)
        return s
