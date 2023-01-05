FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget

COPY build.sh $SRC

ENV PROGRAM=tar
ENV VERSION=1.28

RUN mkdir $PROGRAM

ENV URL=https://ftp.gnu.org/gnu/$PROGRAM/$PROGRAM-$VERSION.tar.gz
ENV FORCE_UNSAFE_CONFIGURE=1

RUN wget $URL
RUN tar -xzvf $PROGRAM-$VERSION.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
