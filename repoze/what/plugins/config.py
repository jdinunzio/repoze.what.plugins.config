# -*- coding: utf-8 -*-
# repoze.what paster config. Based on repoze.who.config.WhoConfig

from ConfigParser import ConfigParser
from StringIO import StringIO

from pkg_resources import EntryPoint
from repoze.who.config import WhoConfig
from repoze.what.middleware import setup_auth


class WhatConfig:
    def __init__(self, here):
        self.here = here
        self.plugins = {}
        self.group_adapters = {}
        self.permission_adapters = {}

    def _makePlugin(self, factory_name, **kw):
        factory = EntryPoint.parse('x=%s' % factory_name).load(False)
        obj = factory(**kw)
        return obj

    def _parsePluginSequence(self, dct, adapter_line):
        for name in adapter_line.split():
            dct[name] = self.plugins[name]

    def parse(self, text):
        if getattr(text, 'readline', None) is None:
            text = StringIO(text)
        cp = ConfigParser(defaults={'here': self.here})
        cp.readfp(text)

        for s_id in [x for x in cp.sections() if x.startswith('plugin:')]:
            plugin_id = s_id[len('plugin:'):]
            options = dict(cp.items(s_id))
            if 'use' in options:
                factory_name = options.pop('use')
                del options['here']
                obj = self._makePlugin(factory_name, **options)
                self.plugins[plugin_id] = obj

        if 'what' in cp.sections():
            what = dict(cp.items('what'))
            if 'group_adapters' in what:
                self._parsePluginSequence(self.group_adapters, 
                                          what['group_adapters'])
            if 'permission_adapters' in what:
                self._parsePluginSequence(self.permission_adapters, 
                                          what['permission_adapters'])


def make_middleware_with_config(app, global_conf, config_file,
                                who_config_file = ''):
    if not who_config_file:
        who_config_file = config_file
    who_parser = WhoConfig(global_conf['here'])
    who_parser.parse(open(who_config_file))
    what_parser = WhatConfig(global_conf['here'])
    what_parser.parse(open(config_file))

    return setup_auth(app,
                      group_adapters=what_parser.group_adapters,
                      permission_adapters=what_parser.permission_adapters,
                      identifiers=who_parser.identifiers,
                      authenticators=who_parser.authenticators,
                      challengers=who_parser.challengers,
                      mdproviders=who_parser.mdproviders,
                      classifier=who_parser.request_classifier,
                      challenge_decider=who_parser.challenge_decider
                     )

