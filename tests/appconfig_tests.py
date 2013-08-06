# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Mathias Weber <mathew.weber@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
#
''' The unit test for the Config object '''

import unittest
import json
import tempfile
import shutil
import os.path

from appconfig import AppConfig, AppConfigValueException, PY2


class TestAppConfig(unittest.TestCase):
    ''' The unit test for the snake build common Config class. '''
    def setUp(self):
        self.config_dir = tempfile.mkdtemp()
        data = {"application_name": "appconfig_test",
                "application_author": "python",
                "application_version": "1.0",
                "Client": {
                    "first": {"default": "Start", "type": "str",
                        "description": "Aldebarans"},
                    "second": {"default": "Stop", "type": "unicode",
                        "description": "Altairians"},
                    "third": {"default": 12, "type": "int",
                        "description": "Amoeboid Zingatularians"},
                    "forth": {"default": 12.2, "type": "float",
                        "description": "Bartledanians"},
                    "fifth": {"default": True, "type": "bool",
                        "description": "Belcerebons"}},
                "Server": {
                    "first": {"default": "End", "type": "str",
                        "description": "Betelgeusians"},
                    "second": {"default": "Accelerate", "type": "unicode",
                        "description": "Blagulon Kappans"},
                    "third": {"default": -12, "type": "int",
                        "description": "Dentrassis"},
                    "forth": {"default": 3.3333, "type": "float",
                        "description": "Dolphins"},
                    "fifth": {"default": False, "type": "bool",
                        "description": "G'Gugvunnts and Vl'hurgs"}},
                "hidden": {
                    "one": {"default": "password", "type": "str",
                        "description": "The hidden password"}}}
        dfd = open(os.path.join(self.config_dir, 'test_data.txt'), 'w')
        dfd.write(json.dumps(data))
        dfd.close()

    def tearDown(self):
        ''' Remove temporary files '''
        if os.path.isdir(self.config_dir):
            shutil.rmtree(self.config_dir)

    def test_init_config(self):
        ''' Initialize the config object with default values and check values.
        '''
        config = AppConfig()
        with self.assertRaises(AppConfigValueException):
            config.init_default_config(os.path.join(self.config_dir,
                    'test_config.txt'))
        config.init_default_config(os.path.join(self.config_dir,
                'test_data.txt'))

        self.assertTrue(config.application_name == 'appconfig_test')
        self.assertTrue(config.application_author == 'python')
        self.assertTrue(config.application_version == '1.0')

        self._check_value(config, 'client', 'first', 'Aldebarans', str,
                'Start', 'Start')
        if PY2:
            self._check_value(config, 'client', 'second', 'Altairians',
                    unicode, 'Stop', 'Stop')
        else:
            self._check_value(config, 'client', 'second', 'Altairians',
                    str, 'Stop', 'Stop')
        self._check_value(config, 'client', 'third', 'Amoeboid Zingatularians',
                int, 12, 12)
        self._check_value(config, 'client', 'forth', 'Bartledanians', float,
                12.2, 12.2)
        self._check_value(config, 'client', 'fifth', 'Belcerebons', bool, True,
                True)

        self._check_value(config, 'server', 'first', 'Betelgeusians', str,
                'End', 'End')
        if PY2:
            self._check_value(config, 'server', 'second', 'Blagulon Kappans',
                    unicode, 'Accelerate', 'Accelerate')
        else:
            self._check_value(config, 'server', 'second', 'Blagulon Kappans',
                    str, 'Accelerate', 'Accelerate')
        self._check_value(config, 'server', 'third', 'Dentrassis', int, -12,
                -12)
        self._check_value(config, 'server', 'forth', 'Dolphins', float, 3.3333,
                3.3333)
        self._check_value(config, 'server', 'fifth',
                "G'Gugvunnts and Vl'hurgs", bool, False, False)

    def test_save_default_config(self):
        ''' Test the save functionality with a default config file '''
        config = AppConfig()
        config.init_default_config(os.path.join(self.config_dir,
                'test_data.txt'))

        config.save()
        # read the generated default output file (only three sections expected
        # nothing else should be in here since we haven't changed one value.
        # but added the default config file
        sections, values, comments = \
                self._parse_config_file(config.get(config.application_name,
                        'config_file'))
        self.assertTrue(sections == 3)
        self.assertTrue(values == 0)
        self.assertTrue(comments == 0)

        config.save(verbose=True)
        # search the verbose file with 3 lines of comment for each entry
        sections, values, comments = \
                self._parse_config_file(config.get(config.application_name,
                        'config_file'))
        self.assertTrue(sections == 3)
        self.assertTrue(values == 0)
        self.assertTrue(comments == 34)

        config.set('client', 'first', 42)
        config.set('client', 'second', 42)
        config.set('server', 'first', 42)
        config.set('server', 'second', 42)
        config.save()

        config.save()
        # read the config file after two value for each section where set
        sections, values, comments = \
                self._parse_config_file(config.get(config.application_name,
                        'config_file'))
        self.assertTrue(sections == 3)
        self.assertTrue(values == 4)
        self.assertTrue(comments == 0)

        config.save(verbose=True)
        # search the verbose file with 3 lines of comment for each entry and
        # some value where set with a none standard value
        sections, values, comments = \
                self._parse_config_file(config.get(config.application_name,
                        'config_file'))
        self.assertTrue(sections == 3)
        self.assertTrue(values == 4)
        self.assertTrue(comments == 34)

        # load default config
        config.load_default()
        self.assertTrue(config.get('client', 'first') == "42")

        os.remove(config.get(config.application_name, 'config_file'))

    def test_save_config(self):
        ''' Test the save functionality of the config module '''
        config = AppConfig()
        config.init_default_config(os.path.join(self.config_dir,
                'test_data.txt'))

        config.save(os.path.join(self.config_dir, 'test_default_output.txt'))
        config.save(os.path.join(self.config_dir,
                'test_default_output_verbose.txt'), True)
        # with directory
        config.save(os.path.join(self.config_dir, 'step',
                'test_default_output.txt'))

        config.set('client', 'first', 42)
        config.set('client', 'second', 42)
        config.set('server', 'first', 42)
        config.set('server', 'second', 42)
        config.save(os.path.join(self.config_dir, 'test_save_output.txt'))
        config.save(os.path.join(self.config_dir,
                'test_save_output_verbose.txt'), True)

        # read the generated default output file (only two sections expected
        # nothing else should be in here since we haven't changed one value.
        sections, values, comments = \
                self._parse_config_file('test_default_output.txt')
        self.assertTrue(sections == 2)
        self.assertTrue(values == 0)
        self.assertTrue(comments == 0)

        # search the verbose file with 3 lines of comment for each entry
        sections, values, comments = \
                self._parse_config_file('test_default_output_verbose.txt')
        self.assertTrue(sections == 2)
        self.assertTrue(values == 0)
        self.assertTrue(comments == 30)

        # read the config file after two value for each section where set
        sections, values, comments = \
                self._parse_config_file('test_save_output.txt')
        self.assertTrue(sections == 2)
        self.assertTrue(values == 4)
        self.assertTrue(comments == 0)

        # search the verbose file with 3 lines of comment for each entry and
        # some value where set with a none standard value
        sections, values, comments = \
                self._parse_config_file('test_save_output_verbose.txt')
        self.assertTrue(sections == 2)
        self.assertTrue(values == 4)
        self.assertTrue(comments == 30)

    def test_load_config(self):
        ''' test the config file loader '''
        tmp_config_file = os.path.join(self.config_dir, 'test_load_config.txt')
        config = AppConfig()
        config.init_default_config(os.path.join(self.config_dir,
                'test_data.txt'))

        f = open(tmp_config_file, 'w')
        f.write('[client]\n')
        f.write('first = The End\n')
        f.write('third = 1337\n')
        f.close()

        config.load(tmp_config_file)

        self._check_value(config, 'client', 'first', 'Aldebarans', str,
                'Start', 'The End')
        self._check_value(config, 'client', 'third', 'Amoeboid Zingatularians',
                int, 12, 1337)
        os.remove(tmp_config_file)

        with self.assertRaises(AppConfigValueException):
            config.load(tmp_config_file)

    def test_set_config(self):
        ''' Test seting and getting values from the config object '''
        config = AppConfig()

        # tests without default config loaded
        config.set('client', 'first', 12)
        value = config.get('client', 'first')
        self.assertTrue(type(value) == str)
        # this is a string since we don't now anything about it
        self.assertTrue(value == '12')

        config.set('client', 'third', -16)
        value = config.get('client', 'third')
        self.assertTrue(type(value) == str)
        # this is a string since we don't now anything about it
        self.assertTrue(value == '-16')

        # and now with default config loaded
        config.init_default_config(os.path.join(self.config_dir,
                'test_data.txt'))

        # check previous set values if the previous value remains.
        self._check_value(config, 'client', 'first', 'Aldebarans', str,
                'Start', "12")
        self._check_value(config, 'client', 'third',
                'Amoeboid Zingatularians', int, 12, -16)

        # now do some test for all kind of types
        config.set('client', 'first', 112)
        self._check_value(config, 'client', 'first', 'Aldebarans', str,
                'Start', "112")
        config.set('client', 'second', 12.45)
        if PY2:
            self._check_value(config, 'client', 'second', 'Altairians',
                    unicode, 'Stop', '12.45')
        else:
            self._check_value(config, 'client', 'second', 'Altairians',
                    str, 'Stop', '12.45')
        config.set('client', 'third', -166)
        self._check_value(config, 'client', 'third',
                'Amoeboid Zingatularians', int, 12, -166)
        config.set('client', 'forth', 11)
        self._check_value(config, 'client', 'forth', 'Bartledanians', float,
                12.2, 11.0)
        config.set('client', 'fifth', False)
        self._check_value(config, 'client', 'fifth', 'Belcerebons', bool,
                True, False)
        # the same with a string
        config.set('client', 'fifth', "False")
        self._check_value(config, 'client', 'fifth', 'Belcerebons', bool,
                True, False)
        config.set('client', 'fifth', "True")
        self._check_value(config, 'client', 'fifth', 'Belcerebons', bool,
                True, True)
        # the same with numbers
        config.set('client', 'fifth', 0)
        self._check_value(config, 'client', 'fifth', 'Belcerebons', bool,
                True, False)
        config.set('client', 'fifth', 1)
        self._check_value(config, 'client', 'fifth', 'Belcerebons', bool,
                True, True)
        # with illegal value
        with self.assertRaises(AppConfigValueException):
            config.set('client', 'fifth', 'no')

        config.set('server', 'first', True)
        self._check_value(config, 'server', 'first', 'Betelgeusians', str,
                'End', 'True')
        config.set('server', 'second', "Arther Dent")
        if PY2:
            self._check_value(config, 'server', 'second', 'Blagulon Kappans',
                    unicode, 'Accelerate', 'Arther Dent')
        else:
            self._check_value(config, 'server', 'second', 'Blagulon Kappans',
                    str, 'Accelerate', 'Arther Dent')
        config.set('server', 'third', 42)
        self._check_value(config, 'server', 'third', 'Dentrassis', int, -12,
                42)
        config.set('server', 'forth', 42.43)
        self._check_value(config, 'server', 'forth', 'Dolphins', float,
                3.3333, 42.43)
        config.set('server', 'fifth', True)
        self._check_value(config, 'server', 'fifth',
                "G'Gugvunnts and Vl'hurgs", bool, False, True)

    def test_get_description_illegal_values(self):
        ''' Test what happens if illegal or not existing values are being
            tried to be accessed.
        '''
        config = AppConfig()
        config.init_default_config(os.path.join(self.config_dir,
                'test_data.txt'))

        # try to access a value that does not exist
        with self.assertRaises(AppConfigValueException):
            config.get_description('server', 'alpha')

        # set a new value with no description and access it.
        config.set('server', 'alpha', "12")
        desc, ctype, default = config.get_description('server', 'alpha')
        self.assertTrue(desc == '')
        self.assertTrue(default == '')
        self.assertTrue(ctype == str)

        # access section which does not exist
        with self.assertRaises(AppConfigValueException):
            config.get_description('sunrise', 'alpha')

        # set value of a not existing section and access it again
        config.set('sunrise', 'alpha', 12)
        desc, ctype, default = config.get_description('sunrise', 'alpha')
        self.assertTrue(desc == '')
        self.assertTrue(default == '')
        self.assertTrue(ctype == str)

    def test_loading_illegal_config_description_files(self):
        ''' Test the mechanism to load config description files with illegal
            values.
        '''
        # read simple config description file with missing value (default
        # value)
        data = {"application_name": 'appconfig-test',
                "Client": {
                    "fifth": {"type": "bool",
                        "description": "Belcerebons"}}}
        dfd = open(os.path.join(self.config_dir, 'test_data2.txt'), 'w')
        dfd.write(json.dumps(data))
        dfd.close()

        with self.assertRaises(AppConfigValueException):
            config = AppConfig()
            config.init_default_config(os.path.join(self.config_dir,
                    'test_data2.txt'))

        # read simple config description file with missing value (type
        # value)
        data = {"application_name": 'appconfig-test',
                "Client": {
                    "fifth": {"default": True,
                        "description": "Belcerebons"}}}
        dfd = open(os.path.join(self.config_dir, 'test_data2.txt'), 'w')
        dfd.write(json.dumps(data))
        dfd.close()

        with self.assertRaises(AppConfigValueException):
            config = AppConfig()
            config.init_default_config(os.path.join(self.config_dir,
                    'test_data2.txt'))

        # read simple config description file with missing value (description
        # value)
        data = {"application_name": 'appconfig-test',
                "Client": {
                    "fifth": {"default": True, "type": 'bool'}}}
        dfd = open(os.path.join(self.config_dir, 'test_data2.txt'), 'w')
        dfd.write(json.dumps(data))
        dfd.close()

        with self.assertRaises(AppConfigValueException):
            config = AppConfig()
            config.init_default_config(os.path.join(self.config_dir,
                    'test_data2.txt'))

        # read simple config description file with an unsuproted type
        data = {"application_name": 'appconfig-test',
                "Client": {
                    "fifth": {"default": True, "type": 'value',
                        "description": "Belcerebons"}}}
        dfd = open(os.path.join(self.config_dir, 'test_data2.txt'), 'w')
        dfd.write(json.dumps(data))
        dfd.close()

        with self.assertRaises(AppConfigValueException):
            config = AppConfig()
            config.init_default_config(os.path.join(self.config_dir,
                    'test_data2.txt'))

    def _check_value(self, config, section, key, edesc, etype, edefault,
            evalue):
        ''' Check if the given config value has the expected values.
            @param config: The config object to check
            @param section: The section to check
            @param key: The key to check
            @param edesc: Expected Description
            @param etype: Expected type
            @param edefault: Expected default value
            @param evalue: Expected value
        '''
        value = config.get(section, key)
        self.assertTrue(type(value) == etype)
        self.assertTrue(value == evalue)
        desc, ctype, default = config.get_description(section, key)
        self.assertTrue(default == edefault)
        self.assertTrue(desc == edesc)
        self.assertTrue(ctype == etype)

    def _parse_config_file(self, filename):
        ''' parse a config file and count the number of sections, values and
            comments.

            @param filename: The name of the config file to read
            @return #section, #values, #comments
        '''
        cfl = open(os.path.join(self.config_dir, filename))
        sections = 0
        values = 0
        comments = 0
        for line in cfl.readlines():
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                sections += 1
            elif line.startswith('#'):
                comments += 1
            elif len(line.split('=')) == 2:
                values += 1
        cfl.close()
        return sections, values, comments
