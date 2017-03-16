# -*- coding: utf-8 -*-
"""Admin helper utilities."""
from league.admin.models import ConfigData, User
from league.slack_messenger import DEFAULT_CONFIG, SLACK_ENABLED


def get_create_root_user(app):
    """
    Return function that creates root user.

    This is basically a hack around the fact that functions that need to be
    registered with before_first_request cannot take arguments.
    """
    def create_root_user():
        """Create root user."""
        if User.get_by_username('root') is None:
            root_user = User(username='root', email='root@localhost',
                             password=app.config['LEAGUE_ROOT_PASS'],
                             active=True,
                             is_admin=True)
            root_user.save()
    return create_root_user


def get_load_messenger_config(app):
    """
    Return function that updates the Slack messenger.

    A hack around circular import issues.
    """
    def load_messenger_config(app):
        """Load Slack messenger configuration."""
        if ConfigData.get_by_key(SLACK_ENABLED) is None:
            new_config = DEFAULT_CONFIG
            update = True
        else:
            new_config = {k: ConfigData.get_by_key('slack_{}'.format(k)).value
                          for k in DEFAULT_CONFIG.keys()}
            if new_config['enabled'] == 'True':
                new_config['enabled'] = True
            else:
                new_config['enabled'] = False
            update = False
        app.extensions['messenger'].update_configuration(config=new_config,
                                                         update_db=update)


def update_messenger_config(app, update_db=False, **kwargs):
    """Update Slack messenger configuration."""
    if update_db:
        for k, v in kwargs.items():
            if k == 'enabled':
                v = 'True' if v else 'False'
            config_item = ConfigData(key='slack_{}'.format(k), value=v)
            config_item.save()
    app.extensions['messenger'].update_configuration(config=kwargs)
