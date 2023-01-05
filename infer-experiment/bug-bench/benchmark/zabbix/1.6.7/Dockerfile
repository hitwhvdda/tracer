FROM prosyslab/bug-bench-base

RUN apt-get -y update
RUN apt-get -y install libmysql++-dev

COPY build.sh $SRC
ENV PROGRAM=zabbix

ENV URL=https://github.com/prosyslab-warehouse/zabbix-1.6.7
ENV GIT_REPO_NAME=zabbix-1.6.7

RUN git clone $URL
RUN mv $GIT_REPO_NAME $PROGRAM

WORKDIR $PROGRAM
