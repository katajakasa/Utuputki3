# -*- coding: utf-8 -*-

import json
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_FILENAME = 'utuputki3.json'
CONF_FILES = [
    os.path.join(BASEDIR, CONF_FILENAME),
    os.path.join('../', CONF_FILENAME),
    os.path.join('~/.local/utuputki3/', CONF_FILENAME),
    os.path.join('/etc/utuputki3/', CONF_FILENAME)
]


def read_config_file(filename):
    config = None
    try:
        with open(filename, 'rb') as handle:
            config = json.loads(handle.read().decode('utf-8'))
    except FileNotFoundError:
        pass
    return config


def read_config(override_file=None):
    config = None
    if override_file:
        config = read_config_file(override_file)
    else:
        for path in CONF_FILES:
            config = read_config_file(path)
            if config:
                break
    return config
