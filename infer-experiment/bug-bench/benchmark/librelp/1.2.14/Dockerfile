FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget autoconf libtool gnutls-dev pkg-config

COPY build.sh $SRC
ENV PROGRAM=librelp

RUN mkdir $PROGRAM

ENV URL=https://github.com/rsyslog/librelp/archive/v1.2.14.tar.gz

RUN wget $URL
RUN tar -xzvf v1.2.14.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
