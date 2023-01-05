FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget libtool m4 automake bison flex

COPY build.sh $SRC
ENV PROGRAM=libming

RUN mkdir $PROGRAM

ENV URL=https://github.com/libming/libming/archive/ming-0_4_8.tar.gz

RUN wget $URL
RUN tar -xzvf ming-0_4_8.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
