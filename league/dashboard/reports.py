# -*- coding: utf-8 -*-
"""Dashboard reports."""
from league.dashboard.models import Game


class Report(object):
    """A convenience class for generating AGA results reports."""

    def __init__(self, season, episode):
        """Build a report."""
        self.season = season
        self.episode = episode

        self.games = Game.get_by_season_ep(season, episode)
        self.players = []
