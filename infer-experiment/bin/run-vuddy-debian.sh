#!/usr/bin/env bash

usage() {
  echo >&2 "Usage: ./bin/$(basename "$0") -p PACKAGE -o OUT_DIR -v PATH_TO_VULN_HIDX"
}

PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"

HMARK_DIR=$PROJECT_HOME/hmark

OUT_DIR=$PROJECT_HOME/result

while getopts ":p:o:v:t:i:" opt; do
  case $opt in
  p)
    PACKAGE=$OPTARG
    ;;
  o)
    OUT_DIR=$(readlink -e $OPTARG)
    ;;
  v)
    VULN_HIDX=$OPTARG
    ;;
  t)
    TIMEOUT=$OPTARG
    ;;
  i)
    INFER_OPTIONS=$OPTARG
    ;;
  \?)
    echo >&2 "Invalid option -$OPTARG"
    usage
    exit 1
    ;;
  :)
    echo >&2 "Option -$OPTARG requires an argument."
    usage
    exit 1
    ;;
  esac
done

if [ -z "$PACKAGE" ]; then
  echo >&2 "Package name must be given!"
  usage
  exit 1
fi

if [ ! -d "$OUT_DIR" ]; then
  echo >&2 "Output directory does not exist!"
  usage
  exit 1
fi

DOCKER_IMAGE=prosyslab/bug-bench-base

CONTAINER_IMAGE=$(docker run --rm -i -v $HMARK_DIR/:/hmark --detach $DOCKER_IMAGE /bin/bash)

docker exec -i $CONTAINER_IMAGE bash -c "apt source $PACKAGE && echo $PACKAGE > pkgname.txt"
docker exec -i $CONTAINER_IMAGE bash -c 'name=$(ls -d */) && \
                                         cd /hmark/hmark-3.1.0/hmark && \
                                         apt install -y python openjdk-16-jre && \
                                         python hmark.py -c /src/$name ON -n && \
                                         pkgname=$(cat /src/pkgname.txt) && \
                                         name=$(echo $name | cut -d / -f 1) && \
                                         mv /hmark/hmark-3.1.0/hmark/hidx/hashmark_4_$name.hidx /hmark/hmark-3.1.0/hmark/hidx/hashmark_4_$pkgname.hidx'

docker cp $CONTAINER_IMAGE:/hmark/hmark-3.1.0/hmark/hidx/hashmark_4_$PACKAGE.hidx $OUT_DIR/hashmark_4_$PACKAGE.hidx

if [ $? -eq 0 ]; then
  echo "hidx saved at $OUT_DIR/hashmark_4_$PACKAGE.hidx"
  python3 $PROJECT_HOME/bin/run-vuddy.py $VULN_HIDX $OUT_DIR/hashmark_4_$PACKAGE.hidx >>$OUT_DIR/result
else
  echo "failed to generate hidx.. maybe hmark doens't support the languages in $PACKAGE"
fi

echo "exiting docker ..."
docker stop $CONTAINER_IMAGE
