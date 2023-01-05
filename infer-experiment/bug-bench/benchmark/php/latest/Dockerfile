FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install autoconf bison re2c pkg-config libxml2-dev libsqlite3-dev clang

COPY build.sh $SRC
ENV PROGRAM=php

ENV URL=https://github.com/php/php-src.git
ENV GIT_REPO_NAME=php-latest

RUN git clone --depth=1 $URL $GIT_REPO_NAME
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
