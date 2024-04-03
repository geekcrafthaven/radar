# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

def quit(_args=None):
    """
    quit commander terminal
    """

    try:
        from commander.termbase.TermBase import TermBase
        TermBase.termbase.cleanup()
        TermBase.termbase.quit_commander_tk()
    except Exception as msg:
        import commander.termbase as output
        output.show_error(str(msg))

    return True
