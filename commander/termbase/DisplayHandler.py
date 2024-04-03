# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


from commander.serialIo.threaded.SerLogger import SerLogger

display = None


class DisplayHandler(SerLogger):
    class OutputEntry:
        def __init__(self, data, alias=False, color=None, current_time=None, direction='=>', lf='\n\t'):
            self.data = data
            self.alias = alias
            self.color = color
            self.time = current_time
            self.dir = direction
            self.lf = lf

    def __init__(self):
        SerLogger.__init__(self)

        self.__text = None
        self.__output_queue = list()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

    @property
    def queue(self):
        return self.__output_queue

    def update_output(self):
        while len(self.__output_queue):
            self.enter()
            entry = self.__output_queue.pop(0)
            self.text.set_enabled(True)
            if entry.alias:
                self.text.insert(self.text.END,
                                 entry.alias + ' ' + entry.dir + ' @' + entry.time + entry.lf, entry.alias)
                self.text.insert(self.text.END,
                                 entry.data.replace('\n', entry.lf) + entry.lf + '\n', entry.alias)
            elif entry.color is not None:
                self.text.set_color('%s' % entry.color, entry.color)
                lf = entry.lf if entry.lf is not None else '\n'
                self.text.insert(self.text.END,
                                 entry.data + lf, '%s' % entry.color)
            else:
                lf = entry.lf if entry.lf is not None else '\n'
                self.text.insert(self.text.END,
                                 entry.data + lf, 'internal')
            self.text.seek(self.text.END)
            self.text.set_enabled(False)
            self.exit()
