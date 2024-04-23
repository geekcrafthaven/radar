# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


try:
    from tkinter import Canvas
    from tkinter import Toplevel
except Exception as msg:
    print('commander error: import tkinter: %s' % msg)
    import sys
    sys.exit(1)


class RadarMap:
    POINT_SIZE = 5
    CLUSTER_SIZE = 10

    def __init__(self, _parent):
        self.__width = 400
        self.__height = 400

        win = Toplevel(_parent)
        win.geometry("%dx%d" % (self.width, self. height))
        win.title('map')

        # my_str1 = StringVar()
        # l1 = Label(win,  textvariable=my_str1)
        # l1.grid(row=1, column=2)
        # my_str1.set("Hi I am Child window")

        self.__map = Canvas(win,
                            width=self.width,
                            height=self.height)

        self.__map.bind("<Configure>", self.on_resize)

        self.__map.pack()

        # y = int(200 / 2)
        # self.w.create_line(0, y, 200, y, fill="#476042")

        # win.overrideredirect(1)  # No win decoration.
        # win.bd = 10
        # Frame.__init__(self, win, relief=GROOVE)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        # wscale = float(event.width)/self.width
        # hscale = float(event.height)/self.height
        self.__width = event.width
        self.__height = event.height
        # resize the canvas
        self.__map.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        # self.w.scale("all", 0, 0, wscale, hscale)
        self.__map.pack()

    def draw_points(self):
        from commander.map.PointsPool import pool
        from commander.map.PointsPool import fields
        from commander.map.PointsPool import Point

        self.__map.delete('all')

        self.__map.create_rectangle(1, 1, self.width, self.height,
                                    fill='#000000', outline='red', width=2)

        area_id = 0
        for item in fields.fields:
            if item.active:
                fill_color = '#3f3f3f'
            else:
                fill_color = '#000000'
            self.__map.create_rectangle((item.x0 + self.width/2), item.y0,
                                        (item.x1 + self.width/2), item.y1,
                                        fill=fill_color, outline='yellow', width=2)
            self.__map.create_text(item.x0 + self.width/2 + RadarMap.POINT_SIZE,
                                   item.y0 + RadarMap.POINT_SIZE,
                                   text='%d' % area_id, fill='yellow')
            area_id += 1

        for item in pool.points:
            x0 = (item.x+self.width/2) - RadarMap.POINT_SIZE
            y0 = (item.y) - RadarMap.POINT_SIZE
            x1 = (item.x+self.width/2) + RadarMap.POINT_SIZE
            y1 = (item.y) + RadarMap.POINT_SIZE
            color = int(0xff * item.weight)
            self.__map.create_oval(x0, y0,
                                   x1, y1,
                                   fill='#0000%02X' % color, outline=None)
            self.__map.create_text(x0 + RadarMap.POINT_SIZE,
                                   y0 + RadarMap.POINT_SIZE,
                                   text='%d' % item.identifier, fill='yellow')

        x = pool.x+self.width/2
        y = pool.y
        x0 = x - RadarMap.CLUSTER_SIZE
        y0 = y - RadarMap.CLUSTER_SIZE
        x1 = x + RadarMap.CLUSTER_SIZE
        y1 = y + RadarMap.CLUSTER_SIZE
        color = int(0xff)
        self.__map.create_oval(x0, y0,
                               x1, y1,
                               fill='#%02x%02x00' % (color, color), outline=None)

        self.__map.pack()
