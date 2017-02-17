# -*- coding: utf-8 -*-
"""Slack integration."""

import requests

from league.config_utils import update_config_file


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
        self.enabled = app.config.get('SLACK_NOTIFICATIONS_ENABLED')
        self.url = app.config.get('SLACK_WEBHOOK')
        self.channel = app.config.get('SLACK_CHANNEL')
        self.username = app.config.get('SLACK_USERNAME')
        self.icon_emoji = app.config.get('SLACK_ICON_EMOJI')
        app.extensions['messenger'] = self

    def update_configuration(self, enabled, url, channel, username, icon_emoji):
        """Update Slack Messenger configuration."""
        self.enabled = enabled
        self.url = url
        self.channel = channel
        self.username = username
        self.icon_emoji = icon_emoji
        update_config_file({'SLACK_NOTIFICATIONS_ENABLED': self.enabled,
                            'SLACK_WEBHOOK': self.url,
                            'SLACK_CHANNEL': self.channel,
                            'SLACK_USERNAME': self.username,
                            'SLACK_ICON_EMOJI': self.icon_emoji})
        pass

    def notify_slack(self, msg):
        """Send a simple notification to Slack."""
        if self.enabled:
            payload = {'username': self.username,
                       'icon_emoji': self.icon_emoji,
                       'channel': self.channel,
                       'text': msg}
            requests.post(self.url, json=payload)
            self.app.logger.debug('Sent {} to {}'.format(msg, self.channel))
        else:
            self.app.logger.debug('Ignoring message request')
