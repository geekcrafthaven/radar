# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

if __name__ == '__main__':
    import sys

    from commander.config.Loader import Loader
    Loader.loader = Loader()

    from commander.termbase.DisplayHandler import DisplayHandler
    DisplayHandler.display = DisplayHandler()

    from commander.storage.Storage import Storage
    Storage.storage = Storage()

    from commander.termbase.TermBase import TermBase
    TermBase.termbase = TermBase()

    if len(sys.argv) == 1:
        try:
            from commander.start import CommanderTk
            commander = CommanderTk()
            commander.start()
            commander.mainloop()
        except Exception as message:
            print(message)
    else:
        command = ' '.join(sys.argv[1:])
        print('call commander with ' + command)
        from commander.termbase.DisplayHandler import DisplayHandler
        assert DisplayHandler.display is not None, 'commander start error: display not set'
        from commander.start import PlainText
        DisplayHandler.display.text = PlainText()

        TermBase.termbase.start()
        TermBase.termbase.interpret_cmd(command)

        while True:
            from commander.termbase.TermBase import TermBase
            TermBase.termbase.perform()
            from time import sleep
            sleep(0.1)

            if len(DisplayHandler.display.queue) == 0:
                break

        TermBase.termbase.cleanup()
