# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def save(cmd_line):
    """
    save current log

    syntax: 
        save FILENAME
    """

    if len(cmd_line) == 1:
        filename = cmd_line[0].strip()

        import commander
        filename = commander.normalize(filename)

        import os
        filename = os.path.expanduser(filename)
        if os.path.isfile(filename):
            output.show_error('save: file %s exists' % filename)
            return False
        else:
            logfile = open(filename, 'w')
            from commander.termbase.DisplayHandler import DisplayHandler
            logfile.write(DisplayHandler.display.text.get('1.0',
                                                          DisplayHandler.display.text.END))
            logfile.close()
            output.show_text('log saved into %s' % filename)
    else:
        output.show_error('syntax: save ' + ' '.join(cmd_line))
        output.show_doc(save)
        return False

    return True


def clean(_args=None):
    """
    clean current log

    syntax: 
        clean
    """

    from commander.termbase.DisplayHandler import DisplayHandler
    DisplayHandler.display.text.set_enabled(True)
    DisplayHandler.display.text.delete('1.0', DisplayHandler.display.text.END)
    DisplayHandler.display.text.set_enabled(False)
    DisplayHandler.display.text.update()

    return True
