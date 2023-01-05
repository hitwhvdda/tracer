FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install nasm pkg-config

COPY build.sh $SRC
ENV PROGRAM=ffmpeg

ENV URL=https://github.com/FFmpeg/FFmpeg
ENV GIT_REPO_NAME=ffmpeg-latest

RUN git clone --depth=1 $URL $GIT_REPO_NAME
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
