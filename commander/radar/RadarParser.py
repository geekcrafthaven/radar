# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.GenericCmd import GenericCmd
from commander.radar.feature.FormatGetCfm import FormatGetCfm
from commander.radar.feature.PointsPool import Point
from commander.utilities.PrettyPrint import VDELIM

from commander.radar.control.BaudrateCfm import BaudrateCfm
from commander.radar.control.IdentityCfm import IdentityCfm
from commander.radar.control.ResetCfm import ResetCfm

from commander.radar.feature.AreaDefineCfm import AreaDefineCfm
from commander.radar.feature.AreaRemoveCfm import AreaRemoveCfm
from commander.radar.feature.AreaReadCfm import AreaReadCfm
from commander.radar.feature.FormatSetCfm import FormatSetCfm
from commander.radar.feature.ReportPositionInd import ReportPositionInd
from commander.radar.feature.ReportAreaInd import ReportAreaInd
from commander.utilities.ints import b2i


def check_command(_command, _payload):
    if _command == GenericCmd.COMMANDS['IDENTITY']:
        return IdentityCfm(_payload)
    elif _command == GenericCmd.COMMANDS['RESET']:
        return ResetCfm(_payload)
    elif _command == GenericCmd.COMMANDS['AREA_DEFINE']:
        fields = AreaDefineCfm(_payload)
        return fields
    elif _command == GenericCmd.COMMANDS['AREA_REMOVE']:
        return AreaRemoveCfm(_payload)
    elif _command == GenericCmd.COMMANDS['AREA_READ']:
        from commander.radar.feature.PointsPool import fields
        areas = AreaReadCfm(_payload)

        fields.field1.x0 = -b2i(areas.area_1.br[0])*10
        fields.field1.y0 = areas.area_1.br[1]*10
        fields.field1.x1 = -b2i(areas.area_1.tl[0])*10
        fields.field1.y1 = areas.area_1.tl[1]*10

        fields.field2.x0 = -b2i(areas.area_2.br[0])*10
        fields.field2.y0 = areas.area_2.br[1]*10
        fields.field2.x1 = -b2i(areas.area_2.tl[0])*10
        fields.field2.y1 = areas.area_2.tl[1]*10

        fields.field3.x0 = -b2i(areas.area_3.br[0])*10
        fields.field3.y0 = areas.area_3.br[1]*10
        fields.field3.x1 = -b2i(areas.area_3.tl[0])*10
        fields.field3.y1 = areas.area_3.tl[1]*10

        return areas
    elif _command == GenericCmd.COMMANDS['BAUDRATE']:
        return BaudrateCfm(_payload)
    elif _command == GenericCmd.COMMANDS['FORMAT_SET']:
        return FormatSetCfm(_payload)
    elif _command == GenericCmd.COMMANDS['FORMAT_GET']:
        return FormatGetCfm(_payload)
    elif _command == GenericCmd.COMMANDS['REPORT_POSITION']:
        position = ReportPositionInd(_payload)
        from commander.radar.feature.PointsPool import pool

        x = -b2i(position.first[0])*10
        y = b2i(position.first[1])*10

        point = Point(1, x, y)
        if point.x != 0 and point.y != 0:
            pool.add(point)

        x = -b2i(position.second[0])*10
        y = b2i(position.second[1])*10

        point = Point(2, x, y)
        if point.x != 0 and point.y != 0:
            pool.add(point)

        return position
    elif _command == GenericCmd.COMMANDS['REPORT_AREA']:
        from commander.radar.feature.PointsPool import fields

        area = ReportAreaInd(_payload)
        if area.area_1 == 1:
            fields.field1.active = True
        else:
            fields.field1.active = False

        if area.area_2 == 1:
            fields.field2.active = True
        else:
            fields.field2.active = False

        if area.area_3 == 1:
            fields.field3.active = True
        else:
            fields.field3.active = False

        return area
    return None


class RadarParser(GenericCmd):
    """
    messages factory
    """

    report_enabled = False

    def __init__(self, payload, alias=None):
        GenericCmd.__init__(self, payload[0])

        self.__alias = alias

        if len(payload[1]) == 0:
            print('payload empty')
            payload[1] = []

        self.__payload = payload
        self.__command = payload[0]
        self.__data = payload[1][0:]
        self.command_obj = check_command(self.__command,
                                         self.__payload)

    @property
    def data(self):
        return self.__data

    def get_command(self):
        return self.command_obj

    def __str__(self):
        if self.command_obj is not None:
            s = self.command_obj.__str__()

        else:
            # emergency solution: command is unknown, print bytes
            s = ''
            s += '%-20s%c %02X %s\n' % ('command', VDELIM,
                                        self.__command, self.str_command(self.__command))
            if len(self.__data) > 0:
                s += '%-20s%c %s' % ('data', VDELIM,
                                     ''.join('%02X ' % self.__data[i] for i in range(0, len(self.__data))))

        return s
