#!/usr/bin/env bash
# usage: bin/run-vuddy-benchmarks.sh
# description: runs vuddy for all packages listed in result/selected-packages.txt and generates output to result/vuddy-selected

PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"
BENCH_LIST=$PROJECT_HOME/result/selected-packages.txt
HMARK_DIR=$PROJECT_HOME/hmark-4.1.0
OUT_DIR=$PROJECT_HOME/result/vuddy-selected

>$OUT_DIR/log

DOCKER_IMAGE=prosyslab/bug-bench-base

initialize() {
    rm -rf $OUT_DIR
    mkdir $OUT_DIR
}

initialize

declare -a bench_list=($(cat $BENCH_LIST))

for bench in "${bench_list[@]}"; do
    echo $bench

    CONTAINER_IMAGE=$(docker run --rm -i -v $HMARK_DIR/:/hmark --detach $DOCKER_IMAGE /bin/bash)

    docker exec -i $CONTAINER_IMAGE bash -c "cd /src && \
                                            apt update && \
                                            apt source $bench && \
                                            apt install -y universal-ctags && \
                                            echo $bench > /src/benchname.txt"
    docker exec -i $CONTAINER_IMAGE bash -c 'cd /src &&
                                            name=$(ls -d */) &&
                                            cd /hmark/ &&
                                            ./hmark_4.0.1_linux_x64 -c /src/$name ON -n &&
                                            benchname=$(cat /src/benchname.txt) &&
                                            name=$(echo $name | cut -d / -f 1) &&
                                            mv /hmark/hidx/hashmark_4_$name.hidx /hmark/hidx/hashmark_4_$benchname.hidx'

    if [ $? -eq 0 ]; then
        echo "SUCCESS: $bench" >>$OUT_DIR/log
        hidx_file=$HMARK_DIR/hidx/hashmark_4_$bench.hidx
        python3 bin/analyze-hidx.py $hidx_file >$OUT_DIR/$bench.json
    else
        echo "ERROR: $bench" >>$OUT_DIR/log
    fi

    echo "exiting docker ..."
    docker stop $CONTAINER_IMAGE

done
