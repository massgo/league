# -*- coding: utf-8 -*-
"""Test forms."""

import pytest

from league.dashboard.forms import GameCreateForm


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
