# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import (DateTimeField, IntegerField, SelectField, StringField,
                     ValidationError)
from wtforms.validators import DataRequired, NumberRange

from league.dashboard.models import Color, Player


class PlayerCreateForm(FlaskForm):
    """Player creation form."""

    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    aga_id = IntegerField(
        'aga_id', validators=[NumberRange(0, 50000)])
    aga_rank = IntegerField(
        'aga_rank', validators=[NumberRange(-30, 9)])


class PlayerDeleteForm(FlaskForm):
    """Player deletion form."""

    player_id = IntegerField('player_id', validators=[NumberRange(0, 50000)])

    @staticmethod
    def validate_player_id(form, field):
        """Check that players are not in extant games."""
        if len(Player.get_by_id(field.data).games) > 0:
            raise ValidationError('Players with extant games cannot be deleted')


class GameDeleteForm(FlaskForm):
    """Game deletion form."""

    game_id = IntegerField('game_id', validators=[NumberRange(0, 50000)])


class GameCreateForm(FlaskForm):
    """Game creation form."""

    white_id = SelectField('white_id', coerce=int,
                           validators=[NumberRange(0, 50000)])
    black_id = SelectField('black_id', coerce=int,
                           validators=[NumberRange(0, 50000)])
    winner = SelectField(
        'winner', choices=[(name, name) for name, member
                           in Color.__members__.items()])
    handicap = SelectField(
        'handicap', coerce=int, choices=[(handi, handi) for handi
                                         in [0, 2, 3, 4, 5, 6, 7, 8, 9]])
    komi = SelectField(
        'komi', coerce=int, choices=[(komi, komi) for komi in [0, 5, 6, 7]])
    season = SelectField('season', coerce=int,
                         validators=[NumberRange(0, 10000)])
    episode = SelectField('episode', coerce=int,
                          validators=[NumberRange(0, 10000)])
    played_at = DateTimeField()

    @staticmethod
    def validate_black_id(form, field):
        """Check that IDs are different."""
        if form.black_id.data == form.white_id.data:
            raise ValidationError('Players cannot play themselves')


class ReportGenerateForm(FlaskForm):
    """Report generation form."""

    season = IntegerField('season', validators=[NumberRange(1, 10000)])
    episode = IntegerField('episode', validators=[NumberRange(1, 10000)])
