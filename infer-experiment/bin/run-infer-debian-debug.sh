#!/usr/bin/env bash

usage() {
  echo >&2 "Usage: ./$(basename "$0") -p PACKAGE -o OUT_DIR"
}

PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"
INFER_DIR=$PROJECT_HOME/infer

OUT_DIR=$(pwd)

while getopts ":p:o:" opt; do
  case $opt in
  p)
    PACKAGE=$OPTARG
    ;;
  o)
    OUT_DIR=$(readlink -e $OPTARG)
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
  echo >&2 "Output directory is not exist!"
  usage
  exit 1
fi

DOCKER_IMAGE=prosyslab/bug-bench-base

CONTAINER_IMAGE=$(docker run --rm -i -v $INFER_DIR/:/infer --detach $DOCKER_IMAGE)

BUILD=/src/build-deb.sh

docker exec $CONTAINER_IMAGE $BUILD $PACKAGE

RESULT_DIR=$OUT_DIR/$PACKAGE

mkdir $RESULT_DIR

pushd $RESULT_DIR

docker cp $CONTAINER_IMAGE:/src .
docker stop $CONTAINER_IMAGE

popd
