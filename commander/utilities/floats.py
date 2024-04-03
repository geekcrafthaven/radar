# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import struct


def convert_to_float(data_bytes):
    return round(struct.unpack('!f', b''.join([b'%c' % byte for byte in data_bytes[::-1]]))[0], 6)


def convert_to_long(float_value):
    return int(b''.join([b'%02X' % byte for byte in struct.pack('!f', float_value)][::-1]), 16)


def convert_to_bytes(float_value):
    # return [byte for byte in struct.pack('!f', float_value)]
    raw_value = convert_to_long(float_value)
    return [(raw_value >> 24) & 0xff,
            (raw_value >> 16) & 0xff,
            (raw_value >> 8) & 0xff,
            (raw_value >> 0) & 0xff]
