# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.feature.FormatCmd import FormatCmd


class FormatSetCfm(FormatCmd):
    def __init__(self, command):
        FormatCmd.__init__(self, command[0])

        payload = command[1]
        if len(payload) == 0:
            payload = [0xff]

        self.__result = payload[0]

    @property
    def result(self):
        return self.__result

    @GenericCmd.fields.getter
    def fields(self):
        return {
            self.str_command(self.command, GenericCmd.COMMANDS): {
                'RESULT': self.str_field(self.result, GenericCmd.RESULT),
            }
        }

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %s' % ('result', VDELIM, self.result,
                                  self.str_field(self.result, GenericCmd.RESULT))

        return s
