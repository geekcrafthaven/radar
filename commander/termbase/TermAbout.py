# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.config.Loader import Loader

import commander.termbase as output


def tool_name():
    return Loader.loader.config.commander.package.name


def tool_revision():
    return Loader.loader.config.commander.package.revision


def about(_args=None):
    """
        program info
    """

    from commander.utilities.PrettyPrint import HLINE, wd

    def copyright():
        ccr = HLINE * wd + '\n'
        ccr += Loader.loader.config.commander.package.name + '\n'
        ccr += Loader.loader.config.commander.package.info + '\n'
        ccr += '\n'
        ccr += Loader.loader.config.commander.package.copyright + ', '
        ccr += Loader.loader.config.commander.package.contact + '\n'
        ccr += HLINE * wd + '\n'

        output.show_text(ccr)

    def revision():
        ccr = HLINE * wd + '\n'
        ccr += '%s rev %s' % (tool_name(), tool_revision()) + '\n'
        ccr += HLINE * wd + '\n'

        output.show_text(ccr)

    copyright()
    revision()

    return True
