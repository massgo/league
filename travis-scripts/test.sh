#! /bin/sh

APP_DIR=app
APP_FILE=autoapp.py

pushd $APP_DIR

export FLASK_APP=$APP_FILE
export FLASK_DEBUG=1
flask lint
flask test

popd
