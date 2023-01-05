FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install libssl-dev libz-dev libcurl4-openssl-dev libexpat-dev tclsh gettext

COPY build.sh $SRC
ENV PROGRAM=python

ENV URL=https://github.com/python/cpython.git
ENV GIT_REPO_NAME=python-latest

RUN git clone --depth=1 $URL $GIT_REPO_NAME
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
