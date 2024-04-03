# -*- coding: utf-8 -*-

# Copyright (c) 2023, Roman Koch, koch.roman@gmail.com
# All rights reserved
#
# SPDX-License-Identifier: MIT

import struct

def bytes_to_uint16(_bytes):
    return (_bytes[0] << 8) + _bytes[1]


def uint16_to_bytes(_value):
    return [(_value >> 8) & 0xff,
            (_value >> 0) & 0xff]


def bytes_to_uint32(_bytes):
    return (_bytes[0] << 24) + (_bytes[1] << 16) + (_bytes[2] << 8) + _bytes[3]


def uint32_to_bytes(_value):
    return [(_value >> 24) & 0xff,
            (_value >> 16) & 0xff,
            (_value >> 8) & 0xff,
            (_value >> 0) & 0xff]


def bytes_to_uint64(_bytes):
    value = (_bytes[0] << 56) + (_bytes[1] << 48) + (_bytes[2] << 40) + (_bytes[3] << 32) + \
        (_bytes[4] << 24) + (_bytes[5] << 16) + \
        (_bytes[6] << 8) + (_bytes[7] << 0)
    return value


def uint64_to_bytes(_value):
    return [(_value >> 56) & 0xff,
            (_value >> 48) & 0xff,
            (_value >> 40) & 0xff,
            (_value >> 32) & 0xff,
            (_value >> 24) & 0xff,
            (_value >> 16) & 0xff,
            (_value >> 8) & 0xff,
            (_value >> 0) & 0xff]
