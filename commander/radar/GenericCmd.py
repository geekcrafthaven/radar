# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


def get_value(type_definition, key):
    if key in type_definition.__dict__:
        return type_definition.__dict__[key]
    else:
        raise Exception('unknown value')


def get_key(type_definition, value):
    return [k for k, v in type_definition.__dict__.items() if v == value][0]


class GenericCmd(object):
    MAX_PAYLOAD_LEN = 32

    COMMANDS = {
        'BAUDRATE': (0x01),
        'IDENTITY': (0x09),
        'RESET': (0x0A),
        'AREA_DEFINE': (0x04),
        'AREA_REMOVE': (0x05),
        'AREA_READ': (0x06),
        'FORMAT_SET': (0x02),
        'FORMAT_GET': (0x03),
        'REPORT_POSITION': (0x07),
        'REPORT_AREA': (0x08),
    }

    RESULT = {
        'FAILURE': 0x00,
        'SUCCESS': 0x01,
    }

    FUNCTION = {
        'CLEAN': 0x08,
        'DISABLE': 0x03,
        'ENABLE': 0x02,
        'GET': 0x00,
        'OFF': 0x07,
        'ON': 0x06,
        'SET': 0x01,
        'START': 0x04,
        'STOP': 0x05,

        'CUSTOM': 0x80,
    }

    def __init__(self, command):
        value = GenericCmd.find_value(command, GenericCmd.COMMANDS)
        self.__command = GenericCmd.COMMANDS[value]

    @property
    def command(self):
        return self.__command

    @property
    def fields(self):
        return {
            'command': self.__command
        }

    @staticmethod
    def str_command(command, dictionary=COMMANDS):
        co = ''
        for v, k in dictionary.items():
            if k == command:
                co += v
                break
        return co

    @staticmethod
    def str_field(field, dictionary):
        co = ''
        for v, k in dictionary.items():
            # print v,k
            if k == field:
                co += v
                break
        return co

    @staticmethod
    def find_field(field, dictionary):
        for v, k in dictionary.items():
            if v == field:
                return v
        return None

    @staticmethod
    def find_value(var, dictionary):
        for k, v in dictionary.items():
            if v == var:
                return k
        return None
