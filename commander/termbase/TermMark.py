# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def mark(tag=None):
    """
    add a timestamp and an optional TAG to the output

    syntax: 
        mark [TAG]
    """

    def __time_line():
        import time
        tm = time.localtime(time.time())
        return '%02d:%02d:%02d' % (tm.tm_hour, tm.tm_min, tm.tm_sec)

    if tag is None:
        tag = 'MARK'
    elif isinstance(tag, type([])):
        if len(tag) > 0:
            tag = ' '.join(['%s' % item for item in tag])
        else:
            tag = 'MARK'
    elif isinstance(tag, type({})):
        tag = tag.__str__()

    date_str = '%s %s' % (__time_line(), tag)

    import commander
    date_str = commander.normalize(date_str)

    date_len = len(date_str)
    from commander.utilities.PrettyPrint import DLINE
    output.show_text(DLINE * date_len)
    output.show_text(date_str)
    output.show_text((DLINE * date_len) + '\n')

    return True
