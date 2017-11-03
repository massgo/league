# -*- coding: utf-8 -*-
"""Test forms."""

from league.admin.forms import CreateUserForm


class TestCreateUserForm:
    """Create user form."""

    def test_validate_user_already_registered(self, user):
        """Enter username that is already registered."""
        form = CreateUserForm(username=user.username, email='foo@bar.com',
                              password='example', first_name=user.first_name,
                              last_name=user.last_name)

        assert form.validate() is False
        assert 'Username already in use' in form.username.errors

    def test_validate_email_already_registered(self, user):
        """Enter email that is already registered."""
        form = CreateUserForm(username='unique', email=user.email,
                              password='example', first_name=user.first_name,
                              last_name=user.last_name)

        assert form.validate() is False
        assert 'Email already in use' in form.email.errors

    def test_validate_success(self, db):
        """Register with success."""
        form = CreateUserForm(username='newusername', email='new@test.test',
                              password='example', first_name='Jane',
                              last_name='Doe')
        assert form.validate() is True
