# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.serialIo.SerialList import SerialList

import commander.termbase as output

termbase = None


class TermBase:
    """
    terminal base
    """
    command_dict = dict()

    def __init__(self):
        self.__input = None
        self.__serial_list = SerialList()

    def __del__(self):
        try:
            self.__serial_list.erase()
        except Exception as msg:
            output.show_error(str(msg))

    @property
    def serial_list(self):
        return self.__serial_list

    @property
    def aliaces(self):
        return self.__serial_list.serial.keys()

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, value):
        self.__input = value

    def cleanup(self):
        output.show_text('clean up... ')
        self.__serial_list.erase()
        output.show_done()

    def open_ports(self, _aliases_to_open):

        if len(_aliases_to_open) == 0:
            output.show_text('open ports: no aliases defined\n')
            return False

        for alias in _aliases_to_open:
            from commander.config import get_device
            device = get_device(alias)
            if device is not None:
                port = device.port
                port_device = port.device
                if not isinstance(port_device, type('')):
                    if 'serial' in dir(port_device):
                        port.device = 'serial:%s' % port_device.serial
                    elif 'vid' in dir(port_device):
                        port.device = '%04X:%04X' % (
                            int(port_device.vid.strip(' #0x'), 16),
                            int(port_device.pid.strip(' #0x'), 16))
                    else:
                        output.show_error(
                            'open ports: unsupported device definition ' + port_device.__str__())
                        return False

                parameter = device.parameter

                try:
                    if self.__serial_list.add(alias, port, parameter):
                        if 'color' in parameter.__dict__ and parameter.color is not None:
                            from commander.termbase.DisplayHandler import DisplayHandler
                            DisplayHandler.display.text.set_color(alias,
                                                                  parameter.color)
                        output.show_text('open ports: port %s opened' %
                                         alias)
                    else:
                        output.show_error('open ports: port "%s" could not be opened' %
                                          alias)
                        return False
                except Exception as message:
                    output.show_error('open ports error: %s' % message)
                    return False
            else:
                output.show_error('open ports: device %s not found in config.json' %
                                  alias)
                return False

            try:
                for item in device.storage:
                    import commander
                    commander.set_var(item.key, item.value)
            except:
                pass

        return True

    def interpret_cmd(self, data):
        try:
            import commander
            data = commander.normalize(data)

            data = data.strip()
            if data == '':
                return

            if ';' in data:
                data_array = data.split(';')
                for data_array_item in data_array:
                    if len(data_array_item) > 0:
                        if self.__interpret_cmd(data_array_item) is False:
                            return False
            else:
                return self.__interpret_cmd(data)

        except Exception as message:
            output.show_error('command interpreter: %s' % message)
            return False

    def __interpret_cmd(self, data):

        cmd_line = data.split()
        command = cmd_line[0].lower().strip()
        args = cmd_line[1:]

        if command in TermBase.command_dict:
            return TermBase.command_dict[command](args)

        else:
            try:
                output.show_text('%s\n' % data)
                alias = command.strip()
                aliases = list()
                if alias == 'all':
                    for item in self.aliaces:
                        aliases.append(item)
                elif ',' in alias:
                    aliases = alias.split(',')
                else:
                    aliases = [alias]

                for alias in aliases:
                    try:
                        port = self.__serial_list.serial[alias]
                        assert port is not None, 'error: port ' + alias + 'not found'

                        return port.handler.run_cmd(args)

                    except Exception as message:
                        message = 'interpret command "' + command + ' ' + \
                            ' '.join(args) + '" error:\n%s' % message
                        output.show_error(message)
                        return False

            except Exception as msg:
                output.show_warning(
                    'unknown terminal command: %s\n%s\n' % (data, msg))
                return False

        return True

    def start(self):
        from commander.termbase import TermAbout
        TermAbout.about(None)

        from commander.config.Loader import Loader
        if Loader.loader.config.setup.default is not None:
            for item in Loader.loader.config.setup.config:
                if item.name == Loader.loader.config.setup.default:
                    from commander.termbase import TermConfig
                    TermConfig.config([item.name])

    def perform(self):
        from commander.termbase.DisplayHandler import DisplayHandler
        DisplayHandler.display.update_output()

        for alias, port in self.__serial_list.serial.items():
            if port.handler is not None:
                port.handler.response()
