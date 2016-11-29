===============================
League
===============================

.. image:: https://travis-ci.org/massgo/league.svg?branch=master
    :target: https://travis-ci.org/massgo/league
    :alt: Build Status

.. image:: https://pyup.io/repos/github/massgo/league/shield.svg
    :target: https://pyup.io/repos/github/massgo/league/
    :alt: Updates

.. image:: https://pyup.io/repos/github/massgo/league/python-3-shield.svg
    :target: https://pyup.io/repos/github/massgo/league/
    :alt: Python 3

A go league app.


Quickstart
----------

Install system deps ::

    brew install pyenv pyenv-virtualenv npm
    pyenv install 3.4.5
    pyenv virtualenv 3.4.5 league
    npm install -g bower

Set your app's secret key as an environment variable. For example,
add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export LEAGUE_SECRET='something-really-secret'

Before running shell commands, set the ``FLASK_APP`` and ``FLASK_DEBUG``
environment variables ::

    export FLASK_APP=/path/to/autoapp.py
    export FLASK_DEBUG=1

Then run the following commands to bootstrap your environment ::

    git clone https://github.com/hndrewaall/league
    cd league
    pyenv activate league
    pip install -r requirements/dev.txt
    flask run

You will see a pretty welcome screen.

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration ::

    flask db init
    flask db migrate
    flask db upgrade
    flask run


Deployment
----------

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``, so that ``ProdConfig`` is used.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.
