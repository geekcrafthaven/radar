# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd


class FormatCmd(GenericCmd):
    MODE = {
        'POSITION': 0x01,
        'AREA': 0x02,
        'COMBO': 0x03,

        'UNDEFINED': 0xff,
    }

    def __init__(self, command):
        GenericCmd.__init__(self, command)
