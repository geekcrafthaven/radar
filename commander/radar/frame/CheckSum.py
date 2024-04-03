# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class CheckSum:
    START_VALUE = 0x1021

    def __init__(self, algorithm='sum'):
        self.__start_value = CheckSum.START_VALUE
        self.__algorithm = None
        self.__switch_algorithm(algorithm.strip().lower())

    def __switch_algorithm(self, algorithm):
        if algorithm == 'crc16' or algorithm == 'sum':
            self.__algorithm = algorithm
        else:
            self.__algorithm = 'sum'
            print('algorithm "%s" unknown.' % algorithm)
            print('default algorithm: "%s".' % self.__algorithm)

    def perform(self, data):
        if self.__algorithm == 'crc16':
            crc = 0  # 0xffff
            for x in data:
                if isinstance(x, int):
                    crc = self.__calc_crc16(x, crc)
                else:
                    crc = self.__calc_crc16(int(x, 16), crc)
        elif self.__algorithm == 'sum':
            crc = 0
            for x in data:
                if isinstance(x, int):
                    crc = (crc + x) & 0xffff
                else:
                    crc = (crc + int(x, 16)) & 0xffff
        else:
            print('check sum calculation error: algorithm "%s" unknown.' %
                  self.__algorithm)

        return crc

    def __calc_crc16(self, x, init_value):
        crc = (init_value ^ x << 8) & 0xffff
        for bit in range(0, 8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1 ^ self.__start_value) & 0xffff
            else:
                crc = (crc << 1) & 0xffff

        return crc
