# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def open(cmd_line):
    """
    open serial connection

    syntax: 
        open all
        open <PORT [alias ALIAS] [color NAME|#RRGGBB] [interpreter hci|scpi DIALECT]>

    default PORT is a device name.
    extended PORT syntax: 
        serial:NUMBER                   NUMBER is a valid usb device serial number
        pid:vid                         pid and vid are hex values like 0122:1C27 for ProfiTest

    color: a color name like red, green, blue etc. or hex values for RR, GG, BB

    default alias: port identifier
    default interpreter: hci
    """

    def search_for_parameter(parameter, command, default_value):
        if parameter in command:
            for index in range(len(command)-1):
                if command[index] == parameter:
                    index += 1
                    if index < len(command):
                        return command[index]
        date_str = 'open: set default value for "%s": %s' % (
            parameter, default_value)
        output.show_text(date_str)
        return default_value

    import commander.config as config
    config.reload()
    if len(cmd_line) > 0:
        port = cmd_line[0].strip()

        alias = search_for_parameter('alias', cmd_line, port.replace(':', '_'))

        from commander.termbase.TermBase import TermBase
        try:
            if port == 'all':
                config_aliases_to_open = config.pre_open()
                return TermBase.termbase.open_ports(config_aliases_to_open)
            else:
                parameter = {}
                parameter['color'] = search_for_parameter('color',
                                                          cmd_line, None)
                parameter['interpreter'] = search_for_parameter('interpreter',
                                                                cmd_line, 'hci').lower()

                from commander.serialIo.threaded.SerialPortThreaded import SerialPortThreaded
                if parameter['interpreter'] == 'scpi':
                    parameter['dialect'] = cmd_line[-1].lower()

                from commander.utilities.dict_tweaks import dict_to_type
                parameter = dict_to_type('parameter', parameter)
                device = dict_to_type('device', {'device': port,
                                                 'baudrate': 115200})

                if TermBase.termbase.serial_list.add(alias, device, parameter):
                    if parameter.color is not None:
                        from commander.termbase.DisplayHandler import DisplayHandler
                        DisplayHandler.display.text.set_color(alias,
                                                              parameter.color)
                    output.show_text('open: port %s opened\n' %
                                     alias)
                else:
                    output.show_text('open: port %s could not be opened\n' %
                                     alias)
                    return False
        except Exception as msg:
            output.show_error(str(msg))
            return False
    else:
        output.show_error('syntax: open ' + ' '.join(cmd_line))
        output.show_doc(open)
        return False

    return True


def close(cmd_line):
    """
    close serial port

    syntax: 
        close <ALIAS[,ALIAS]|all>       close post(s)
        close                           like "close all"               
    """

    from commander.termbase.TermBase import TermBase
    if len(cmd_line) == 0:
        cmd_line.append('all')

    if len(cmd_line) == 1:
        try:
            alias = cmd_line[0].strip()
            if alias.lower() == 'all':
                portlist = TermBase.termbase.serial_list.serial.copy()
                if len(portlist) == 0:
                    output.show_text('close: no open ports\n')
                else:
                    for name in portlist:
                        TermBase.termbase.serial_list.remove(name)
                        output.show_text('port %s closed\n' % name)
            elif TermBase.termbase.serial_list.has_port(alias):
                TermBase.termbase.serial_list.remove(alias)
                output.show_text('port %s closed\n' % alias)
            else:
                output.show_error('close port: unknown port: %s\n' % alias)
        except Exception as msg:
            output.show_error('close port: %s\n' % msg)
            return False
    else:
        output.show_error('syntax: close ' + ' '.join(cmd_line))
        output.show_doc(close)
        return False

    return True


def list(cmd_line):
    """
    list used and available devices (serial ports)

    syntax: 
        list                            usb devices 
        list DEVICE                     device info
    """

    from commander.termbase.TermBase import TermBase

    if len(cmd_line) == 0:
        serial_list = TermBase.termbase.serial_list.__str__()
        output.show_text(serial_list)
    else:
        for device in cmd_line:
            device = device.strip()
            info = TermBase.termbase.serial_list.get_device_info(device)

            if info is None:
                output.show_error('device %s unknown' % device)
                return False
            else:
                from commander.utilities.PrettyPrint import SLINE, wd, header

                output.show_text(header('%-15s %s' %
                                        ('field', 'value')))
                output.show_text('%-15s %s' %
                                 ('device', device))
                for key, value in info.items():
                    output.show_text('%-15s %s' % (key, value))

                output.show_text(SLINE * wd)
    return True
