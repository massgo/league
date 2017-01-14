# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, render_template, request

from league.utils import admin_required, flash_errors

from .forms import CreateUserForm, DeleteUsersForm
from .models import User

blueprint = Blueprint('admin', __name__, url_prefix='/admin',
                      static_folder='../static')


@blueprint.route('/users/', methods=['GET', 'POST'])
@admin_required
def list_and_delete_users():
    """List and delete users."""
    data = {'row_objects': User.get()}
    form = DeleteUsersForm(request.form, data=data)
    if form.validate_on_submit():
        user_ids = form.table.data
        User.delete_by_id(user_ids)
        flash('Users {} deleted!'.format(user_ids), 'success')
    else:
        flash_errors(form)

    return render_template('admin/users.html', delete_users_form=form)


@blueprint.route('/create_user/', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create new user."""
    form = CreateUserForm()
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
