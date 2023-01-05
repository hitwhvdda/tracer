FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget autoconf libtool gnutls-dev pkg-config

COPY build.sh $SRC
ENV PROGRAM=librelp

ENV URL=https://github.com/prosyslab-warehouse/librelp-1.2.14
ENV GIT_REPO_NAME=librelp-1.2.14

RUN git clone $URL -b patch
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
