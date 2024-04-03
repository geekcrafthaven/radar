# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.utilities.ints import b2i


class Field:
    def __init__(self, _x0, _y0, _x1, _y1):
        self.__active = False
        self.__x0 = _x0
        self.__y0 = _y0
        self.__x1 = _x1
        self.__y1 = _y1

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, _value):
        self.__active = _value

    @property
    def x0(self):
        return self.__x0

    @x0.setter
    def x0(self, _value):
        self.__x0 = _value

    @property
    def y0(self):
        return self.__y0

    @y0.setter
    def y0(self, _value):
        self.__y0 = _value

    @property
    def x1(self):
        return self.__x1

    @x1.setter
    def x1(self, _value):
        self.__x1 = _value

    @property
    def y1(self):
        return self.__y1

    @y1.setter
    def y1(self, _value):
        self.__y1 = _value


class Fields:
    def __init__(self):
        self.__field = [Field(0,0,0,0), Field(0,0,0,0), Field(0,0,0,0)]

    @property
    def fields(self):
        return self.__field

    @property
    def field1(self):
        return self.__field[0]

    @property
    def field2(self):
        return self.__field[1]

    @property
    def field3(self):
        return self.__field[2]

    def set_active(self, _index, _value):
        if _index in [1, 2, 3]:
            self.__field[_index - 1].active(_value)


fields = Fields()


class Point:
    MAX_COUNTER = 33

    def __init__(self, _identifier=0xff, _x=0, _y=0):
        self.__identifier = _identifier
        self.__x = _x
        self.__y = _y
        self.__counter = Point.MAX_COUNTER

    @property
    def counter(self):
        return self.__counter

    @property
    def identifier(self):
        return self.__identifier

    @identifier.setter
    def identifier(self, _value):
        self.__identifier = _value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, _value):
        self.__x = _value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, _value):
        self.__y = _value

    def reset(self):
        self.__counter = Point.MAX_COUNTER

    def perform(self):
        self.__counter = 0 if self.__counter <= 1 else self.__counter - 1


class Pool:

    def __init__(self):
        self.__points = []

    @property
    def points(self):
        return self.__points

    def add(self, _point):
        found = False
        for item in self.__points:
            if item.x == _point.x and item.y == _point.y:
                found = True
                item.reset()
        if not found:
            self.__points.append(_point)

    def perform(self):
        tmp = self.__points
        self.__points = []
        for item in tmp:
            item.perform()

            if item.counter > 0:
                self.add(item)


pool = Pool()
