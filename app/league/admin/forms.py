# -*- coding: utf-8 -*-
"""Admin forms."""
from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, FieldList, FormField,
                     HiddenField, IntegerField, StringField)
from wtforms.validators import DataRequired, Email, Length, NumberRange

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


class UserForm(FlaskForm):
    selected = BooleanField()
    user_id = HiddenField()


class DeleteUsersForm(FlaskForm):
    """User deletion form."""

    users = FieldList(FormField(UserForm))

    def validate(self):
        """Check that users exist."""
        initial_validation = super().validate()
        if not initial_validation:
            return False

        valid = True
        for user in self.users.entries:
            if user.selected and User.get_by_id(user.user_id) is None:
                self.users.errors.append('User with id {} does not exist'.
                                         format(user.user_id))
                valid = False

        return valid
