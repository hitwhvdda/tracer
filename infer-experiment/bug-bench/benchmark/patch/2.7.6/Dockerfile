FROM prosyslab/bug-bench-base

RUN apt-get -y update

COPY build.sh $SRC

ENV URL=https://github.com/prosyslab-warehouse/patch-2.7.6.git
ENV PROGRAM=patch-2.7.6

RUN git clone $URL

WORKDIR $PROGRAM