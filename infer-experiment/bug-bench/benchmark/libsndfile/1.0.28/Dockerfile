FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget automake pkg-config python libtool autogen

COPY build.sh $SRC

ENV PROGRAM=libsndfile

RUN mkdir $PROGRAM

ENV URL=https://github.com/libsndfile/libsndfile/archive/refs/tags/1.0.28.tar.gz

RUN wget $URL
RUN tar -xzvf 1.0.28.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
