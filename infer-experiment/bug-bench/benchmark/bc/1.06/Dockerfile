FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget flex

COPY build.sh $SRC

ENV PROGRAM=bc

RUN mkdir $PROGRAM

ENV URL=https://ftp.gnu.org/gnu/bc/bc-1.06.tar.gz

RUN wget $URL
RUN tar -xvzf bc-1.06.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
