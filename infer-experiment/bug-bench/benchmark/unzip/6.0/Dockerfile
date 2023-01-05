FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget

COPY build.sh $SRC

ENV PROGRAM=unzip

RUN mkdir $PROGRAM

ENV URL=http://downloads.sourceforge.net/infozip/unzip60.tar.gz

RUN wget $URL
RUN tar -xzvf unzip60.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
