FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install automake libncurses5-dev

COPY build.sh $SRC
ENV PROGRAM=zsh

ENV URL=https://github.com/prosyslab-warehouse/zsh-5.4.2
ENV GIT_REPO_NAME=zsh-5.4.2

RUN git clone $URL -b patch
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
