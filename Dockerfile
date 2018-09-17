FROM python:3.6

RUN apt-get update && \
    apt-get install -y postgresql-contrib nginx supervisor gettext curl && \
    apt-get -y autoclean && \
    pip3 install uwsgi

RUN groupadd --gid 1000 node \
  && useradd --uid 1000 --gid node --shell /bin/bash --create-home node

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 10.2.1

RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash

RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

RUN npm install -g gulp bower

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

RUN mkdir -p /app/front/ && \
    mkdir -p /app/front/admin && \
    mkdir -p /app/front/site && \
    chown -R node:node /app/front/

USER node

COPY ./front/admin/package.json /app/front/admin/package.json
COPY ./front/admin/package-lock.json /app/front/admin/package-lock.json
COPY ./front/admin/gulpfile.js /app/front/admin/gulpfile.js
COPY ./front/admin/bower.json /app/front/admin/bower.json

COPY ./front/site/package.json /app/front/site/package.json
COPY ./front/site/package-lock.json /app/front/site/package-lock.json
COPY ./front/site/gulpfile.js /app/front/site/gulpfile.js
COPY ./front/site/bower.json /app/front/site/bower.json


RUN cd /app/front/admin && npm install
RUN cd /app/front/site && npm install

USER root

ENV DJANGO_LOG_FILE=logfile.log

COPY ./ /app/

RUN rm /etc/nginx/nginx.conf && \
  ln -s /app/deploy/nginx.conf /etc/nginx/ && \
  rm /etc/nginx/sites-enabled/default && \
  ln -s /app/deploy/nginx-app.conf /etc/nginx/sites-enabled/nginx-app.conf && \
  rm /etc/supervisor/supervisord.conf && \
  mkdir -p /app/data/logs && \
  mkdir -p /app/static && \
  touch /app/data/logs/$DJANGO_LOG_FILE

RUN cd /app/front/admin && gulp build
RUN cd /app/front/site && gulp build

WORKDIR /app
ENV UWSGI_TOUCH_CHAIN_RELOAD /app/touch_to_chain_reload


EXPOSE 80

VOLUME ["/app/data"]

CMD mkdir -p /app/data/logs; \
    touch /app/data/logs/$DJANGO_LOG_FILE; \
    touch $UWSGI_TOUCH_CHAIN_RELOAD; \
    supervisord -n -c /app/deploy/supervisord_web.conf