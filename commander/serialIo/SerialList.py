# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2024 Roman Koch <koch.roman@gmail.com>
# SPDX-FileType: SOURCE
# SPDX-FileContributor: Created by Roman Koch
# SPDX-License-Identifier: MIT

from commander.serialIo.threaded.SerialPortThreaded import SerialPortThreaded


class SerialList(object):
    """
    list of serial ports
    """

    def __init__(self):
        self.serial = {}
        self.device = {}

    def add(self, _alias, _device, _parameter):
        # assert 'device' in _device, "serial list add: open %s, no device specified" % _alias
        for val in list(self.device.values()):
            assert val != _device.device, 'device %s already opened with alias %s' % (
                _device.device, _alias)

        device_identifier = _device.device

        if ':' in device_identifier:
            ports = self.list_serial_ports()
            extended_device_identifier = device_identifier.split(':')
            if len(extended_device_identifier) == 2:
                if 'serial' in extended_device_identifier[0]:
                    serial = extended_device_identifier[1]
                    for port in ports:
                        if port.serial_number == serial:
                            _device.device = port.device
                            break
                else:
                    vid = int(extended_device_identifier[0], 16)
                    pid = int(extended_device_identifier[1], 16)
                    for port in ports:
                        if port.pid == pid and port.vid == vid:
                            _device.device = port.device
                            break

        self.device[_alias] = _device.device
        self.serial[_alias] = SerialPortThreaded(_alias, _device,  _parameter)
        if not self.serial[_alias].start():  # could not open port, remove association
            del self.serial[_alias]
            del self.device[_alias]
            return False
        else:  # port opened, threads active
            return True

    def remove(self, alias):
        # print 'close %s' % name
        self.serial[alias].stop()
        del self.serial[alias]
        del self.device[alias]

    def erase(self):
        for alias in self.serial.keys():
            self.serial[alias].stop()
        self.serial = {}
        self.device = {}

    def has_port(self, alias):
        return alias in self.serial

    def get_port(self, alias):
        return self.serial[alias]

    def get_device_info(self, _device):
        from commander.serialIo.phy.SerialPhyPython import SerialPhyPython
        devices = SerialPhyPython.list_devices()
        for item in devices:
            if item.device == _device:
                result = {}
                result['name'] = item.name if item.name is not None else ''
                result['description'] = item.description if item.description is not None else ''
                result['serial_number'] = item.serial_number if item.serial_number is not None else ''
                result['product'] = item.product if item.product is not None else ''
                result['subsystem'] = item.subsystem if item.subsystem is not None else ''
                result['pid'] = ('%04X' %
                                 item.pid) if item.pid is not None else '0000'
                result['vid'] = ('%04X' %
                                 item.vid) if item.vid is not None else '0000'
                return result
        return None

    def list_serial_ports(self):
        print('scan for serial ports...', end=' ')

        result = []

        try:
            from commander.serialIo.phy.SerialPhyPython import SerialPhyPython
            result += SerialPhyPython.list_devices()
        except Exception as msg:
            print('\npyserial devices could not be enumerated: ', msg)

        print(' done')
        return result

    def __str__(self):
        from commander.utilities.PrettyPrint import DLINE, wd, SLINE
        s = ''
        s += DLINE * wd + '\n'
        s += 'serial ports\n'
        s += SLINE * wd + '\n'
        s += '%-26s:%6s:%-18s:%-7s\n' % ('port',
                                         'status', 'alias', 'interpreter')
        s += SLINE * wd + '\n'

        ports = sorted(self.list_serial_ports())
        opened_ports = dict()
        for alias in self.serial.keys():
            from commander.serialIo.threaded.SerialPortThreaded import SerialPortThreaded
            from commander.utilities.dict_tweaks import value_to_key
            interpreter = value_to_key(
                SerialPortThreaded.INTERPRETER, self.serial[alias].interpreter)
            dialect = self.serial[alias].handler.dialect
            opened_ports[self.device[alias]] = {
                'alias': alias, 'interpreter': interpreter + ('' if dialect is None else ' %s' % dialect)}

        if len(ports) == 0:
            s += 'no ports available' + '\n'
        else:
            for item in sorted(ports):
                device_name = item.device

                if len(device_name) > 26:
                    device_name = '...' + device_name[-23:]
                if item.device in opened_ports:
                    alias = opened_ports[item.device]['alias']
                    interpreter = opened_ports[item.device]['interpreter']
                    s += '%-26s:%6s:%-18s:%-7s\n' % (
                        device_name[-23:], 'open', alias[:18], interpreter)
                else:
                    s += '%-26s:%6s:%-18s:%-7s\n' % (
                        device_name[-23:], 'closed', '', '')

        s += SLINE * wd + '\n'

        return s
