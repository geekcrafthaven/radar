# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.control.IdentityCmd import IdentityCmd


class IdentityCfm(IdentityCmd):
    def __init__(self, command):
        IdentityCmd.__init__(self, command[0])

        payload = command[1]
        if len(payload) != 8:
            payload = [0] * (8-len(payload)) + payload

        self.__year = (payload[0] >> 4) + 2020
        self.__month = payload[0] & 0x0f
        self.__day = payload[1]
        self.__major = payload[2]
        self.__minor = payload[3]
        self.__identifier = payload[4:]

    @property
    def date(self):
        return '%02d.%02d.%04d' % (self.__day, self.__month, self.__year)

    @property
    def revision(self):
        return '%d.%d' % (self.__major, self.__minor)

    @property
    def identifier(self):
        return ''.join(['%02X' % a for a in self.__identifier])

    @GenericCmd.fields.getter
    def fields(self):
        command = self.str_command(self.command)
        identity_fields = {
            command:  {
                'DATE': self.date,
                'REVISION': self.revision,
                'IDENTIFIER': self.identifier,
            }
        }
        return identity_fields

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  GenericCmd.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %02X %04X %s' % ('date', VDELIM, self.__day, self.__month, self.__year,
                                            self.date)
        s += '\n'
        s += '%-20s%c %02X %02X %s' % ('revision', VDELIM, self.__major, self.__minor,
                                       self.revision)
        s += '\n'
        s += '%-20s%c %s %s' % ('identifier', VDELIM, ' '.join(['%02X' % a for a in self.__identifier]),
                                self.identifier)

        return s
