#! /bin/bash

APP_DIR=app

npm install -g bower

pushd $APP_DIR
bower install --force
pip install -r requirements/release.txt
popd
