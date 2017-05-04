FROM python:3.5-alpine

RUN mkdir -p /usr/src/app

RUN apk --no-cache add ca-certificates wget

RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://github.com/sgerrand/alpine-pkg-R/releases/download/3.3.1-r0/sgerrand.rsa.pub
RUN wget https://github.com/sgerrand/alpine-pkg-R/releases/download/3.3.1-r0/R-3.3.1-r0.apk

WORKDIR /usr/src/app
ADD requirements/ /usr/src/app/requirements/

RUN apk add --no-cache --virtual .build-deps \
  build-base postgresql-dev libffi-dev libxml2-dev libxslt-dev libjpeg libjpeg-turbo-dev \
    && pip install -r requirements/production.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

ADD . /usr/src/app
#USER nobody # creating celerybeat-schedule file needs root as the emptydir is mounted as such
CMD []
