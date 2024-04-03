# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from threading import Lock


class SerLogger:
    """
    logger
    """

    def __init__(self):
        self.lock = Lock()

    def enter(self):
        self.lock.acquire()

    def exit(self):
        self.lock.release()
