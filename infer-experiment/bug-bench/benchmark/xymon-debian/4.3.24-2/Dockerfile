FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install libpcre3-dev libssl-dev libc-ares-dev librrd-dev yp-tools

COPY build.sh $SRC

ENV URL=https://github.com/prosyslab-warehouse/xymon-debian-4.3.24-2.git
ENV PROGRAM=xymon-debian-4.3.24-2

RUN git clone $URL

WORKDIR $PROGRAM