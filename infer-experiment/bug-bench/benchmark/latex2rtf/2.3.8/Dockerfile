FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget

COPY build.sh $SRC
ENV PROGRAM=latex2rtf

RUN mkdir $PROGRAM

ENV URL=https://downloads.sourceforge.net/project/latex2rtf/latex2rtf-unix/2.3.8/latex2rtf-2.3.8.tar.gz

RUN wget $URL
RUN tar -xzvf latex2rtf-2.3.8.tar.gz -C $PROGRAM --strip-components 1

WORKDIR $PROGRAM
