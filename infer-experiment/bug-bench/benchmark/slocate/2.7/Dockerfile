FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install tzdata wget autoconf

COPY build.sh $SRC
ENV PROGRAM=slocate

ENV URL=https://github.com/prosyslab-warehouse/slocate-2.7
ENV GIT_REPO_NAME=slocate-2.7

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
