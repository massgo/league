# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from flask import url_for
from webtest import TestApp

from league.app import create_app
from league.database import db as _db
from league.settings import TestConfig

from .factories import UserFactory


@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """A user for the tests."""
    user = UserFactory(password='myprecious')
    db.session.commit()
    return user


@pytest.fixture
def authed_user(db, testapp):
    """A user that has been authenticated with the testapp."""
    password = 'some_test_password'
    user = UserFactory(password=password)
    res = testapp.get(url_for('dashboard.dashboard'))
    # Fills out login form in navbar
    form = res.forms['loginForm']
    form['username'] = user.username
    form['password'] = password
    form.submit().follow()


@pytest.fixture
def users(db):
    """Some users for the tests."""
    users = [UserFactory(), UserFactory()]
    db.session.commit()
    return users
