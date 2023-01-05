FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget bison flex swig libpython2-dev

COPY build.sh $SRC
ENV PROGRAM=u-boot

ENV URL=https://github.com/prosyslab-warehouse/u-boot-2019.07
ENV GIT_REPO_NAME=u-boot-2019.07

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
