FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install wget

COPY build.sh $SRC

ENV PROGRAM=mp3rename

RUN mkdir $PROGRAM

ENV URL=https://launchpad.net/ubuntu/+archive/primary/+files/mp3rename_0.6.orig.tar.gz

RUN wget $URL
RUN tar -xvzf mp3rename_0.6.orig.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
