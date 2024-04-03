# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.radar.RadarCommand import RadarCommand
from commander.radar import RadarCommandControl
from commander.radar import RadarCommandFeature

RadarCommand.command_dict['baudrate'] = RadarCommandControl.baudrate
RadarCommand.command_dict['identity'] = RadarCommandControl.identity
RadarCommand.command_dict['reset'] = RadarCommandControl.reset
RadarCommand.command_dict['area'] = RadarCommandFeature.area
RadarCommand.command_dict['format'] = RadarCommandFeature.format
RadarCommand.command_dict['report'] = RadarCommandFeature.report
