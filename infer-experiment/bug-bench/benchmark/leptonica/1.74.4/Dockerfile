FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install cmake

COPY build.sh $SRC

ENV URL=https://github.com/prosyslab-warehouse/leptonica-1.74.4.git
ENV PROGRAM=leptonica-1.74.4

RUN git clone $URL

WORKDIR $PROGRAM