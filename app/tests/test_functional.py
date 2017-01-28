# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from flask import url_for

from league.dashboard.models import Color

from .factories import GameFactory, UserFactory


class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_200(self, db, testapp):
        """Login successful."""
        password = 'some_test_password'
        user = UserFactory(password=password)
        # Goes to homepage
        res = testapp.get('/dashboard/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = password
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get(url_for('dashboard.dashboard'))
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow().follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.get('/dashboard/')
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
        res = testapp.get('/dashboard/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert 'Unknown user' in res


class TestUser:
    """Users."""

    def test_delete_user(self, testapp, authed_user):
        """Test user deletion."""
        res = testapp.get(url_for('admin.list_and_delete_users'))
        raw_form = res.html.find('form', {'id': 'deleteUsersForm'})
        found_users = [int(inp.get('value')) for inp in
                       raw_form.find_all('input', {'name': 'obj_id'})]
        assert len(found_users) == 2

        form = res.forms['deleteUsersForm']
        form.fields['obj_id'][1].checked = True
        post_res = form.submit().follow()
        assert post_res.status_code == 200

        post_raw_form = post_res.html.find('form', {'id': 'deleteUsersForm'})
        post_found_users = [int(inp.get('value')) for inp in
                            post_raw_form.find_all('input',
                                                   {'name': 'obj_id'})]
        assert len(post_found_users) == 1


class TestPlayer:
    """Players."""

    def test_get_players(self, testapp, players):
        """Check that we can list players."""
        res = testapp.get(url_for('dashboard.get_players'))
        assert res.status_int == 200

        found_players = []
        for row in res.html.find('table').find('tbody').find_all('tr'):
            found_players.append([col.text for col in row.find_all('td')])
        assert len(players) == 2

    def test_delete_player(self, testapp, players):
        """Test player deletion."""
        res = testapp.get(url_for('dashboard.get_players'))
        raw_form = res.html.find('form', {'id': 'playerDeleteForm'})
        found_players = [int(inp.get('value')) for inp in
                         raw_form.find_all('input', {'name': 'player_id'})]
        assert len(found_players) == 2

        form = res.forms['playerDeleteForm']
        form.fields['player_id'][0].checked = True
        post_res = form.submit().follow()
        assert post_res.status_code == 200

        post_raw_form = post_res.html.find('form', {'id': 'playerDeleteForm'})
        post_found_players = [int(inp.get('value')) for inp in
                              post_raw_form.find_all('input',
                                                     {'name': 'player_id'})]
        assert len(post_found_players) == 1


class TestGame:
    """Games."""

    def test_get_games(self, testapp, db):
        """Check that we can get games."""
        first_game = GameFactory(winner=Color.white, handicap=3, komi=0)
        second_game = GameFactory(winner=Color.black, handicap=0, komi=7)
        db.session.commit()

        post_res = testapp.get(url_for('dashboard.get_games'))
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

        post_res = testapp.post(url_for('dashboard.create_game'), form)

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
        get_res = testapp.get(url_for('dashboard.get_games'))
        assert get_res.status_int == 200

        retrieved_games = get_res.json
        assert len(retrieved_games) == 2

        delete_res = testapp.delete('/dashboard/games/{}'.format(
                                    retrieved_games[0]['game_id']))
        assert delete_res.status_int == 204

        new_get_res = testapp.get(url_for('dashboard.get_games'))
        assert new_get_res.status_int == 200

        new_games = new_get_res.json
        assert len(new_games) == 1
