#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
from util import create_dirs


class LogManager(object):
    def __init__(self, path):
        create_dirs(path)
        logging.basicConfig(filename=path, filemode='w', level=logging.INFO)
        self.logging = logging.getLogger('main')
