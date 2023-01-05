FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget libglib2.0-dev

COPY build.sh $SRC

ENV PROGRAM=libslirp
ENV VERSION=4.1.0

RUN mkdir $PROGRAM

ENV URL=https://gitlab.freedesktop.org/slirp/libslirp/-/archive/v4.1.0/libslirp-v4.1.0.tar.gz

RUN wget $URL
RUN tar -xzvf $PROGRAM-v$VERSION.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
