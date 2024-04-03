# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

def value_to_key(table, value):
    for k, v in table.items():
        if value == v:
            return k
    return None


def dict_to_type(_name, _dict):
    for key, value in _dict.items():
        if isinstance(value, type({})):
            _dict[key] = dict_to_type(key, value)
        elif isinstance(value, type([])):
            tmp_array = list()
            for item in value:
                if isinstance(item, type({})):
                    tmp_array.append(
                        dict_to_type(key+'_item', item))
                else:
                    tmp_array.append(item)
            _dict[key] = tmp_array

    return type(_name, (object, ), _dict)
