# -*- coding: utf-8 -*-
"""Admin forms."""
from collections import OrderedDict

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, FieldList, Form, FormField,
                     HiddenField, IntegerField, StringField)
from wtforms.validators import DataRequired, Email, Length, NumberRange

from league.forms import CheckboxTableField

from .models import User


class CreateUserForm(FlaskForm):
    """Create user form."""

    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=3, max=25)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(min=3, max=25)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6,
                                                                    max=40)])
    password = StringField('Password',
                           validators=[DataRequired(), Length(min=6, max=40)])
    is_admin = BooleanField('Admin?')

    def validate(self):
        """Validate the form."""
        initial_validation = super().validate()
        if not initial_validation:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already in use')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already in use')
            return False
        return True


class DeleteUsersForm(FlaskForm):
    """User deletion form."""
    columns = OrderedDict([('User Name', 'username'),
                           ('First Name', 'first_name'),
                           ('Last Name', 'last_name'),
                           ('Email', 'email')])
    table = CheckboxTableField(columns=columns, validators=[DataRequired()])

    def process(self, formdata=None, obj=None, data=None, **kwargs):
        formdata = self.meta.wrap_formdata(self, formdata)

        for field in self._fields.values():
            field.process(formdata, data)

    def validate(self):
        """Check that users exist."""
        initial_validation = super().validate()
        if not initial_validation:
            return False

        valid = True
        for user_id in self.table.data:
            if User.get_by_id(user_id) is None:
                self.table.errors.append('User with id {} does not exist',
                                         format(user_id))
                valid = False
            elif user_id == current_user.id:
                self.table.errors.append('You cannot delete yourself!')
                valid = False

        return valid
