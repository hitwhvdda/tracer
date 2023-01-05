#!/bin/bash

PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"
RESULT_DIR=$PROJECT_HOME/result

CONTAINER_IMAGE=$(docker run -i --rm --detach prosyslab/bug-bench-base)

docker exec $CONTAINER_IMAGE apt update
docker exec $CONTAINER_IMAGE apt list >$RESULT_DIR/bug-bench-base-apt-list.txt

docker kill $CONTAINER_IMAGE
