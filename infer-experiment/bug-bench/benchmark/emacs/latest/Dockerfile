FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install autoconf texinfo pkg-config libgnutls28-dev libtinfo-dev

COPY build.sh $SRC
ENV PROGRAM=emacs

ENV URL=https://github.com/emacs-mirror/emacs.git
ENV GIT_REPO_NAME=emacs-latest

RUN git clone --depth=1 $URL $GIT_REPO_NAME
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
