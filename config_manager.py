#!/usr/bin/env python
# -*- coding: utf-8 -*-


import toml


class ConfigManager(object):
    def __init__(self):
        self.path = None
        self.cfg = None

    def read_config(self, path):
        self.path = path
        self.cfg = toml.load(path)

    def write_config(self):
        toml.dump(self.cfg, self.path)
