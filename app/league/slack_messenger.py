#slack_messenger
import requests

class SlackMessenger(object):

    enabled = False

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
        if self.url:
            self.enabled = True

    def notify_slack(self, msg):
        """Something something something"""
        msg.update(self.payload)
        r = requests.post(self.url, json=payload)
