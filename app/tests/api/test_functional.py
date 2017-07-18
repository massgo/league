# -*- coding: utf-8 -*-
"""API functional tests."""
import pytest
from flask import url_for

from league.models import Color

from ..factories import GameFactory


class TestGame:
    """Games."""

    def test_get_games(self, testapp, db):
        """Check that we can get games."""
        first_game = GameFactory(winner=Color.white, handicap=3, komi=0)
        second_game = GameFactory(winner=Color.black, handicap=0, komi=7)
        db.session.commit()

        post_res = testapp.get(url_for('api.get_games'))
        assert post_res.status_int == 200

        games = post_res.json
        assert len(games) == 2

        assert int(games[0]['game_id']) == first_game.id
        assert games[0]['winner'] == first_game.winner.name
        assert int(games[0]['handicap']) == first_game.handicap
        assert int(games[0]['komi']) == first_game.komi

        assert int(games[1]['game_id']) == second_game.id
        assert games[1]['winner'] == second_game.winner.name
        assert int(games[1]['handicap']) == second_game.handicap
        assert int(games[1]['komi']) == second_game.komi

    @pytest.mark.parametrize('winner', ['white'])
    @pytest.mark.parametrize('handicap', [0, 8])
    @pytest.mark.parametrize('komi', [0, 7])
    @pytest.mark.parametrize('season', [1])
    @pytest.mark.parametrize('episode', [1])
    def test_create_game(self, testapp, players, winner, handicap, komi, season,
                         episode):
        """Check that we can create a game."""
        form = {
            'white_id': players[0].id,
            'black_id': players[1].id,
            'winner': winner,
            'handicap': handicap,
            'komi': komi,
            'season': season,
            'episode': episode
        }

        post_res = testapp.post(url_for('api.create_game'), form)

        assert post_res.status_code == 201
        game = post_res.json

        assert int(game['game_id']) == 1
        assert game['white_id'] == players[0].id
        assert game['black_id'] == players[1].id
        assert game['winner'] == winner
        assert game['handicap'] == handicap
        assert game['komi'] == komi
        assert game['season'] == season
        assert game['episode'] == episode

    def test_delete_game(self, testapp, games):
        """Test game deletion."""
        get_res = testapp.get(url_for('api.get_games'))
        assert get_res.status_int == 200

        retrieved_games = get_res.json
        assert len(retrieved_games) == 2

        delete_res = testapp.delete('/dashboard/games/{}'.format(
                                    retrieved_games[0]['game_id']))
        assert delete_res.status_int == 204

        new_get_res = testapp.get(url_for('api.get_games'))
        assert new_get_res.status_int == 200

        new_games = new_get_res.json
        assert len(new_games) == 1
