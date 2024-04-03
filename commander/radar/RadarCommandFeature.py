# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def area(cmd_line):
    """
    control region filter

    syntax:
        <ALIAS[, ALIAS[...]]|all> area define ID TYPE CORNER
        <ALIAS[, ALIAS[...]]|all> area remove ID
        <ALIAS[, ALIAS[...]]|all> area read

    parameter:
        ID              area identifier 1,2 or 3
        CORNER          four area corners, x and y, signed byte, in cm
        TYPE            0: detect, 1: ignore
    """


    command = cmd_line[0].lower().strip()
    payload = cmd_line[1:]
    try:
        from commander.radar.feature.AreaDefineReq import AreaDefineReq
        from commander.radar.feature.AreaRemoveReq import AreaRemoveReq
        from commander.radar.feature.AreaReadReq import AreaReadReq

        if command == 'define':
            if len(payload) > 0:
                return AreaDefineReq(*payload)
        elif command == 'remove':
            if len(payload) > 0:
                return AreaRemoveReq(*payload)
        elif command == 'read':
            return AreaReadReq()

        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(area)
    return None


def format(cmd_line):
    """
    control radar report format

    syntax:
        <ALIAS[, ALIAS[...]]|all> format set MODE
        <ALIAS[, ALIAS[...]]|all> format get

    parameter:
        MODE            1: position, 2: area, 3: combo 
    """


    command = cmd_line[0].lower().strip()
    payload = cmd_line[1:]
    try:
        from commander.radar.feature.FormatSetReq import FormatSetReq
        from commander.radar.feature.FormatGetReq import FormatGetReq

        if command == 'set':
            if len(payload) > 0:
                return FormatSetReq(*payload)
        elif command == 'get':
            return FormatGetReq()

        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(format)
    return None

def report(cmd_line):
    """
    control report 

    syntax:
        <ALIAS[, ALIAS[...]]|all> report <ignore|show>
    """

    from commander.radar.RadarParser import RadarParser
    command = cmd_line[0].lower().strip()
    if command == 'ignore':
        RadarParser.report_enabled = False
    elif command == 'show':
        RadarParser.report_enabled = True
    else:
        output.show_error('wrong parameter')
        output.show_doc(report)

    return None
