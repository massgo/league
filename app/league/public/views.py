# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, logout_user

from league.admin.models import User
from league.extensions import login_manager
from league.public.forms import LoginForm

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET'])
def home():
    """Home page."""
    return redirect(url_for('dashboard.dashboard'))


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', login_form=form)
