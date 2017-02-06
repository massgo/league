# -*- coding: utf-8 -*-
"""Slack integration module."""
import requests

class SlackMessenger(object):

    def __init__(self, app=None):
        if app:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.url = app.config.get('SLACK_WEBHOOK')
        self.channel = app.config.get('SLACK_CHANNEL')
        self.username = app.config.get('SLACK_USERNAME') or 'leaguebot'
        self.icon_emoji = app.config.get('SLACK_ICON_EMOJI') or ':robot:'
        app.extensions['messenger'] = self

    def notify_slack(self, msg):
        """Sends a simple notification to Slack."""
        try:
            payload = {'username': self.username,
                        'icon_emoji': self.icon_emoji,
                        'channel': self.channel,
                        'text': msg}
            r = requests.post(self.url, json=self.payload)
        except AttributeError as e:
            self.app.logger.warning('Environmental variables for Slack ' +
                'integration are not configured: {0}'.format(e))
        except requests.exceptions.RequestException as e:
            self.app.logger.error(e)
