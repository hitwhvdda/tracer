FROM ubuntu:20.04

# basic setting
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV SRC=/src
ENV OUT=/out
RUN mkdir -p $SRC $OUT/smake-out

ENV BUILD=/src/build.sh

# Sparrow
ENV SMAKE_DIR=/smake
ENV SMAKE_BIN=$SMAKE_DIR/smake
ENV SMAKE_OUT=$OUT/smake-out

# Infer
ENV INFER_DIR=/infer
ENV INFER_BIN=$INFER_DIR/infer/bin/infer

# CodeQL
ENV CODEQL_DIR=/codeql
ENV CODEQL_BIN=$CODEQL_DIR/codeql

# for debian package build
ENV DEB_BUILD_OPTIONS="nocheck notest"
RUN sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
COPY build-deb.sh $SRC

RUN apt-get update && \
    apt-get upgrade -y
RUN apt-get install -y make git gcc tzdata bear dpkg-dev libtinfo5

RUN git clone https://github.com/prosyslab/smake.git

WORKDIR $SRC
