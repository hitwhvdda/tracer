FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install glib2.0-dev libgtk2.0-dev

COPY build.sh $SRC
ENV PROGRAM=gimp

ENV URL=https://github.com/prosyslab-warehouse/gimp-2.6.7
ENV GIT_REPO_NAME=gimp-2.6.7

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
