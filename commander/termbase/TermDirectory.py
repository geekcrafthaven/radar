# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def dir(cmd_line):
    """
    print directory

    syntax: 
        dir [DIRECTORY]
    """

    if len(cmd_line) == 0:
        cmd_line.append('.')

    import os
    for item in cmd_line:
        item = os.path.expanduser(item)
        if os.path.isdir(item):
            output.show_text(item)
            for cur, _dirs, files in os.walk(item):
                if cur != item:
                    break
                for f in sorted(files + _dirs):
                    output.show_text(os.path.abspath(os.path.join(cur, f)))

        else:
            output.show_error('syntax error: dir ' + ' '.join(cmd_line))
            output.show_text('directory ' + ' '.join(cmd_line) + ' not found')
            output.show_doc(dir)

    return True
