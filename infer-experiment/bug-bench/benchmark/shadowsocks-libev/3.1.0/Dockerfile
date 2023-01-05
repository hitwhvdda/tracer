FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get install -y --no-install-recommends gettext build-essential autoconf libtool libpcre3-dev asciidoc xmlto libev-dev libc-ares-dev automake libmbedtls-dev libsodium-dev

COPY build.sh $SRC
ENV PROGRAM=shadowsocks-libev

ENV URL=https://github.com/prosyslab-warehouse/shadowsocks-libev-3.1.0
ENV GIT_REPO_NAME=shadowsocks-libev-3.1.0

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
