#! /bin/bash

APP_DIR=app

pushd $APP_DIR
bower install --force
pip install -r requirements/release.txt
popd
