FROM prosyslab/bug-bench-base

RUN apt-get update
RUN apt-get -y install wget pkg-config libtool autoconf

COPY build.sh $SRC

ENV PROGRAM=fribidi

RUN mkdir $PROGRAM

ENV URL=https://github.com/fribidi/fribidi/archive/v1.0.7.tar.gz

RUN wget $URL
RUN tar -xvzf v1.0.7.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
