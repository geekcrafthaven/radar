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
        self.__field = [Field(0, 0, 0, 0), Field(
            0, 0, 0, 0), Field(0, 0, 0, 0)]

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
    def __init__(self, _identifier=0xff, _x=0, _y=0):
        self.__identifier = _identifier
        self.__x = _x
        self.__y = _y
        self.__weight = 1

    @property
    def weight(self):
        return self.__weight

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
        self.__weight = 1

    def perform(self):
        self.__weight = 0 if self.__weight < 0.01 else self.__weight * 0.95


class Pool:
    def __init__(self):
        self.__points = []
        self.__x = 0
        self.__y = 0
        self.__w = 0

    @property
    def points(self):
        return self.__points

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def w(self):
        return self.__w

    def add(self, _point):
        found = False
        for item in self.__points:
            if item.x == _point.x and item.y == _point.y:
                found = True
                item.reset()
        if not found:
            self.__points.append(_point)

    def __weight_point(self, _cluster):
        weight = 0
        x_weight = 0
        y_weight = 0
        for item in _cluster:
            weight += item.weight
            x_weight += item.x * item.weight
            y_weight += item.y * item.weight
        if weight > 0:
            x = x_weight / weight
            y = y_weight / weight
            w = weight
        else:
            x = 0
            y = 0
            w = 0
        return (x, y, w)

    def perform(self):
        tmp = self.__points
        self.__points = []
        for item in tmp:
            item.perform()

            if item.weight > 0:
                self.add(item)

        (x, y, w) = self.__weight_point(self.__points)
        if w > 0:
            self.__x = x
            self.__y = y
            self.__w = w
        else:
            self.__x = 0
            self.__y = 0
            self.__w = 0


class Cluster:
    def __init__(self):
        self.__clusters = {}

    def add(self, _point):
        # if len(self.__cluster) == 0:
        #    pass
        # else:
        #    pass
        pass

    def perform(self):
        for item in self.__clusters:
            item.perform()



pool = Pool()
