#!/bin/bash

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

venv_path=.venv

if [ -d "${venv_path}" ]; then
    echo "venv ${venv_path} exists"
else
    python3 -m venv $venv_path
    if [ $? -ne 0 ]; then
        echo "error: cant create venv ${venv_path}"
        popd
        exit
    else
        . $venv_path/bin/activate && python3 -m pip install --upgrade pip && python3 -m pip install -r res/requirements.txt && deactivate
    fi
fi

. $venv_path/bin/activate && python3 -m commander
deactivate
