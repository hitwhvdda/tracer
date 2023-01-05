FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install tzdata wget cmake

COPY build.sh $SRC
ENV PROGRAM=openjpeg

ENV URL=https://github.com/prosyslab-warehouse/openjpeg-2.2.0
ENV GIT_REPO_NAME=openjpeg-2.2.0

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
