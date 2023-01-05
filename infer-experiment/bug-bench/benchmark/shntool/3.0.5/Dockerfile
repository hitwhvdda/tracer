FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget

COPY build.sh $SRC

ENV PROGRAM=shntool
ENV VERSION=3.0.5

RUN mkdir $PROGRAM

ENV URL=http://shnutils.freeshell.org/shntool/dist/src/shntool-3.0.5.tar.gz

RUN wget $URL
RUN tar -xzvf $PROGRAM-$VERSION.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
