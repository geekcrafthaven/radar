# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd


class BaudrateCmd(GenericCmd):
    
    BAUDRATE = {
        '9600': 0x002580,
        '19200': 0x004B00,
        '38400': 0x009600,
        '57600': 0x00E100,
        '115200': 0x01C200,
        '256000': 0x03E800,
    }

    def __init__(self, command):
        GenericCmd.__init__(self, command)
