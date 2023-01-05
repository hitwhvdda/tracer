FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget

COPY build.sh $SRC
ENV PROGRAM=latex2rtf

ENV URL=https://github.com/prosyslab-warehouse/latex2rtf-2.1.1
ENV GIT_REPO_NAME=latex2rtf-2.1.1

RUN git clone $URL -b patch
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
