# -*- coding: utf-8 -*-
"""Slack integration module."""
import requests

class SlackMessenger(object):

    def __init__(self, app=None):
        if app:
            self.app = app
            self.init_app(app)

    def init_app(self, app):
        self.url = app.config.get('SLACK_WEBHOOK')
        self.channel = app.config.get('SLACK_CHANNEL')
        self.payload = {'username': 'webhookbot',
                        'icon_emoji': ':ghost:',
                        'channel': self.channel}
        app.extensions['messenger'] = self

        def f(msg):
            """Sends message to Slack."""
            msg.update(self.payload)
            try:
                r = requests.post(self.url, json=self.payload)
            except requests.exceptions.RequestException as e:
                pass

        if self.url:
            self.notify_slack = f

    def notify_slack(self, msg):
        """SLACK_WEBHOOK not initialized."""
        pass
