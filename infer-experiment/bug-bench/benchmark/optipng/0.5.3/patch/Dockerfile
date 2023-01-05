FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget

COPY build.sh $SRC
ENV PROGRAM=optipng

ENV URL=https://github.com/prosyslab-warehouse/optipng-0.5.3
ENV GIT_REPO_NAME=optipng-0.5.3

RUN git clone $URL -b patch
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
