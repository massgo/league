# -*- coding: utf-8 -*-
"""Model unit tests."""

from league.dashboard.reports import Report
from league.models import Game, Player


class TestReport:
    """User tests."""

    def test_generate_report(self, games):
        """Generate a report."""
        report = Report(1, 1)
        assert report.season == 1
        assert report.episode == 1

        players = list(report.players)
        games = list(report.games)
        assert len(players) == 4
        assert len(games) == 2

        for game in games:
            assert isinstance(game, Game)
        for player in players:
            assert isinstance(player, Player)
