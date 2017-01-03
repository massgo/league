#! /bin/sh

export FLASK_APP=autoapp.py

while true
do
    rm -rf migrations && flask db init && flask db migrate && flask db upgrade && break
    sleep 1
done

uwsgi -s /tmp/uwsgi/uwsgi.sock --plugin python3 --manage-script-name --mount /=autoapp:app
