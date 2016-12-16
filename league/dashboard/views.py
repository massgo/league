# -*- coding: utf-8 -*-
"""Dashboard."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from league.dashboard.forms import PlayerCreateForm, GameCreateForm
from league.dashboard.models import Player, Game
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
@blueprint.route('/players/', methods=['GET', 'POST'])
def players():
    """Create a new player."""
    form = PlayerCreateForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
        if form.validate_on_submit():
            Player.create(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                aga_id=form.aga_id.data,
                rank=form.rank.data
            )
            flash('Player created!', 'success')
        else:
            flash_errors(form)
    players = Player.query.all()
    return render_template('dashboard/players.html', players=players,
                           player_create_form=form)


@csrf_protect.exempt
@blueprint.route('/games/', methods=['GET', 'POST'])
def games():
    """Create a new game."""
    form = GameCreateForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
        print(form.handicap.data)
        print(form.komi.data)
        if form.validate_on_submit():
            Game.create(
                white_id=form.white_id.data,
                black_id=form.black_id.data,
                winner=form.winner.data,
                handicap=form.handicap.data,
                komi=form.komi.data
            )
            flash('Game added!', 'success')
        else:
            flash_errors(form)
    games = Game.query.all()
    return render_template('dashboard/games.html', games=games,
                           game_create_form=form)
