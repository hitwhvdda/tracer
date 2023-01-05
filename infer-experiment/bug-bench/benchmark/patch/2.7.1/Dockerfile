FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget xz-utils

COPY build.sh $SRC

ENV PROGRAM=patch

RUN mkdir $PROGRAM

ENV URL=https://ftp.gnu.org/gnu/patch/patch-2.7.1.tar.xz

RUN wget $URL
RUN tar -xvf patch-2.7.1.tar.xz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
