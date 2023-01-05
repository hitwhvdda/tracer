FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget g++

COPY build.sh $SRC
ENV PROGRAM=sam2p

ENV URL=https://github.com/prosyslab-warehouse/sam2p-0.49.4

ENV GIT_REPO_NAME=sam2p-0.49.4

RUN git clone $URL -b patch
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
