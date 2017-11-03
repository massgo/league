# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for

from ..factories import UserFactory


class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_200(self, db, testapp):
        """Login successful."""
        password = 'some_test_password'
        user = UserFactory(password=password)
        # Goes to homepage
        res = testapp.get('/dashboard/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = password
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get(url_for('dashboard.dashboard'))
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow().follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.get('/dashboard/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert 'Invalid password' in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        """Show error if username doesn't exist."""
        # Goes to homepage
        res = testapp.get('/dashboard/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert 'Unknown user' in res


class TestUser:
    """Users."""

    def test_delete_user(self, testapp, authed_user):
        """Test user deletion."""
        res = testapp.get(url_for('admin.list_and_delete_users'))
        raw_form = res.html.find('form', {'id': 'deleteUsersForm'})
        found_users = [int(inp.get('value')) for inp in
                       raw_form.find_all('input', {'name': 'obj_id'})]
        assert len(found_users) == 2

        form = res.forms['deleteUsersForm']
        form.fields['obj_id'][1].checked = True
        post_res = form.submit().follow()
        assert post_res.status_code == 200

        post_raw_form = post_res.html.find('form', {'id': 'deleteUsersForm'})
        post_found_users = [int(inp.get('value')) for inp in
                            post_raw_form.find_all('input',
                                                   {'name': 'obj_id'})]
        assert len(post_found_users) == 1
