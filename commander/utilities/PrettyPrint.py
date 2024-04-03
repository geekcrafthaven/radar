# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

wd = 80
sp = 15

HLINE = '*'

DLINE = '='
# DLINE = chr(205)

SLINE = '-'
# SLINE = chr(196)

CLINE = '~'

# VDELIM = ' '
VDELIM = '|'
# VDELIM = chr(179)

DNCON = '+'
# DNCON = chr(194)

UPCON = '+'
# UPCON = chr(193)

CRCON = '+'
# CRCON = chr(197)

tabspace = 0


def sr():
    global tabspace
    tabspace += 4
    return ' ' * tabspace


def sl():
    global tabspace
    tabspace = (tabspace - 4) if tabspace > 4 else 0
    return ' ' * tabspace


def sc():
    global tabspace
    return ' ' * tabspace


def header(comment):
    s = DLINE * wd + '\n'
    s += comment + '\n'
    s += SLINE * wd
    return s


def doctrim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = 0xffff
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < 0xffff:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:

    return '    ' + '\n    '.join(trimmed)
