FROM alpine:3.5

COPY requirements/prod.txt requirements.txt

# Stolen from https://nickjanetakis.com/blog/alpine-based-docker-images-make-a-difference-in-real-world-apps
RUN apk add --no-cache --virtual .build-deps \
        build-base postgresql-dev libffi-dev python3 python3-dev uwsgi uwsgi-python3 \
        && pip3 install -r requirements.txt \
        && find /usr/local \
            \( -type d -a -name test -o -name tests \) \
            -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
            -exec rm -rf '{}' + \
        && runDeps="uwsgi uwsgi-python3 python3 libpq $( \
            scanelf --needed --nobanner --recursive /usr/local \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
        )" \
        && apk add --virtual .rundeps $runDeps \
        && apk del .build-deps

COPY . /app
WORKDIR /app

VOLUME /tmp/uwsgi

CMD ["./migrate_and_run.sh"]
