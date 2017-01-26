#! /bin/bash

APP_DIR=app
APP_FILE=autoapp.py

pushd $APP_DIR
FLASK_APP=$APP_FILE flask assets build
popd
