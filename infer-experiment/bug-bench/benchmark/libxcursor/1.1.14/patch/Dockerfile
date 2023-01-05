FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install autoconf xutils-dev libtool pkgconf libx11-dev libxrender-dev libxcursor-dev systemd

COPY build.sh $SRC
ENV PROGRAM=libxcursor

ENV URL=https://github.com/prosyslab-warehouse/libXcursor-1.1.14
ENV GIT_REPO_NAME=libXcursor-1.1.14

RUN git clone $URL -b patch
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
