# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def help(cmd_line):
    """
    commander help

    syntax: 
        help                        terminal help
        help radar                  radar commands
    """

    from commander.termbase import TermAbout
    TermAbout.tool_revision()

    def __usage_line(cmd, comment):
        output.show_text(cmd)
        output.show_doc(comment)

    from commander.termbase.TermBase import TermBase
    if len(cmd_line) == 0:
        from commander.utilities.PrettyPrint import header
        output.show_text(header('internal commands'))

        for key, value in TermBase.command_dict.items():
            __usage_line(key, value)

    else:
        cmd_line_0 = cmd_line[0].lower()

        if cmd_line_0 == 'hci':
            pass
            #from commander.hci.HciCommand import HciCommand
            #HciCommand().help()
        elif cmd_line_0 == 'radar':
            from commander.radar.RadarCommand import RadarCommand
            RadarCommand().help()
        else:
            if cmd_line_0 in TermBase.command_dict:
                __usage_line(cmd_line_0, TermBase.command_dict[cmd_line_0])
            else:
                output.show_error('help error: unknown command ' + cmd_line_0)
                return False

    return True
