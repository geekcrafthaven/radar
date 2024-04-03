# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


class RadarCommand:
    """
    create and send a HCI command
    """

    command_dict = dict()

    def __init__(self):
        pass

    def help(self):
        from commander.utilities.PrettyPrint import header

        output.show_text(header('Radar commands'))
        for key, value in RadarCommand.command_dict.items():
            output.show_text('%s' % key)
            output.show_doc(value)

    def interpret(self, cmd_line):
        if len(cmd_line) > 0:
            entered_cmd = cmd_line[0].lower().strip()

            if entered_cmd in RadarCommand.command_dict:
                return RadarCommand.command_dict[entered_cmd](cmd_line[1:])

            else:
                output.show_text('unknown radar command: %s' %
                                 (' '.join(entered_cmd)))

        return None
