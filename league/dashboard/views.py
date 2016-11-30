# -*- coding: utf-8 -*-
"""Dashboard."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from league.dashboard.forms import PlayerCreateForm
from league.dashboard.models import Player
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
@blueprint.route('/player/', methods=['GET', 'POST'])
def create_player():
    """Create a new player."""
    form = PlayerCreateForm(request.form, csrf_enabled=False)
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
    return redirect(url_for('dashboard.dashboard'))
