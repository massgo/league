#! /bin/sh

APP_DIR=app
APP_FILE=autoapp.py

pushd $APP_DIR
bower install --force
FLASK_APP=$APP_FILE flask assets build
popd

docker-compose build
