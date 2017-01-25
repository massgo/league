#! /bin/bash

APP=league_app
DB=league_db
WEB=league_webserver
REPO=055326413375.dkr.ecr.us-east-1.amazonaws.com

docker pull $REPO/$APP:latest
docker pull $REPO/$DB:latest
docker pull $REPO/$WEB:latest

docker-compose build
