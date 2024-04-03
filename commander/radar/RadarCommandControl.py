# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def baudrate(cmd_line):
    """
    radar port baudrate
    syntax:
        <ALIAS[, ALIAS[...]]|all> baudrate VALUE

    parameter:
        VALUE           0x002580	9600	(Standard)
                        0x004B00	19200	
                        0x009600	38400	
                        0x00E100	57600	
                        0x01C200	115200	
                        0x03E800	256000	    
    """

    try:
        from commander.radar.control.BaudrateReq import BaudrateReq

        if len(cmd_line) > 0:
            return BaudrateReq(cmd_line[0])
        output.show_error('not enough parameter')
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(baudrate)
    return None


def identity(cmd_line):
    """
    radar identity and firmware version

    syntax:
        <ALIAS[, ALIAS[...]]|all> identity
    """

    try:
        from commander.radar.control.IdentityReq import IdentityReq
        return IdentityReq()
    except Exception as msg:
        output.show_error(str(msg))

    output.show_doc(identity)
    return None


def reset(cmd_line):
    """
    radar firmware reset
    syntax:
        <ALIAS[, ALIAS[...]]|all> reset
    """

    try:
        from commander.radar.control.ResetReq import ResetReq
        return ResetReq()
    except Exception as msg:
        output.show_failure(msg)

    output.show_doc(reset)
    return None
