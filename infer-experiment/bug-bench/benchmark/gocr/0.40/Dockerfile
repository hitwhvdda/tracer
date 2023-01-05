FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget

COPY build.sh $SRC
ENV PROGRAM=gocr

ENV URL=https://github.com/prosyslab-warehouse/gocr-0.40
ENV GIT_REPO_NAME=gocr-0.40

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
