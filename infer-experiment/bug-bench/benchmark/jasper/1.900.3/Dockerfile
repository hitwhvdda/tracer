FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install autoconf libtool libjpeg-dev

COPY build.sh $SRC
ENV PROGRAM=jasper

ENV URL=https://github.com/prosyslab-warehouse/jasper-1.900.3
ENV GIT_REPO_NAME=jasper-1.900.3

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
