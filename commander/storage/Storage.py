# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

import commander.termbase as output


storage = None


class Storage:
    def __init__(self):
        self.__variable = {}
        self.clean()

    @property
    def variable(self):

        def _foobar(_key, _storage, _result):
            if isinstance(_storage, type([])):
                for item in _storage:
                    _foobar(_key, item, _result)
            elif isinstance(_storage, type({})):
                for key, value in _storage.items():
                    _foobar((_key + '_' + key).strip('_'), value, _result)
            else:
                _result[_key] = _storage

        tmp_dict = self.__variable
        self.__set_date(tmp_dict)
        self.__set_date_path(tmp_dict)
        self.__set_time(tmp_dict)
        self.__set_time_path(tmp_dict)

        result = dict()
        _foobar('', self.__variable, result)

        return result

    @variable.setter
    def variable(self, _value):
        self.__variable.update(_value)

    @property
    def environment(self):
        def _foobar(_key, _storage, _result):
            if isinstance(_storage, type([])):
                for item in _storage:
                    _foobar(_key, item, _result)
            elif isinstance(_storage, type({})):
                tmp = dict()
                for key, value in _storage.items():
                    _foobar(key, value, tmp)

                _result[_key] = type(_key, (object,), tmp)

            else:
                _result[_key] = _storage

        tmp_dict = self.__variable
        self.__set_date(tmp_dict)
        self.__set_date_path(tmp_dict)
        self.__set_time(tmp_dict)
        self.__set_time_path(tmp_dict)

        result = dict()
        _foobar('ENV', tmp_dict, result)

        return result

    def clean(self, _name=None):
        if _name is None:
            self.__variable = {}
            return True
        else:
            _name = _name.upper()
            if _name in self.__variable:
                del self.__variable[_name]
                return True
        return False

    def load(self, _full_filename):
        import os
        assert os.path.exists(os.path.realpath(
            _full_filename)), 'storage load error: file not found ' + _full_filename

        with open(_full_filename, encoding='utf-8', mode='r') as storage_file:
            import json
            data = json.load(storage_file)
            if 'environment' in data:
                for name, value in data['environment'].items():
                    self.set_value(name.upper(), value)

    def save(self, _full_filename):
        data = {}
        import os

        if 'environment' not in data:
            data['environment'] = {}

        for name, value in self.__variable.items():
            data['environment'][name.upper()] = value

        with open(_full_filename, encoding='utf-8', mode='w') as storage_file:
            try:
                import json
                json.dump(data, storage_file)
            except Exception as message:
                pass

    def commit(self, _full_filename):
        data = {}
        import os
        if os.path.exists(os.path.realpath(_full_filename)):
            with open(_full_filename, encoding='utf-8', mode='r') as storage_file:
                try:
                    import json
                    data = json.load(storage_file)
                except Exception as message:
                    pass

        if 'environment' not in data:
            data['environment'] = {}

        for name, value in self.__variable.items():
            data['environment'][name.upper()] = value

        with open(_full_filename, encoding='utf-8', mode='w') as storage_file:
            import json
            json.dump(data, storage_file)

    def is_empty(self):
        return len(self.variable) == 0

    def is_defined(self, _name):
        _name = _name.upper()
        if _name in ['DATE', 'TIME', 'DATE_PATH', 'TIME_PATH']:
            return True

        if _name in self.variable:
            return True
        else:
            try:
                eval(_name, Storage.storage.environment)
                return True
            except:
                pass

        return False

    def __set_date(self, _data):
        from datetime import datetime
        _data['DATE'] = datetime.now().date().isoformat()

    def __set_date_path(self, _data):
        from datetime import datetime
        _data['DATE_PATH'] = datetime.now().date().strftime('%Y_%m_%d')

    def __set_time(self, _data):
        from datetime import datetime
        _data['TIME'] = datetime.now().time().strftime('%H:%M:%S')

    def __set_time_path(self, _data):
        from datetime import datetime
        _data['TIME_PATH'] = datetime.now().time().strftime('%H_%M_%S')

    def normalize(self, _str):
        # works with:
        # print(commander.normalize('/bla/blub/${DATE_PATH}_${TIME_PATH}/xx${COUNTER}.png'))
        # print(commander.normalize('${COUNTER}'))
        # print(commander.normalize('mark $TEST $DRIVE $TIME'))

        name_expression = '(\$)(\{){0,1}(\w+)(\}){0,1}'
        import re
        command = re.compile(name_expression, re.MULTILINE)

        for item in command.findall(_str):
            assert len(item) == 4, 'storage normalize string error: regexp'
            var_name = item[2].upper()

            var_value = self.get_value(var_name)
            if var_value is None:
                var_value = var_name
                output.show_warning(
                    'variable %s not in storage; use %s' % (var_name, var_value))

            var_definition = ''.join(item)
            _str = _str.replace(var_definition, var_value)

        return _str

    def get_value(self, _name):
        _name = _name.upper()
        if _name in self.variable:
            return '%s' % self.variable[_name]
        else:
            try:
                return '%s' % eval(_name, Storage.storage.environment)
            except:
                pass

        return None

    def set_value(self, _name, _value):
        _name = _name.upper()
        self.__variable[_name] = _value
