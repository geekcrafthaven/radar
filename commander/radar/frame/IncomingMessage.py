# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

class IncomingMessage:
    """
    incoming monitoring message base class
    """

    def __init__(self, data, name='Generic', msg_type='hex'):
        self.DATA = data
        self.NAME = name
        self.TYPE = msg_type

    def __str__(self):
        return self.NAME + ' ' + self.add_str()

    def add_str(self):
        if self.TYPE == 'str':
            return ''.join(chr(b) for b in self.DATA)
        else:
            return ''.join('%02X ' % b for b in self.DATA)
