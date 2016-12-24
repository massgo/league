# -*- coding: utf-8 -*-
"""Dashboard."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from league.dashboard.forms import (GameCreateForm, GameDeleteForm,
                                    PlayerCreateForm, PlayerDeleteForm)
from league.dashboard.models import Game, Player
from league.extensions import csrf_protect
from league.utils import flash_errors

blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard',
                      static_folder='../static')


@blueprint.route('/')
def dashboard():
    """Dashboard."""
    players = Player.query.all()
    return render_template('dashboard/dashboard.html', players=players)


@csrf_protect.exempt
@blueprint.route('/players/', methods=['GET'])
def get_players():
    """Get list of players."""
    form = PlayerCreateForm(request.form, csrf_enabled=False)
    players = Player.query.all()
    return render_template('dashboard/players.html', players=players,
                           player_create_form=form)


@csrf_protect.exempt
@blueprint.route('/players/', methods=['POST'])
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


@csrf_protect.exempt
@blueprint.route('/players/delete', methods=['POST'])
def delete_player():
    """Delete a player."""
    form = PlayerDeleteForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        Player.delete(Player.get_by_id(form.player_id.data))
        flash('Player deleted!', 'success')
    else:
        flash_errors(form)
    return redirect(url_for('dashboard.get_players'))


@csrf_protect.exempt
@blueprint.route('/games/', methods=['GET'])
def get_games():
    """Get list of games."""
    form = GameCreateForm(request.form, csrf_enabled=False)
    games = Game.query.all()
    return render_template('dashboard/games.html', games=games,
                           game_create_form=form)


@csrf_protect.exempt
@blueprint.route('/games/', methods=['POST'])
def create_game():
    """Create a new game."""
    form = GameCreateForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        white = Player.get_by_aga_id(form.white_id.data)
        black = Player.get_by_aga_id(form.black_id.data)
        Game.create(
            white=white,
            black=black,
            winner=form.winner.data,
            handicap=form.handicap.data,
            komi=form.komi.data,
            season=form.season.data,
            episode=form.episode.data
        )
        flash('Game created!', 'success')
    else:
        flash_errors(form)
    games = Game.query.all()
    return render_template('dashboard/games.html', games=games,
                           game_create_form=form)


@csrf_protect.exempt
@blueprint.route('/games/delete', methods=['POST'])
def delete_game():
    """Delete a game."""
    form = GameDeleteForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        Game.delete(Game.get_by_id(form.game_id.data))
        flash('Game deleted!', 'success')
    else:
        flash_errors(form)
    return redirect(url_for('dashboard.get_games'))


@csrf_protect.exempt
@blueprint.route('/reports/', methods=['GET'])
def get_reports():
    """Get results report for submission to AGA."""
    games = Game.query.all()
    players = Player.query.all()
    return render_template('dashboard/reports.html', games=games,
                           players=players)
