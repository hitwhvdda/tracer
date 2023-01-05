FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget g++

COPY build.sh $SRC
ENV PROGRAM=sam2p

RUN mkdir $PROGRAM

ENV URL=https://github.com/pts/sam2p/archive/v0.49.4.tar.gz

RUN wget $URL
RUN tar -xzvf v0.49.4.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM