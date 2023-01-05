FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install pkg-config autoconf intltool autopoint libtool libglib2.0-dev

COPY build.sh $SRC
ENV PROGRAM=autotrace

ENV URL=https://github.com/prosyslab-warehouse/autotrace-20200219.65
ENV GIT_REPO_NAME=autotrace-20200219.65

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
