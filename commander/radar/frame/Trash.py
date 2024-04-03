# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


class Trash(object):
    DEFAULT_VERBOSITY = 0

    def __init__(self):
        self.address = 0x00
        self.control = 0x00

    def serialize(self, header, data):
        print('SERIALIZE NOT SUPPORTED FOR TRASH')
        payload = data.serialize()
        return self.control, payload

    def deserialize(self, header, data):
        from commander.radar.frame.IncomingMessage import IncomingMessage
        msg = IncomingMessage(data, 'Unknown')
        return {'msg': msg}
