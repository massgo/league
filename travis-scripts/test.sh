#! /bin/bash

APP_DIR=app
APP_FILE=autoapp.py

cd $APP_DIR

export FLASK_APP=$APP_FILE
export FLASK_DEBUG=1
flask lint && flask test

exit ?!
