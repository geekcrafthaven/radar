# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

class ShortCut:

    KEY_MODIFIER = [
        "Alt",
        "Control",
        "Shift",
        "Any"
    ]

    KEY_TYPE = [
        "Button",
        "ButtonRelease",
        "Enter",
        "Leave",
        "KeyPress",
        "KeyRelease",
        "Motion",
        "MouseWheel"
    ]

    KEY_DETAIL = [
        "Insert",
        "Pause",
        "Print",
        "Scroll_Lock",
        "BackSpace",
        "Delete",
        "Down",
        "End",
        "Escape",
        "Home",
        "Left",
        "Linefeed",
        "Next",
        "Prior",
        "Return",
        "Right",
        "Tab",
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "KP_0",
        "KP_1",
        "KP_X",
        "KP_Add",
        "KP_Begin",
        "KP_Decimal",
        "KP_Delete",
        "KP_Divide",
        "KP_Down",
        "KP_End",
        "KP_Enter",
        "KP_Home",
        "KP_Insert",
        "KP_Left",
        "KP_Multiply",
        "KP_Next",
        "KP_Prior",
        "KP_Right",
        "KP_Subtract",
        "KP_Up"
    ]

    def __init__(self) -> None:
        self.__modifier = []
        self.__type = ''
        self.__detail = ''

        self.__value = ''

        self.__enabled = True
        self.__exclusive = True
        self.__execute = True

    def __str__(self):
        s = ''

        s += 'key    : %s\n' % self.key
        s += 'value  : %s\n' % self.value
        s += 'options:'
        s += ' enabled' if self.__enabled else ' disabled'
        s += ' exclusive' if self.__exclusive else ' additive'
        s += ' execute' if self.__execute else ' extensible'
        s += '\n'

        return s

    @property
    def key(self):
        result = ''

        for item in self.__modifier:
            if len(result) > 0:
                result += '-'
            result += item

        if len(self.__type) > 0:
            if len(result) > 0:
                result += '-'
            result += self.__type

        if len(self.__detail) > 0:
            if len(result) > 0:
                result += '-'
            result += self.__detail

        return '<' + result + '>'

    @property
    def value(self):
        return self.__value

    @property
    def enabled(self):
        return self.__enabled

    @property
    def exclusive(self):
        return self.__exclusive

    def is_equal(self, _mod, _type, _detail):
        if _type == self.__type:
            if _detail == self.__detail:
                if len(_mod) == len(self.__modifier):
                    for item in _mod:
                        if item not in self.__modifier:
                            return False
                    return True
        return False

    def parse(self, _short_cut_data):
        self.__enabled = True
        try:
            self.__enabled = _short_cut_data.options.enabled
        except:
            self.__enabled = True

        self.__exclusive = True
        try:
            self.__exclusive = _short_cut_data.options.exclusive
        except:
            self.__exclusive = True

        self.__execute = True
        try:
            self.__execute = _short_cut_data.options.execute
        except:
            self.__execute = True

        self.__value = ""
        try:
            self.__value = _short_cut_data.value
        except:
            pass

        self.__modifier = []
        try:
            modifier = _short_cut_data.key.modifier
            if isinstance(modifier, type("")):
                modifier = [modifier]

            if isinstance(modifier, type([])):
                for item in modifier:
                    assert item in ShortCut.KEY_MODIFIER, "modifier " + \
                        modifier + " not in modifiers list"
                    self.__modifier.append(item)
            else:
                raise Exception("unknown modifier type")

        except:
            pass

        self.__type = ''
        try:
            key_type = _short_cut_data.key.type
            assert key_type in ShortCut.KEY_TYPE, "key type " + \
                key_type + " not in key types list"
            self.__type = key_type

        except:
            pass

        self.__detail = ''
        try:
            detail = _short_cut_data.key.detail
            assert detail in ShortCut.KEY_DETAIL, "key detail " + \
                detail + " not in key details list"
            self.__detail = detail

        except:
            pass
