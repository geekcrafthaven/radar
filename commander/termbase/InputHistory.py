# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import os


class InputHistory:
    """
    Store/Load some __command lines
    """

    DEFAULT_HISTORY_SIZE = 100

    def __init__(self, filename, pool_size=DEFAULT_HISTORY_SIZE):
        self.__filename = filename
        self.__pool_size = pool_size

        self.__history = []

        self.__cursor = len(self.__history)

    def create(self):
        history_file = open(self.__filename, 'w')
        history_file.close()

    def load(self):
        if not os.path.isfile(self.__filename):
            raise Exception('error: file %s not found' % self.__filename)

        history_file = open(self.__filename, 'r+')

        for line in history_file.readlines():
            line = line.strip()
            if len(line) > 0:
                self.append(line)

        history_file.close()

    def store(self):
        if not os.path.isfile(self.__filename):
            raise Exception('error: file %s not found' % self.__filename)

        history_file = open(self.__filename, 'w')

        for item in self.__history:
            item = item.strip()
            if len(item) > 0:
                history_file.write(item + '\n')

        history_file.close()

    def append(self, line):
        if len(self.__history) > 0 and self.__history[len(self.__history) - 1] == line:
            self.__cursor = len(self.__history)
            return

        self.__history.append(line)

        if len(self.__history) > self.__pool_size:
            self.__history.pop(0)

        self.__cursor = len(self.__history)

    def remember_prev(self):
        if self.__cursor < len(self.__history):
            if self.__cursor > 0:
                self.__cursor -= 1
            elif self.__cursor == 0:
                self.__cursor = 0
            result = self.__history[self.__cursor]
        else:
            if len(self.__history) > 0:
                self.__cursor = len(self.__history) - 1
                result = self.__history[self.__cursor]
            else:
                self.__cursor = len(self.__history)
                result = ''

        return result

    def remember_next(self):
        if self.__cursor < len(self.__history):
            self.__cursor += 1
            if self.__cursor < len(self.__history):
                result = self.__history[self.__cursor]
            else:
                result = ''
        else:
            self.__cursor = len(self.__history)
            result = ''

        return result
