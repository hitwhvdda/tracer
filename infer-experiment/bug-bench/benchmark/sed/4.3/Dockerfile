FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget xz-utils autoconf texinfo

COPY build.sh $SRC

ENV PROGRAM=sed
ENV VERSION=4.3

RUN mkdir $PROGRAM

ENV URL=https://ftp.gnu.org/gnu/$PROGRAM/$PROGRAM-$VERSION.tar.xz

RUN wget $URL
RUN tar -xvf $PROGRAM-$VERSION.tar.xz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
