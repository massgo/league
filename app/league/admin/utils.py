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
            if k == 'enabled':
                v = 'True' if v else 'False'
            config_item = SiteSettings(key='slack_{}'.format(k), value=v)
            config_item.save()
    else:
        new_config = {k: SiteSettings.get_by_key('slack_{}'.format(k)).value
                      for k in DEFAULT_CONFIG.keys()}
        if new_config['enabled'] == 'True':
            new_config['enabled'] = True
        else:
            new_config['enabled'] = False
        app.extensions['messenger'].update_configuration(config=new_config)


def update_messenger_config(app, **kwargs):
    """Update Slack messenger configuration."""
    for k, v in kwargs.items():
        if k == 'enabled':
            v = 'True' if v else 'False'
        config_item = SiteSettings.get_by_key(key='slack_{}'.format(k))
        config_item.value = v
        config_item.update()
    app.extensions['messenger'].update_configuration(config=kwargs)


def load_extension_config(app, extension_name):
    """Load an extension's configuration from the database."""
    extension = app.extensions[extension_name]
    new_config = {key: SiteSettings.get_by_key('{}_{}'.format(extension_name, key)).value
                  for key in extension.config.keys()}
    extension.update_config(new_config)
    new_config


def update_extension_config(app, extension_name, **kwargs):
    for key, value in league_config.items():
        if type(value) == bool:
            value = 'True' if value else 'False'
        config_item = SiteSettings.get_by_key(
            key='{extension}_{key}'.format(extension=extension_name, key=key))
        config_item.value = value
        config_item.update()
    league_config.update(kwargs)
    return kwargs


