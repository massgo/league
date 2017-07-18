# -*- coding: utf-8 -*-
"""API."""
from datetime import timezone

from flask import Blueprint, jsonify, request, url_for
from flask_login import login_required

from league.api.forms import GameCreateForm, GameUpdateForm
from league.extensions import csrf_protect, messenger
from league.models import Color, Game, Player

blueprint = Blueprint('api', __name__, url_prefix='/api/v1.0',
                      static_folder='../static')


def _set_game_create_choices(game_create_form):
    """
    Calculate choices for season and episode and update form.

    Should allow up to one more than current maxima.
    """
    max_season, max_episode = Game.get_max_season_ep()
    game_create_form.season.choices = [(s, s) for s in range(1, max_season + 2)]
    game_create_form.episode.choices = [(e, e) for e in
                                        range(1, max_episode + 2)]

    player_choices = [
        (player.id, '{} ({})'.format(player.full_name, player.aga_id))
        for player in Player.get_players()
    ]
    game_create_form.white_id.choices = player_choices
    game_create_form.black_id.choices = player_choices


@blueprint.route('/games/all', methods=['GET'])
@login_required
def get_games():
    """Get all games."""
    form = GameCreateForm(request.form, csrf_enabled=False)
    _set_game_create_choices(form)

    games = Game.query.all()
    return jsonify([game.to_dict() for game in games]), 200


@blueprint.route('/games/', methods=['POST'])
@login_required
def create_game():
    """Create a new game."""
    form = GameCreateForm(request.form)
    _set_game_create_choices(form)
    if form.validate_on_submit():
        white = Player.get_by_id(form.white_id.data)
        black = Player.get_by_id(form.black_id.data)
        played_at = None
        if form.played_at.data is not None:
            played_at = form.played_at.data.astimezone(timezone.utc)
        game = Game.create(
            white=white,
            black=black,
            winner=form.winner.data,
            handicap=form.handicap.data,
            komi=form.komi.data,
            season=form.season.data,
            episode=form.episode.data,
            played_at=played_at
        )
        messenger.notify_slack(_slack_game_msg(game))
        return jsonify(game.to_dict()), 201
    else:
        return jsonify(**form.errors), 404


def _slack_game_msg(game):
    if game.winner is Color.white:
        msg = '<{w_url}|{w_name}> (W) defeated <{b_url}|{b_name}> (B)'
    else:
        msg = '<{b_url}|{b_name}> (B) defeated <{w_url}|{w_name}> (W)'
    result = (msg + ' at {handicap} stones, {komi}.5 komi at <!date^{date_val}'
              '^{{time}} on {{date_num}}|{date_string}> '
              '(S{season:0>2}E{episode:0>2})')

    # Gross hack around the fact that we retrieve as naive DateTimes.
    # See: https://github.com/massgo/league/issues/93
    utc_time = int(game.played_at.replace(tzinfo=timezone.utc).timestamp())

    return result.format(w_name=game.white.full_name,
                         w_url=url_for('dashboard.get_player',
                                       player_id=game.white.id, _external=True),
                         b_name=game.black.full_name,
                         b_url=url_for('dashboard.get_player',
                                       player_id=game.black.id, _external=True),
                         handicap=game.handicap,
                         komi=game.komi,
                         date_string=game.played_at,
                         date_val=utc_time,
                         season=game.season,
                         episode=game.episode)


@blueprint.route('/games/', methods=['PATCH'])
@login_required
def update_game():
    """Update an existing game."""
    form = GameUpdateForm(request.form)
    _set_game_create_choices(form)
    if form.validate_on_submit():
        white = Player.get_by_id(form.white_id.data)
        black = Player.get_by_id(form.black_id.data)
        played_at = None
        if form.played_at.data is not None:
            played_at = form.played_at.data.astimezone(timezone.utc)
        game = Game.get_by_id(form.game_id.data)
        game.update(
            white=white,
            black=black,
            winner=form.winner.data,
            handicap=form.handicap.data,
            komi=form.komi.data,
            season=form.season.data,
            episode=form.episode.data,
            played_at=played_at
        )
        return jsonify(game.to_dict()), 200
    else:
        return jsonify(**form.errors), 404


@blueprint.route('/games/<int:game_id>', methods=['DELETE'])
@login_required
@csrf_protect.exempt
def delete_game(game_id):
    """Delete a game."""
    game = Game.get_by_id(game_id)
    if game is not None:
        game.delete()
        return '', 204
    else:
        return '', 404
