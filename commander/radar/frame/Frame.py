# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.frame.Trash import Trash
from commander.radar.frame.CheckSum import CheckSum
from commander.utilities.PrettyPrint import SLINE, wd
from commander.config import verbosity


class Frame:
    DEFAULT_VERBOSITY = 0

    DELIM = [0xff, 0xee, 0xdd]

    PARSERS = {}  # 0x20

    def __init__(self):
        self.trash = Trash()

        self.verbosity = Frame.DEFAULT_VERBOSITY
        self.verbosity = verbosity()

        self.__start = 0
        self.__stop = 0
        self.__data = None
        self.__data_len = 0

    @property
    def data(self):
        return self.__data

    @property
    def start(self):
        return self.__start

    @property
    def stop(self):
        return self.__stop

    def __print(self, byte_string):
        # Achtung: gibt kompletten buffer aus
        # print 'byte_string:', ''.join('%02X ' % byte_string[i] for i in range(0, len(byte_string)) )
        pass

    def register(self, address, parser):
        Frame.PARSERS[address] = parser
        if self.verbosity >= 0x0f:
            print('frame payload parser reg: %d' % address)

    def serialize(self, address, _data):
        if address not in Frame.PARSERS:
            if self.verbosity >= 0x0f:
                print('frame check: unknown address')
            return False

        ctrl, data = self.PARSERS[address].serialize(_data)

        checksum = (CheckSum('sum').perform(data)) & 0xff
        data_len = len(data)

        command = Frame.DELIM + \
            [data_len >> 8, data_len & 0xff] + data + \
            [checksum] + \
            Frame.DELIM[::-1]

        bytes_string = b''.join(b'%c' % byte for byte in command)

        if self.verbosity >= 0x0f:
            print(SLINE * wd)
            print('tx HDLC: %s' % (b' '.join(b'%02X' %
                  byte for byte in bytes_string)).upper())

        return bytes_string

    def check(self, data):
        self.__start = 0
        self.__stop = 0
        self.__data = None
        self.__data_len = 0

        frame_start = 0
        while len(data[frame_start:]) > frame_start + 2 and \
                (data[frame_start+0] != Frame.DELIM[0] or
                 data[frame_start+1] != Frame.DELIM[1] or
                 data[frame_start+2] != Frame.DELIM[2]):
            frame_start += 1

        self.__start = frame_start
        data = data[frame_start:]

        if len(data) < 5:
            return False

        self.__data_len = (data[3] << 8) + data[4]

        if len(data) < self.__data_len + 9:
            return False

        in_calc_check = (CheckSum('sum').perform(
            data[5:5+self.__data_len])) & 0xff
        check = data[5+self.__data_len]
        if check != in_calc_check:
            if self.verbosity >= 0x0f:
                print('%s' % (b''.join(b'%02X' % byte for byte in data)))
                print('frame check: wrong checksum: %04X %04X' %
                      (check, in_calc_check))
            return False

        self.__stop = self.__start + 6 + self.__data_len + 2

        if len(data[frame_start:]) > 6+self.__data_len+2 and \
                (data[6+self.__data_len+0] != Frame.DELIM[2] or
                 data[6+self.__data_len+1] != Frame.DELIM[1] or
                 data[6+self.__data_len+2] != Frame.DELIM[0]):
            print('frame check: wrong frame delimiter')
            return False

        # return [byte for byte in data[:data_len + 6]]

        self.__data = [int(a) for a in data[5:5+self.__data_len]]

        return True

    def deserialize(self, _frame):
        print('RADAR rx:', ' '.join('%02X' % byte for byte in _frame))

        address = 0x20
        parser = self.trash
        if address in Frame.PARSERS:
            parser = Frame.PARSERS[address]

        ctrl = 0x01

        payload = _frame

        return {'address': address, 'ctrl': ctrl, 'payload': parser.deserialize(ctrl, payload)}
