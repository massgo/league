# -*- coding: utf-8 -*-
"""Dashboard."""
from datetime import timezone
from urllib.parse import urljoin

from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import login_required, login_user

from league.dashboard.forms import (GameCreateForm, GameUpdateForm,
                                    PlayerCreateForm, PlayerDeleteForm,
                                    ReportGenerateForm)
from league.dashboard.models import Color, Game, Player
from league.dashboard.reports import Report
from league.extensions import csrf_protect, messenger
from league.public.forms import LoginForm
from league.utils import flash_errors

blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard',
                      static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
def dashboard():
    """Dashboard."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = (request.args.get('next') or
                            url_for('dashboard.dashboard'))
            return redirect(redirect_url)
        else:
            flash_errors(form)
    players = Player.query.all()
    games = Game.query.all()
    return render_template('dashboard/dashboard.html', login_form=form,
                           players=players, games=games,
                           episode_stats=Game.episode_stats())


@blueprint.route('/players/', methods=['GET'])
@login_required
def get_players():
    """Get list of players."""
    form = PlayerCreateForm(request.form)
    players = Player.query.all()
    return render_template('dashboard/players.html', players=players,
                           player_create_form=form)


@blueprint.route('/players/', methods=['POST'])
@login_required
def create_player():
    """Create a new player."""
    form = PlayerCreateForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        Player.create(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            aga_id=form.aga_id.data,
            aga_rank=form.aga_rank.data
        )
        flash('Player created!', 'success')
    else:
        flash_errors(form)
    players = Player.query.all()
    return render_template('dashboard/players.html', players=players,
                           player_create_form=form)


@blueprint.route('/players/<int:player_id>', methods=['GET'])
def get_player(player_id):
    """Get game history and statistics for player."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('public.home')
            return redirect(redirect_url)
        else:
            flash_errors(form)

    player = Player.get_by_id(player_id)

    return render_template(
        'dashboard/player.html',
        player=player,
        episode_stats=player.episode_stats(),
        season_stats=player.season_stats(),
        league_stats=player.league_stats(),
        login_form=form
    )


@blueprint.route('/players/delete/', methods=['POST'])
@login_required
def delete_player():
    """Delete a player."""
    form = PlayerDeleteForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        Player.delete(Player.get_by_id(form.player_id.data))
        flash('Player deleted!', 'success')
    else:
        flash_errors(form)
    return redirect(url_for('dashboard.get_players'))


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


@blueprint.route('/games/', methods=['GET'])
@login_required
def list_games():
    """Get list of games."""
    form = GameCreateForm(request.form, csrf_enabled=False)
    _set_game_create_choices(form)

    games = Game.query.all()
    return render_template('dashboard/games.html', games=games,
                           game_create_form=form)


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
                         w_url=urljoin(messenger.base_url,
                                       url_for('dashboard.get_player',
                                               player_id=game.white.id)),
                         b_name=game.black.full_name,
                         b_url=urljoin(messenger.base_url,
                                       url_for('dashboard.get_player',
                                               player_id=game.black.id)),
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


@blueprint.route('/reports/', methods=['GET'])
@login_required
def get_reports():
    """Get reports page."""
    form = ReportGenerateForm(request.form, csrf_enabled=False)
    return render_template('dashboard/reports.html', report_generate_form=form)


@blueprint.route('/reports/', methods=['POST'])
@login_required
def generate_report():
    """Generate results report for submission to AGA."""
    form = ReportGenerateForm(request.form, csrf_enabled=False)
    report = None
    if form.validate_on_submit():
        report = Report(form.season.data, form.episode.data)
    else:
        flash_errors(form)
    return render_template('dashboard/reports.html', report=report,
                           report_generate_form=form)
