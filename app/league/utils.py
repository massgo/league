# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from functools import wraps

from flask import flash, request
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS

from league.extensions import login_manager


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(
                getattr(form, field).label.text, error), category)


def admin_required(func):
    """Check that user is logged in and an administrator."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        # See implementation of flask_login.utils.login_required
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not (current_user.is_authenticated and current_user.is_admin):
            return login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view
