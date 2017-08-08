# -*- coding: utf-8 -*-
"""Admin helper utilities."""
from league.admin.models import SiteSettings, User
from league.slack_messenger import DEFAULT_CONFIG, SLACK_ENABLED


def create_root_user(app):
    """Create root user."""
    if User.get_by_username('root') is None:
        root_user = User(username='root', email='root@localhost',
                         password=app.config['LEAGUE_ROOT_PASS'],
                         active=True,
                         is_admin=True)
        root_user.save()


def load_messenger_config(app):
    """Load Slack messenger configuration."""
    if SiteSettings.get_by_key(SLACK_ENABLED) is None:
        for k, v in DEFAULT_CONFIG.items():
            config_item = SiteSettings(key='slack_{}'.format(k), value=v)
            config_item.save()
    else:
        new_config = {k: SiteSettings.get_by_key('slack_{}'.format(k)).value
                      for k in DEFAULT_CONFIG.keys()}
        app.extensions['messenger'].update_configuration(config=new_config)


def update_messenger_config(app, **kwargs):
    """Update Slack messenger configuration."""
    for key, value in kwargs.items():
        if type(value) == bool:
            value = 'True' if value else 'False'
        config_item = SiteSettings.get_by_key(key='slack_{}'.format(key))
        config_item.value = value
        config_item.update()
    app.extensions['messenger'].update_configuration(config=kwargs)


def load_site_config(app):
    """Load site settings from the database."""
    config = app.config['SITE_SETTINGS']
    new_config = dict()
    for key in config:
        config_item = SiteSettings.get_by_key(
            key='site_settings_{}'.format(key))
        if config_item is not None:
            new_config[key] = config_item.value
    config.update(new_config)
    app.config.update(SITE_SETTINGS=config)


def update_site_settings(app, **kwargs):
    """Update site settings."""
    config = app.config['SITE_SETTINGS']
    for key, value in kwargs.items():
        if type(value) == bool:
            value = 'True' if value else 'False'
        config_item = SiteSettings.get_by_key(
            key='site_settings_{key}'.format(key=key))
        if config_item is not None:
            config_item.value = value
            config_item.update()
        else:
            config_item = SiteSettings(
                key='site_settings_{}'.format(key), value=value)
            config_item.save()
    config.update(**kwargs)
    app.config.update(SITE_SETTINGS=config)
