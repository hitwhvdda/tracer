FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install cmake

COPY build.sh $SRC
ENV PROGRAM=leptonica

ENV URL=https://github.com/prosyslab-warehouse/leptonica-1.75.2
ENV GIT_REPO_NAME=leptonica-1.75.2

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
