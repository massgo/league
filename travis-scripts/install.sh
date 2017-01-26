#! /bin/bash

APP_DIR=app

pushd $APP_DIR
npm install -g bower && bower install --force && pip install -r requirements/release.txt
popd

exit $?
