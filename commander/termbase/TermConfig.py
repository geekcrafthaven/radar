# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def config(cmd_line):
    """
    config load configuration
    called without parameter print configurations list

    syntax:
        config [CONFIGURATION]

    note: call "close all" to start with a clean slate
    """

    from commander.config import setup_configs, get_device, setup_default, reload, change_station
    if len(cmd_line) == 0:
        from commander.utilities.PrettyPrint import SLINE, wd, header
        output.show_text(header('available configurations\n' + '%-20s %-20s %-s' %
                                ('name', 'station', 'aliases')))
        for item in setup_configs():
            result = '%-20s %-20s ' % (item.name, item.station)
            start_at = 42
            for alias in item.aliases:
                if start_at == 0:
                    result = ' ' * 42
                result += '%-10s' % alias + ' '

                device = get_device(alias).port.device
                if isinstance(device, type('')):
                    result += device
                elif 'serial' in dir(device):
                    result += 'serial:%s' % device.serial
                elif 'vid' in dir(device):
                    result += '%04X:%04X' % (
                        int(device.vid.strip(' #0x'), 16),
                        int(device.pid.strip(' #0x'), 16))
                else:
                    result += 'unsupported device definition'

                output.show_text('%-s' % result)
                start_at = 0

                try:
                    for item in device.storage:
                        import commander
                        commander.set_var(item.key, item.value)
                except:
                    pass

        output.show_text(SLINE * wd)
        output.show_text('default: %s' % setup_default())
        output.show_text(SLINE * wd)
    else:
        reload()
        for item in cmd_line:
            item = item.lower()

            found_flag = False
            for setup in setup_configs():
                if setup.name == item:
                    output.show_text('open ' + item +
                                     ' with aliases: ' +
                                     ', '.join(setup.aliases))

                    output.show_text('change station to ' +
                                     setup.station)
                    change_station(setup.station)

                    from commander.termbase.TermBase import TermBase
                    return TermBase.termbase.open_ports(setup.aliases)

            output.show_error('config: configuration ' + item + ' not found')
            output.show_doc(commander.config)
            return False

    return True
