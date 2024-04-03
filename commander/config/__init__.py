# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.config.Loader import Loader


def reload():
    try:
        return Loader.loader.reload()
    except Exception as message:
        print(message)
        return []


def verbosity():
    try:
        return Loader.loader.config.commander.verbosity
    except Exception as message:
        print(message)
        return 0


def ignored_dirs():
    try:
        return Loader.loader.config.commander.path_excludes
    except Exception as message:
        print(message)
        return []


def library_path():
    try:
        return Loader.loader.config.commander.storage.library
    except Exception as message:
        print(message)
        return ''


def gallery_path():
    try:
        return Loader.loader.config.commander.storage.gallery
    except Exception as message:
        print(message)
        return ''


def calibration_path():
    try:
        return Loader.loader.config.commander.storage.calibration
    except Exception as message:
        print(message)
        return ''


def picture_filename():
    try:
        return Loader.loader.config.commander.storage.picture
    except Exception as message:
        print(message)
        return ''


def movie_filename():
    try:
        return Loader.loader.config.commander.storage.movie
    except Exception as message:
        print(message)
        return ''


def movie_coder():
    try:
        return Loader.loader.config.commander.storage.movie.codec
    except Exception as message:
        print(message)
        return ''


def station_list():
    option_list = []
    for station in Loader.loader.config.station:
        option_list.append(station.name)
    return option_list


def change_station(_station):
    for index in range(len(Loader.loader.config.station)):
        if Loader.loader.config.station[index].name == _station:
            Loader.current_station = index


def current_station_name():
    try:
        return Loader.loader.config.station[Loader.current_station].name
    except Exception as message:
        print(message)
        Loader.current_station = 0
        return Loader.loader.config.station[Loader.current_station].name


def picture_config():
    def __return_value():
        return Loader.loader.config.station[Loader.current_station].camera.picture
    try:
        reload()
        return __return_value()
    except Exception as message:
        print(message)
        Loader.current_station = 0
        return __return_value()


def movie_config():
    def __return_value():
        return Loader.loader.config.station[Loader.current_station].camera.movie
    try:
        return __return_value()
    except Exception as message:
        print(message)
        Loader.current_station = 0
        return __return_value()


def frame_buffer_config():
    def __return_value():
        return Loader.loader.config.station[Loader.current_station].camera.frame_buffer
    try:
        reload()
        return __return_value()
    except Exception as message:
        print(message)
        Loader.current_station = 0
        return __return_value()


def postprocess_config():
    def __return_value():
        return Loader.loader.config.station[Loader.current_station].camera.post_process
    try:
        return __return_value()
    except Exception as message:
        print(message)
        Loader.current_station = 0
        return __return_value()


def calibration_config():
    def __return_value():
        return Loader.loader.config.station[Loader.current_station].camera.calibration
    try:
        reload()
        return __return_value()
    except Exception as message:
        print(message)
        Loader.current_station = 0
        return __return_value()


def permissions_config():
    def __return_value():
        return Loader.loader.config.station[Loader.current_station].camera.permissions
    try:
        return __return_value()
    except Exception as message:
        print(message)
        Loader.current_station = 0
        return __return_value()


def database_name():
    try:
        return Loader.loader.config.commander.database.name
    except Exception as message:
        print(message)
        return 'commander'


def database_host():
    try:
        return Loader.loader.config.commander.database.host
    except Exception as message:
        print(message)
        return 'localhost'


def database_port():
    try:
        return Loader.loader.config.commander.database.port
    except Exception as message:
        print(message)
        return '3306'


def database_user():
    try:
        return Loader.loader.config.commander.database.user
    except Exception as message:
        print(message)
        return 'pi'


def database_password():
    try:
        return Loader.loader.config.commander.database.password
    except Exception as message:
        print(message)
        return ''


def get_device(_alias):
    for device in Loader.loader.config.setup.devices:
        if _alias == device.alias:
            return device
    return None


def pre_open():
    if Loader.loader.config.setup.default is not None:
        for item in Loader.loader.config.setup.config:
            if item.name == Loader.loader.config.setup.default:
                return item.aliases
    else:
        return []


def get_shortcuts():
    if Loader.loader.config.commander.shortcut is not None:
        result = []
        for item in Loader.loader.config.commander.shortcut:
            from commander.config.ShortCut import ShortCut
            new_short_cut = ShortCut()
            new_short_cut.parse(item)
            result.append(new_short_cut)

        return result
    else:
        return []


def setup_configs():
    return Loader.loader.config.setup.config


def setup_default():
    return Loader.loader.config.setup.default


def font_color():
    try:
        return Loader.loader.config.commander.appearance.font
    except:
        return "#070707"


def signal_color():
    try:
        return Loader.loader.config.commander.appearance.signal
    except:
        return "#ff0000"


def done_color():
    try:
        return Loader.loader.config.commander.appearance.done
    except:
        return "#007f00"


def emphasis_color():
    try:
        return Loader.loader.config.commander.appearance.emphasis
    except:
        return "#0000ff"


def positiv_color():
    try:
        return Loader.loader.config.commander.appearance.positiv
    except:
        return "#011f01"


def negativ_color():
    try:
        return Loader.loader.config.commander.appearance.negativ
    except:
        return "#1f0101"
