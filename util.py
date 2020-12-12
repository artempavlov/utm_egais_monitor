#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import errno
import sys
import subprocess


def create_dirs(path):
    dirname = os.path.dirname(os.path.abspath(path))
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def open_file(path):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', path))
    elif os.name == 'nt':
        os.startfile(path)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', path))
