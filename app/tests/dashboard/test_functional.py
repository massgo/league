# -*- coding: utf-8 -*-
"""API functional tests."""
from flask import url_for


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
