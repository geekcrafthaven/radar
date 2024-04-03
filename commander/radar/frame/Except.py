# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

class Except(object):

    DEFAULT_VERBOSITY = 0

    def __init__(self):
        self.address = 0xff
        self.control = 0x01

    def serialize(self, header, data):
        print('SERIALIZE NOT SUPPORTED FOR Exception')
        payload = data.serialize()
        return self.control, payload

    def deserialize(self, header, data):
        return {'data': data}
