FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install cmake

COPY build.sh $SRC

ENV URL=https://github.com/prosyslab-warehouse/libssh-0.9.2.git
ENV PROGRAM=libssh-0.9.2

RUN git clone $URL

WORKDIR $PROGRAM