# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.utilities.ints import b2i


class Area:
    def __init__(self):
        self.__identifier = 0xff
        self.__type = 0xff
        self.__tl_x = 0xff
        self.__tl_y = 0xff
        self.__bl_x = 0xff
        self.__bl_y = 0xff
        self.__tr_x = 0xff
        self.__tr_y = 0xff
        self.__br_x = 0xff
        self.__br_y = 0xff

    @property
    def identifier(self):
        return self.__identifier

    @property
    def type(self):
        return self.__type

    @property
    def data(self):
        return [
            self.__tl_x,
            self.__tl_y,
            self.__bl_x,
            self.__bl_y,
            self.__br_x,
            self.__br_y,
            self.__tr_x,
            self.__tr_y,
        ]

    @property
    def tl(self):
        return (self.__tl_x, self.__tl_y)

    @property
    def bl(self):
        return (self.__bl_x, self.__bl_y)

    @property
    def tr(self):
        return (self.__tr_x, self.__tr_y)

    @property
    def br(self):
        return (self.__br_x, self.__br_y)

    def deserialize(self, _data):
        if len(_data) < 10:
            _data = [0] * (10-len(_data)) + _data

        self.__identifier = _data[0] & 0x03
        self.__type = _data[1] & 0x01
        self.__tl_x = _data[2]
        self.__tl_y = _data[3]
        self.__bl_x = _data[4]
        self.__bl_y = _data[5]
        self.__br_x = _data[6]
        self.__br_y = _data[7]
        self.__tr_x = _data[8]
        self.__tr_y = _data[9]

    def serialize(self):
        data = []

        data[0] = self.__identifier
        data[1] = self.__type
        data[2] = self.__tl_x
        data[3] = self.__tl_y
        data[4] = self.__bl_x
        data[5] = self.__bl_y
        data[6] = self.__br_x
        data[7] = self.__br_y
        data[8] = self.__tr_x
        data[9] = self.__tr_y

        return data

    def __str__(self):
        from commander.utilities.PrettyPrint import VDELIM
        s = ''
        s += '%-20s%c %02X %d' % ('identifier', VDELIM, self.identifier,
                                  self.identifier)
        s += '\n'
        s += '%-20s%c %02X %s' % ('type', VDELIM, self.type,
                                  'detect' if self.type == 0 else 'ignore')
        s += '\n'
        s += '%-20s%c %02X %02X (%+4.2f,%+4.2f)' % ('top-left', VDELIM, self.__tl_x, self.__tl_y,
                                                    b2i(self.__tl_x), b2i(self.__tl_y))
        s += '\n'
        s += '%-20s%c %02X %02X (%+4.2f,%+4.2f)' % ('btm-left', VDELIM, self.__bl_x, self.__bl_y,
                                                    b2i(self.__bl_x), b2i(self.__bl_y))
        s += '\n'
        s += '%-20s%c %02X %02X (%+4.2f,%+4.2f)' % ('btm-right', VDELIM, self.__br_x, self.__br_y,
                                                    b2i(self.__br_x), b2i(self.__br_y))
        s += '\n'
        s += '%-20s%c %02X %02X (%+4.2f,%+4.2f)' % ('top-right', VDELIM, self.__tr_x, self.__tr_y,
                                                    b2i(self.__tr_x), b2i(self.__tr_y))

        return s
