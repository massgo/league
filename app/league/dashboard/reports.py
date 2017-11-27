# -*- coding: utf-8 -*-
"""Dashboard reports."""
from league.models import Game


class Report(object):
    """A convenience class for generating AGA results reports."""

    def __init__(self, season, episode):
        """Build a report."""
        self.season = season
        self.episode = episode

        self.games = []
        if self.episode > 0:
            self.games = Game.get_by_season_ep(season, episode)
        elif self.episode == 0:
            self.games = Game.get_by_season(season)

        player_sets = [game.players for game in self.games]
        self.players = frozenset().union(*player_sets)
