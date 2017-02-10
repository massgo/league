# -*- coding: utf-8 -*-
"""Slack integration."""

import requests


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
        if self.enabled:
            self.url = app.config.get('SLACK_WEBHOOK')
            self.channel = app.config.get('SLACK_CHANNEL')
            self.username = app.config.get('SLACK_USERNAME')
            self.icon_emoji = app.config.get('SLACK_ICON_EMOJI')
            self.base_url = app.config.get('SLACK_BASE_URL')
        app.extensions['messenger'] = self

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
