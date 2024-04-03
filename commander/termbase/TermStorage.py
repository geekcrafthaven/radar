# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


def response(cmd_line):
    """
    user response handling

    syntax:
        ans VARIABLE VALUE
    """

    def help_on_error():
        output.show_error('syntax error: ans ' + ' '.join(cmd_line))
        output.show_doc(response)

    def storage_set(_name, _value):
        import commander
        _value = commander.normalize(_value)
        if commander.is_var(_name):
            commander.set_var(_name, _value)
            output.show_text('set %s to %s' %
                             (_name, _value))
        else:
            output.show_text('request %s unknown' % _name)
            return False

        return True

    if len(cmd_line) > 1:
        return storage_set(cmd_line[0].upper(), ' '.join(cmd_line[1:]))
    else:
        help_on_error()
        return False

    return True


def storage(cmd_line):
    """
    handle variables

    syntax:
        storage [list]                      storage content
        storage env                         representation for expression evalueation
        storage clean [NAME]                clean up storage content
        storage save FULL_FILE_NAME         store current storage content
        storage commit FULL_FILE_NAME       store added/changed variables content (keep unchanged)   
        storage load FULL_FILE_NAME         load (update) content 
        storage get NAME                    get value by key
        storage set NAME VALUE              set value by key

    default value for FULL_FILE_NAME is storage.json
    """

    import commander
    from commander.storage.Storage import Storage

    def storage_list():
        from commander.utilities.PrettyPrint import SLINE, wd, header
        if not Storage.storage.is_empty():
            output.show_text(header('storage (key=value)'))
            for key, value in Storage.storage.variable.items():
                if isinstance(value, type('')):
                    output.show_text(
                        '%s = \'%s\'' % (key, value))
                else:
                    output.show_text('%s = %s' % (key, value))
            output.show_text(SLINE * wd)
        else:
            output.show_text('storage is empty')
            return False

        return True

    def env_list():
        def foobar(_dict, _name, _list):
            for xx, yy in _dict.items():
                if '__' not in xx[:2]:
                    if isinstance(yy, type(type)):
                        foobar(yy.__dict__, '%s.%s' %
                               (_name, xx), _list)
                    else:
                        if isinstance(yy, type('')):
                            _list.append('%s.%s = \'%s\'' % (_name, xx, yy))
                        else:
                            _list.append('%s.%s = %s' % (_name, xx, yy))

        try:
            if not Storage.storage.is_empty():
                env_list = []
                for env_key, env_value in Storage.storage.environment.items():
                    if '__' not in env_key[:2]:
                        foobar(env_value.__dict__, env_key, env_list)

                from commander.utilities.PrettyPrint import SLINE, wd, header
                output.show_text(header('environment (key=value)'))
                for list_item in sorted(env_list):
                    output.show_text(list_item)
                output.show_text(SLINE * wd)
            else:
                output.show_text('storage is empty')
                return False
        except:
            pass

        return True

    def storage_save(_filename=None):
        if _filename is None:
            _filename = 'storage.json'

        import os
        _filename = os.path.expanduser(_filename)

        output.show_text('save storage content to ' + _filename)

        Storage.storage.save(_filename)

        output.show_done()
        return True

    def storage_commit(_filename=None):
        if _filename is None:
            _filename = 'storage.json'

        import os
        _filename = os.path.expanduser(_filename)

        output.show_text('commit storage content to ' + _filename)

        Storage.storage.commit(_filename)

        output.show_done()
        return True

    def storage_load(_filename=None):
        if _filename is None:
            _filename = 'storage.json'

        import os
        _filename = os.path.expanduser(_filename)

        output.show_text('load storage content from ' + _filename)

        try:
            Storage.storage.load(_filename)
        except Exception as message:
            output.show_error('storage command error: %s' % message)
            return False

        output.show_done()
        return True

    def storage_clean(_name=None):
        if not Storage.storage.is_empty():
            if Storage.storage.clean(_name) is True:
                message = 'storage erased' if _name is None else 'variable %s erased' % _name
                output.show_text(message)
            else:
                message = 'storage erase failed' if _name is None else 'variable %s not found' % _name
                output.show_text(message)
                return False
        else:
            output.show_text('storage is empty')
            return False
        return True

    def storage_get(_name):
        if not Storage.storage.is_empty():
            if commander.is_var(_name):
                output.show_text('%s is "%s"' %
                                   (_name, commander.get_var(_name)))
            else:
                output.show_text('unknown variable %s' % _name)
                return False
        else:
            output.show_text('storage is empty')
            return False
        return True

    def storage_set(_name, _value):
        if commander.is_var(_name):
            output.show_text('old value for %s = %s' %
                               (_name, commander.get_var(_name)))
        commander.set_var(_name, _value)
        output.show_text('%s is "%s"' % (_name, _value))
        return True

    def help_on_error():
        output.show_error('syntax error: storage ' + ' '.join(cmd_line))
        output.show_doc(storage)

    if len(cmd_line) == 0:
        return storage_list()
    else:
        if cmd_line[0].lower() == 'list':
            return storage_list()
        elif cmd_line[0].lower() == 'env':
            return env_list()
        elif cmd_line[0].lower() == 'save':
            if len(cmd_line) > 1:
                return storage_save(cmd_line[1])
            else:
                return storage_save()
        elif cmd_line[0].lower() == 'commit':
            if len(cmd_line) > 1:
                return storage_commit(cmd_line[1])
            else:
                return storage_commit()
        elif cmd_line[0].lower() == 'load':
            if len(cmd_line) > 1:
                return storage_load(cmd_line[1])
            else:
                return storage_load()
        elif cmd_line[0].lower() == 'clean':
            if len(cmd_line) > 1:
                return storage_clean(cmd_line[1])
            else:
                return storage_clean()
        elif cmd_line[0].lower() == 'get':
            if len(cmd_line) > 1:
                return storage_get(cmd_line[1])
            else:
                help_on_error()
                return False
        elif cmd_line[0].lower() == 'set':
            if len(cmd_line) > 2:
                return storage_set(cmd_line[1], ' '.join(cmd_line[2:]))
            else:
                help_on_error()
                return False
        else:
            help_on_error()
            return False

    return True
