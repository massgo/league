#! /bin/bash

APP=league_app
DB=league_db
WEB=league_webserver
REPO=055326413375.dkr.ecr.us-east-1.amazonaws.com
VERSION=$(cat VERSION)

if [ "$TRAVIS_PULL_REQUEST" == "false" ] && [ "$TRAVIS_BRANCH" == "master" ] && [ -n "$TRAVIS_TAG" ]; then
    docker tag $APP:latest $REPO/$APP:$VERSION
    docker tag $DB:latest $REPO/$DB:$VERSION
    docker tag $WEB:latest $REPO/$WEB:$VERSION

    docker push $REPO/$APP:$VERSION
    docker push $REPO/$DB:$VERSION
    docker push $REPO/$WEB:$VERSION
fi
