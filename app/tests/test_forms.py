# -*- coding: utf-8 -*-
"""Test forms."""

import pytest

from league.dashboard.forms import GameCreateForm
from league.public.forms import LoginForm
from league.user.forms import RegisterForm


class TestRegisterForm:
    """Register form."""

    def test_validate_user_already_registered(self, user):
        """Enter username that is already registered."""
        form = RegisterForm(username=user.username, email='foo@bar.com',
                            password='example', confirm='example')

        assert form.validate() is False
        assert 'Username already registered' in form.username.errors

    def test_validate_email_already_registered(self, user):
        """Enter email that is already registered."""
        form = RegisterForm(username='unique', email=user.email,
                            password='example', confirm='example')

        assert form.validate() is False
        assert 'Email already registered' in form.email.errors

    def test_validate_success(self, db):
        """Register with success."""
        form = RegisterForm(username='newusername', email='new@test.test',
                            password='example', confirm='example')
        assert form.validate() is True


class TestLoginForm:
    """Login form."""

    def test_validate_success(self, user):
        """Login successful."""
        user.set_password('example')
        user.save()
        form = LoginForm(username=user.username, password='example')
        assert form.validate() is True
        assert form.user == user

    def test_validate_unknown_username(self, db):
        """Unknown username."""
        form = LoginForm(username='unknown', password='example')
        assert form.validate() is False
        assert 'Unknown username' in form.username.errors
        assert form.user is None

    def test_validate_invalid_password(self, user):
        """Invalid password."""
        user.set_password('example')
        user.save()
        form = LoginForm(username=user.username, password='wrongpassword')
        assert form.validate() is False
        assert 'Invalid password' in form.password.errors

    def test_validate_inactive_user(self, user):
        """Inactive user."""
        user.active = False
        user.set_password('example')
        user.save()
        # Correct username and password, but user is not activated
        form = LoginForm(username=user.username, password='example')
        assert form.validate() is False
        assert 'User not activated' in form.username.errors


class TestGameCreateForm:
    """Game create form."""

    @pytest.mark.parametrize('winner', ['white', 'black'])
    @pytest.mark.parametrize('handicap', [0, 8])
    @pytest.mark.parametrize('komi', [0, 7])
    @pytest.mark.parametrize('season', [1])
    @pytest.mark.parametrize('episode', [1])
    def test_validate_success(self, players, winner, handicap, komi, season,
                              episode, season_choices, episode_choices):
        """Create a valid game."""
        form = GameCreateForm(white_id=players[0].id,
                              black_id=players[1].id,
                              winner=winner,
                              handicap=handicap,
                              komi=komi,
                              season=season,
                              episode=episode)
        player_choices = [(player.id, player.full_name) for player in players]
        form.white_id.choices = player_choices
        form.black_id.choices = player_choices
        form.season.choices = season_choices
        form.episode.choices = episode_choices
        assert form.validate() is True, ('Validation failed: {}'
                                         ''.format(form.errors))
