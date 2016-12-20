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
        'aga_id', validators=[DataRequired(), NumberRange(0, 50000)])


class GameCreateForm(Form):
    """Game creation form."""

    white_id = IntegerField(
        'white_id', validators=[DataRequired(), NumberRange(0, 50000)])
    black_id = IntegerField(
        'black_id', validators=[DataRequired(), NumberRange(0, 50000)])
    winner = StringField(
        'winner', validators=[DataRequired(), AnyOf(
            [name for name, member in Color.__members__.items()])])
    handicap = IntegerField(
        'handicap', validators=[DataRequired(), NumberRange(0, 9)])
    komi = IntegerField(
        'komi', validators=[DataRequired(), AnyOf([0, 5, 6, 7])])
