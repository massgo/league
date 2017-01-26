# -*- coding: utf-8 -*-
"""Admin helper utilities."""
from league.admin.models import User


def get_create_root_user(app):
    """
    Return function that creates root user.

    This is basically a hack around the fact that functions that need to be
    registered with before_first_request cannot take arguments.
    """
    def create_root_user():
        """Create root user."""
        if User.get_by_username('root') is None:
            root_user = User(username='root', email='root@localhost',
                             password=app.config['LEAGUE_ROOT_PASS'],
                             active=True,
                             is_admin=True)
            root_user.save()
    return create_root_user
