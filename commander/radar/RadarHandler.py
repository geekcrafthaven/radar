# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.frame.Frame import Frame
from commander.radar.frame.Except import Except
from commander.radar.frame.Host import Host
from commander.radar.frame.Trash import Trash
from commander.radar.RadarCommand import RadarCommand
from commander.radar.RadarParser import RadarParser
from commander.serialIo.threaded.SerLogger import SerLogger

import commander.termbase as output

class RadarHandler(SerLogger):
    def __init__(self, _port, _alias):
        SerLogger.__init__(self)

        self.__port = _port
        self.__alias = _alias

        self.__rx_buffer = b''

        self.__input_queue = list()

        self.__frame = Frame()

        self.__except = Except()
        self.__host = Host()
        self.__trash = Trash()

        self.__frame.register(self.__trash.address, self.__trash)
        self.__frame.register(self.__except.address, self.__except)
        self.__frame.register(self.__host.address, self.__host)

    @property
    def dialect(self):
        return None

    def perform(self, _data=None):
        if _data is not None:
            self.__perform(_data)

    def __perform(self, _data):
        self.__rx_buffer += _data

        while self.__frame.check(self.__rx_buffer):
            command = self.__frame.deserialize(self.__frame.data)
            self.__rx_buffer = self.__rx_buffer[self.__frame.stop:]
            if 'address' in command:
                if command['address'] == self.__host.address:
                    if len(command['payload']) > 0:
                        hci_parser = RadarParser(command['payload'],
                                                 alias=self.__alias)
                        if hci_parser is not None:
                            output.show(data=hci_parser.__str__(),
                                        alias=self.__alias)
                            self.__auto_responser(hci_parser.get_command(),
                                                  self.__alias)

                            hci_command = hci_parser.get_command()
                            assert hci_command is not None, 'radar handler error: unknown command object'

                            from commander.storage.Storage import Storage
                            Storage.storage.variable = {
                                self.__alias.upper(): hci_command.fields,
                            }

                    else:
                        # commands without payload
                        pass

                elif command['address'] == self.__except.address:
                    message = ''.join(
                        '%02X' % byte for byte in command['payload']['data'])
                    output.show(data='crash@0x' + message,
                                alias=self.__alias, direction=':X', lf=' ')
                else:
                    message = command['payload']['msg'].__str__()
                    output.show(data=('%02X %02X ' %
                                      (command['address'],
                                       command['ctrl'])) + message,
                                alias=self.__alias, direction='??', lf=' ')
            else:
                # commands without address field
                pass

    def __auto_responser(self, _cmd, _alias):
        pass

    def run_cmd(self, _args):
        commander = RadarCommand()
        _command = commander.interpret(_args)
        if _command is not None:

            from commander.termbase.DisplayHandler import DisplayHandler
            DisplayHandler.display.enter()
            output.show(data=_command.__str__(),
                        alias=self.__alias,
                        direction='<=')
            DisplayHandler.display.exit()

            data_bytes = _command.sdu
            if len(data_bytes) > 0:
                frame_bytes = self.__frame.serialize(self.__host.address,
                                                     data_bytes)
                self.__port.send(frame_bytes)

    def response(self):
        while len(self.__input_queue):
            item = self.__input_queue.pop()

            assert item['alias'] == self.__alias, 'radar handler response error: handler alias (' + \
                self.__alias + ' != response alias ' + item['alias']

            self.run_cmd(item['command'])
