# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import Form
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange


class PlayerCreateForm(Form):
    """Player creation form."""

    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    aga_id = IntegerField('aga_id',
                          validators=[DataRequired(), NumberRange(0, 50000)])
    rank = IntegerField('aga_id',
                        validators=[DataRequired(), NumberRange(-30, 9)])
