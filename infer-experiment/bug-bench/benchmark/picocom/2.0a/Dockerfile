FROM prosyslab/bug-bench-base

RUN apt-get -y update

COPY build.sh $SRC
ENV PROGRAM=picocom

ENV URL=https://github.com/prosyslab-warehouse/picocom-2.0a
ENV GIT_REPO_NAME=picocom-2.0a

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
