# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('LEAGUE_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LEAGUE_ROOT_PASS = os.environ.get('LEAGUE_ROOT_PASS', 'root')
    SLACK_NOTIFICATIONS_ENABLED = 'SLACK_WEBHOOK' in os.environ
    SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')
    SLACK_BASE_URL = os.environ.get('SLACK_BASE_URL')
    SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')
    SLACK_USERNAME = os.environ.get('SLACK_USERNAME', 'leaguebot')
    SLACK_ICON_EMOJI = os.environ.get('SLACK_ICON_EMOJI', ':robot_face:')


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'postgresql')
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgresql')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')
    SQLALCHEMY_DATABASE_URI = ('postgresql://{}:{}@db/{}').format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_DB
    )
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    LEAGUE_ROOT_PASS = 'root'


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    LOGIN_DISABLED = True

    # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    BCRYPT_LOG_ROUNDS = 4

    WTF_CSRF_ENABLED = False  # Allows form testing

    SLACK_NOTIFICATIONS_ENABLED = False
