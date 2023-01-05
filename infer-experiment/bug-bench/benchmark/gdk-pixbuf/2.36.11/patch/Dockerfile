FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install wget gtk-doc-tools autoconf autopoint libtool libglib2.0-dev libtiff-dev libpng-dev
COPY build.sh $SRC
ENV PROGRAM=gdk-pixbuf

ENV URL=https://github.com/prosyslab-warehouse/gdk-pixbuf-2.36.11
ENV GIT_REPO_NAME=gdk-pixbuf-2.36.11

RUN git clone $URL -b patch
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
