FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install libncurses-dev

COPY build.sh $SRC
ENV PROGRAM=vim

ENV URL=https://github.com/vim/vim.git
ENV GIT_REPO_NAME=vim-latest

RUN git clone --depth=1 $URL $GIT_REPO_NAME
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
