# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt
from operator import methodcaller

import pytest

from league.dashboard.models import Color, Game, Player
from league.admin.models import Role, User

from .factories import GameFactory, PlayerFactory, UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User('foo', 'foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username='foo', email='foo@bar.com')
        user.save()
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password='myprecious')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self):
        """Check password."""
        user = User.create(username='foo', email='foo@bar.com',
                           password='foobarbaz123')
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('barfoobaz') is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name='Foo', last_name='Bar')
        assert user.full_name == 'Foo Bar'

    def test_roles(self):
        """Add a role to a user."""
        role = Role(name='admin')
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles


class TestGame:
    """Game model tests."""

    def test_create(self, db):
        """Test game creation."""
        game = Game(PlayerFactory(), PlayerFactory(), Color.white, 0, 7, 1, 1)
        game.save()
        games = Game.query.all()
        players = Player.query.all()
        assert len(games) == 1
        assert len(players) == 2

    def test_get_max_season_ep(self, db):
        """Test calculation of maximum season and episode."""
        games = [GameFactory(season=s, episode=e)
                 for (s, e) in [(1, 1), (1, 2)]]
        map(methodcaller('save'), games)
        assert Game.get_max_season_ep() == (1, 2)
