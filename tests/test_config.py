#! /usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2008, José Dinuncio <jdinunci@uc.edu.ve>
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.
#
##############################################################################

import unittest

from repoze.what.plugins.config import WhatConfig

CONFIG_TEXT = '''
[plugin:mydict]
use = collections:defaultdict
keyone = blah
keytwo = foo

[plugin:myotherdict]
use = collections:defaultdict
keyuno = bar
keydos = baz

[what]
group_adapters = mydict myotherdict
permission_adapters = myotherdict


'''

PLUGINS = ['mydict', 'myotherdict' ]


class TestWhatConfig(unittest.TestCase):
    '''Tests for WhatConfig'''

    def test_makePlugin(self):
        wc = WhatConfig('')
        obj = wc._makePlugin('collections:defaultdict', a='abc', b='def')
        assert repr(obj) == "defaultdict(None, {'a': 'abc', 'b': 'def'})"

    def test_parse(self):
        wc = WhatConfig('')
        wc.parse(CONFIG_TEXT)
        for plugin in PLUGINS:
            assert plugin in wc.plugins
        assert 'mydict' in wc.group_adapters
        assert 'myotherdict' in wc.group_adapters
        assert 'mydict' not in wc.permission_adapters
        assert 'myotherdict' in wc.permission_adapters

