# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import IntegerField, StringField
from wtforms.validators import AnyOf, DataRequired, NumberRange

from league.dashboard.models import Color


class PlayerCreateForm(Form):
    """Player creation form."""

    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    aga_id = IntegerField(
        'aga_id', validators=[NumberRange(0, 50000)])
    aga_rank = IntegerField(
        'aga_rank', validators=[NumberRange(-30, 9)])


class PlayerDeleteForm(Form):
    """Player deletion form."""

    player_id = IntegerField('player_id', validators=[NumberRange(0, 50000)])


class GameDeleteForm(Form):
    """Game deletion form."""

    game_id = IntegerField('game_id', validators=[NumberRange(0, 50000)])


class GameCreateForm(Form):
    """Game creation form."""

    white_id = IntegerField(
        'white_id', validators=[NumberRange(0, 50000)])
    black_id = IntegerField(
        'black_id', validators=[NumberRange(0, 50000)])
    winner = StringField(
        'winner', validators=[AnyOf(
            [name for name, member in Color.__members__.items()])])
    handicap = IntegerField(
        'handicap', validators=[NumberRange(0, 9)])
    komi = IntegerField(
        'komi', validators=[AnyOf([0, 5, 6, 7])])
