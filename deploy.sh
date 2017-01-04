#! /bin/sh

APP=league_app
DB=league_db
WEB=league_webserver
REPO=055326413375.dkr.ecr.us-east-1.amazonaws.com

docker tag $APP:latest $REPO/$APP:latest
docker tag $DB:latest $REPO/$DB:latest
docker tag $WEB:latest $REPO/$WEB:latest

$(aws ecr get-login)

docker push $REPO/$APP:latest
docker push $REPO/$DB:latest
docker push $REPO/$WEB:latest
