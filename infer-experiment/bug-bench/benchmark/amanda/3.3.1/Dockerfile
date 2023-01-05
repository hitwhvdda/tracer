FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get install -y libglib2.0-dev

COPY build.sh $SRC
ENV PROGRAM=amanda

ENV URL=https://github.com/prosyslab-warehouse/amanda-3.3.1
ENV GIT_REPO_NAME=amanda-3.3.1

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
