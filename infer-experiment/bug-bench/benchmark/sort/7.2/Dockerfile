FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget

COPY build.sh $SRC

ENV PROGRAM=sort
ENV VERSION=7.2

RUN mkdir $PROGRAM

ENV URL=https://ftp.gnu.org/gnu/coreutils/coreutils-$VERSION.tar.gz

RUN wget $URL
RUN tar -xzvf coreutils-$VERSION.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
