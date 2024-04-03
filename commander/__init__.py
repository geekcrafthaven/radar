# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT


def set_var(name, value):
    try:
        from commander.storage.Storage import Storage
        Storage.storage.set_value(name, value)
    except:
        print('set', name, value)


def is_var(name):
    result = False
    try:
        from commander.storage.Storage import Storage
        value = Storage.storage.is_defined(name)
        return value
    except:
        print('defined?', name, value)


def get_var(name):
    value = None
    try:
        from commander.storage.Storage import Storage
        value = Storage.storage.get_value(name)
        return value
    except:
        print('get', name, value)


def normalize(name):
    result = None
    try:
        from commander.storage.Storage import Storage
        result = Storage.storage.normalize(name)
        #print('normalize', name, result)
    except:
        result = name
    return result
