# -*- coding: utf-8 -*-
"""Helper utility for managing application settings."""
import json
from os.path import exists, getsize, join

from flask import current_app


def update_config_file(new_config):
    """Update application configuration variables."""
    config_file = join(current_app.config.get('APP_DIR'),
                       current_app.config.get('CONFIG_FILE'))
    if exists(config_file) and getsize(config_file) > 0:
        with open(config_file, 'r') as f:
            config_items = json.load(f)
    else:
        config_items = dict()
    config_items.update(new_config)
    if exists(config_file):
        with open(config_file, 'w') as f:
            json.dump(config_items, f)
