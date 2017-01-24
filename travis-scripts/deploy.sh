#! /bin/bash

APP=league_app
DB=league_db
WEB=league_webserver
REPO=055326413375.dkr.ecr.us-east-1.amazonaws.com
VERSION=$(cat VERSION)

docker tag $APP:$VERSION $REPO/$APP:latest
docker tag $DB:$VERSION $REPO/$DB:latest
docker tag $WEB:$VERSION $REPO/$WEB:latest

$(aws ecr get-login)

docker push $REPO/$APP:$VERSION
docker push $REPO/$DB:$VERSION
docker push $REPO/$WEB:$VERSION
