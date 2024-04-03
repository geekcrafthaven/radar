# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander

from commander.termbase import TermStorage
from commander.termbase import TermLog
from commander.termbase import TermPorts
from commander.termbase import TermConfig
from commander.termbase import TermDirectory
from commander.termbase import TermMark
from commander.termbase import TermQuit
from commander.termbase import TermAbout
from commander.termbase import TermHelp
from commander.termbase.TermBase import TermBase
from commander.config import done_color, positiv_color, negativ_color, signal_color

TermBase.command_dict['help'] = TermHelp.help
TermBase.command_dict['about'] = TermAbout.about
TermBase.command_dict['quit'] = TermQuit.quit
TermBase.command_dict['mark'] = TermMark.mark
TermBase.command_dict['dir'] = TermDirectory.dir
TermBase.command_dict['config'] = TermConfig.config
TermBase.command_dict['open'] = TermPorts.open
TermBase.command_dict['close'] = TermPorts.close
TermBase.command_dict['list'] = TermPorts.list
TermBase.command_dict['save'] = TermLog.save
TermBase.command_dict['clean'] = TermLog.clean
TermBase.command_dict['storage'] = TermStorage.storage
TermBase.command_dict['ans'] = TermStorage.response

global show, show_text, show_done, show_warning, show_error, show_success, show_failure, show_doc


def show(data, alias, direction='=>', lf='\n  '):
    def __time_line():
        import time
        tm = time.localtime(time.time())
        return '%02d:%02d:%02d' % (tm.tm_hour, tm.tm_min, tm.tm_sec)

    if len(data) > 0:
        if isinstance(data, type(b'')):
            data = data.decode()

        from commander.termbase.DisplayHandler import DisplayHandler
        entry = DisplayHandler.OutputEntry(data,
                                           alias=alias,
                                           current_time=__time_line(),
                                           direction=direction,
                                           lf=lf)
        DisplayHandler.display.queue.append(entry)


def show_text(data, _color=None, _timestamp=None, _service=None, _lf=None):
    if len(data) > 0:
        if isinstance(data, type(b'')):
            data = data.decode()

        if _timestamp is not None:
            data = '${DATE} ${TIME} ' + data
        if _service is not None:
            if isinstance(_service, type('')):
                data += _service + ' ' + data
            elif isinstance(_service, type([])):
                data += ' '.join(['%s' %
                                 item for item in _service]) + ' ' + data
            else:
                data += _service.__str__() + ' ' + data

        data = commander.normalize(data)

        from commander.termbase.DisplayHandler import DisplayHandler
        entry = DisplayHandler.OutputEntry(data,
                                           color=_color,
                                           lf=_lf)
        DisplayHandler.display.queue.append(entry)


def show_done(message=None):
    if message is None:
        commander.termbase.show_text('done', _color=done_color())
    else:
        commander.termbase.show_text('done: ' + message, _color=done_color())


def show_warning(data):
    show_text('warning: ' + data, _color=signal_color())


def show_error(data):
    show_text('error: ' + data, _timestamp=True, _color=signal_color())


def show_success():
    show_text('success', _color=positiv_color())


def show_failure():
    show_text('failure', _color=negativ_color())


def show_doc(entity):
    from commander.utilities.PrettyPrint import doctrim
    commander.termbase.show_text(doctrim(entity.__doc__))
