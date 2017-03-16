# -*- coding: utf-8 -*-
"""Slack integration."""
import requests

DEFAULT_CONFIG = {'enabled': False,
                  'webhook': '',
                  'channel': '',
                  'username': 'leaguebot',
                  'icon_emoji': ':robot_face:'}
SLACK_ENABLED = 'slack_enabled'


class SlackMessenger(object):
    """A Slack messenger."""

    def __init__(self, app=None):
        """Initialize messenger."""
        self.enabled = False
        if app:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        """Initialize Slack Messenger."""
        self.app = app
        self.config = DEFAULT_CONFIG
        app.extensions['messenger'] = self

    def update_configuration(self, config):
        """Update Slack Messenger configuration."""
        self.config.update(config)

    def notify_slack(self, msg):
        """Send a simple notification to Slack."""
        if self.config['enabled']:
            payload = {'username': self.config['username'],
                       'icon_emoji': self.config['icon_emoji'],
                       'channel': self.config['channel'],
                       'text': msg}
            requests.post(self.config['webhook'], json=payload)
            self.app.logger.debug('Sent {} to {}'.format(msg, self.channel))
        else:
            self.app.logger.debug('Ignoring message request: webhook disabled.')
