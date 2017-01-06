# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, render_template, request

from league.utils import admin_required, flash_errors

from .forms import CreateUserForm, DeleteUsersForm, UserForm
from .models import User

blueprint = Blueprint('admin', __name__, url_prefix='/admin',
                      static_folder='../static')


@blueprint.route('/users/')
@admin_required
def list_users():
    """List users."""
    # form = DeleteUsersForm(request.form)
    # users = User.query.all()
    # for user in users:
    #     form.users.append_entry(UserForm())
    form = UserForm(request.form)
    return render_template('admin/users.html', delete_users_form=form)


@blueprint.route('/users/delete', methods=['POST'])
@admin_required
def delete_users():
    """Delete users."""
    if form.validate_on_submit():
        users_ids_to_delete = form.user_ids.data
        flash('Users {} deleted!'.format(users_ids_to_delete), 'success')
    else:
        flash_errors(form)
    users = User.query.all()


@blueprint.route('/create_user/', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create new user."""
    form = CreateUserForm(request.form)
    if form.validate_on_submit():
        User.create(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data, email=form.email.data,
                    password=form.password.data, is_admin=form.is_admin.data,
                    active=True)
        flash('User created!', 'success')
    else:
        flash_errors(form)
    return render_template('admin/create_user.html', create_user_form=form)


@blueprint.route('/')
@admin_required
def settings():
    """Admin settings."""
    return render_template('admin/settings.html')
