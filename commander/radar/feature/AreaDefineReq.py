# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.feature.Area import Area
from commander.radar.feature.AreaCmd import AreaCmd
from commander.utilities.ints import b2i, i2b


class AreaDefineReq(AreaCmd):
    def __init__(self, _identifier, _type, *_area):
        AreaCmd.__init__(self, GenericCmd.COMMANDS['AREA_DEFINE'])

        self.__identifier = int(_identifier, 10) & 0x03

        _area = [i2b((int(a, 10))) for a in _area]
        if len(_area) < 8:
            _area = [0]*(8-len(_area)) + _area
        self.__area = Area()
        self.__area.deserialize(_area)

        self.__type = int(_type, 10) & 0x01

    @property
    def identifier(self):
        return self.__identifier

    @property
    def area(self):
        return self.__area.data

    @property
    def type(self):
        return self.__type

    @property
    def sdu(self):
        return [self.command, self.identifier] + self.area + [self.__type]

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %s' % ('command', VDELIM, self.command,
                                  self.str_command(self.command, GenericCmd.COMMANDS))
        s += '\n'
        s += '%-20s%c %02X %d' % ('identifier', VDELIM, self.identifier,
                                  self.identifier)

        tl = self.__area.tl
        bl = self.__area.bl
        br = self.__area.br
        tr = self.__area.tr

        s += '\n'
        s += '%-20s%c %02X %02X (%+4.2f,%+4.2f)' % ('top-left', VDELIM, tl[0], tl[1],
                                                    b2i(tl[0]), b2i(tl[1]))
        s += '\n'
        s += '%-20s%c %02X %02X (%+4.2f,%+4.2f)' % ('btm-left', VDELIM, bl[0], bl[1],
                                                    b2i(bl[0]), b2i(bl[1]))
        s += '\n'
        s += '%-20s%c %02X %02X (%+4.2f,%+4.2f)' % ('btm-right', VDELIM, br[0], br[1],
                                                    b2i(br[0]), b2i(br[1]))
        s += '\n'
        s += '%-20s%c %02X %02X (%+4.2f,%+4.2f)' % ('top-right', VDELIM, tr[0], tr[1],
                                                    b2i(tr[0]), b2i(tr[1]))

        s += '\n'
        s += '%-20s%c %02X %s' % ('type', VDELIM, self.type,
                                  'detect' if self.type == 0 else 'ignore')

        return s
