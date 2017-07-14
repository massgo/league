# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt
from operator import methodcaller

from league.models import Color, Game, Player

from .factories import GameFactory, PlayerFactory


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

    def test_set_created_at(self, db):
        """Test game creation with specified created_at."""
        some_datetime = dt.datetime(2017, 1, 1, 1, 1, 1, 1)
        game = GameFactory(created_at=some_datetime)
        game.save()
        games = Game.query.all()
        assert games[0].created_at == some_datetime

    def test_set_played_at(self, db):
        """Test game creation with specified played_at."""
        some_datetime = dt.datetime(2017, 1, 1, 1, 1, 1, 1)
        game = GameFactory(played_at=some_datetime)
        game.save()
        games = Game.query.all()
        assert games[0].played_at == some_datetime

    def test_get_max_season_ep(self, db):
        """Test calculation of maximum season and episode."""
        games = [GameFactory(season=s, episode=e)
                 for (s, e) in [(1, 1), (1, 2), (2, 1)]]
        map(methodcaller('save'), games)
        assert Game.get_max_season_ep() == (2, 2)

    def test_latest_season_episode(self, db):
        """Test calculation of latest (season, episode) tuple."""
        games = [GameFactory(season=s, episode=e)
                 for (s, e) in [(1, 1), (1, 2), (2, 1), (3, 1)]]
        map(methodcaller('save'), games)
        assert Game.latest_season_episode() == (3, 1)
