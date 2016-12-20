# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from flask import url_for

from league.dashboard.models import Color
from league.user.models import User

from .factories import GameFactory, UserFactory

skip_public = pytest.mark.skip(reason='Public pages disabled')


@skip_public
class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_200(self, user, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert 'Invalid password' in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        """Show error if username doesn't exist."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert 'Unknown user' in res


@skip_public
class TestRegistering:
    """Register a user."""

    def test_can_register(self, user, testapp):
        """Register a new user."""
        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get('/')
        # Clicks Create Account button
        res = res.click('Create account')
        # Fills out the form
        form = res.forms['registerForm']
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_passwords_dont_match(self, user, testapp):
        """Show error if passwords don't match."""
        # Goes to registration page
        res = testapp.get(url_for('public.register'))
        # Fills out form, but passwords don't match
        form = res.forms['registerForm']
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secrets'
        # Submits
        res = form.submit()
        # sees error message
        assert 'Passwords must match' in res

    def test_sees_error_message_if_user_already_registered(self, user, testapp):
        """Show error if user already registered."""
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = testapp.get(url_for('public.register'))
        # Fills out form, but username is already registered
        form = res.forms['registerForm']
        form['username'] = user.username
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit()
        # sees error
        assert 'Username already registered' in res


class TestPlayer:
    """Players."""

    def test_list_players(self, testapp, players):
        """Check that we can list players."""
        res = testapp.get(url_for('dashboard.players'))
        assert res.status_int == 200

        found_players = []
        for row in res.html.find('table').find('tbody').find_all('tr'):
            found_players.append([col.text for col in row.find_all('td')])
        assert len(players) == 2


class TestGame:
    """Games."""

    def test_list_games(self, testapp, db):
        """Check that we can list games."""

        first_game = GameFactory(winner=Color.white, handicap=3, komi=0)
        second_game = GameFactory(winner=Color.black, handicap=0, komi=7)

        res = testapp.get(url_for('dashboard.games'))
        assert res.status_int == 200

        games = []
        for row in res.html.find('table').find('tbody').find_all('tr'):
            games.append([col.text for col in row.find_all('td')])

        assert len(games) == 2
        assert games[0] == [str(first_game.white.aga_id),
                            str(first_game.black.aga_id),
                            first_game.winner.name, str(first_game.handicap),
                            str(first_game.komi)]
        assert games[1] == [str(second_game.white.aga_id),
                            str(second_game.black.aga_id),
                            second_game.winner.name, str(second_game.handicap),
                            str(second_game.komi)]
