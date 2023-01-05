#!/usr/bin/env bash

usage() {
  echo >&2 "Usage: ./$(basename "$0") -p PACKAGE -v VERSION -o OUT_DIR -i \"INFER_OPTIONS\""
}

PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"
INFER_DIR=$PROJECT_HOME/infer

OUT_DIR=$PROJECT_HOME/result

while getopts ":p:v:o:i:" opt; do
  case $opt in
  p)
    PACKAGE=$OPTARG
    ;;
  v)
    VERSION=$OPTARG
    ;;
  o)
    OUT_DIR=$(readlink -e $OPTARG)
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

if [ -z "$PACKAGE" ] || [ -z "$VERSION" ]; then
  echo >&2 "Package name and version must be given!"
  usage
  exit 1
fi

if [ ! -d "$OUT_DIR" ]; then
  echo >&2 "Output directory is not exist!"
  usage
  exit 1
fi

DOCKER_IMAGE=prosyslab/bug-bench-$PACKAGE:$VERSION

CONTAINER_IMAGE=$(docker run --rm -i -v $INFER_DIR/:/infer --detach $DOCKER_IMAGE)

BUILD=/src/build.sh
INFER_OUT=infer-out
OUT=/out/$INFER_OUT

docker exec $CONTAINER_IMAGE $BUILD infer

RESULT_DIR=$OUT_DIR/$PACKAGE-$VERSION

mkdir $RESULT_DIR

pushd $RESULT_DIR

docker cp $CONTAINER_IMAGE:$OUT .
docker stop $CONTAINER_IMAGE

$INFER_DIR/infer/bin/infer analyze $INFER_OPTIONS

popd
