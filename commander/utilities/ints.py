# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


def b2i(_value):
    a = int(_value)
    if a > 127:
        return (a - 0x0100) 
    return a

def i2b(_value):
    if _value < 0:
        return (0x0100 + _value)
    return _value
