#!/usr/bin/env bash

PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"
INFER_BIN=$PROJECT_HOME/infer/infer/bin/infer

if [[ -f $1 ]]; then
  $INFER_BIN run --api-misuse --no-starvation \
    --no-self-in-block --no-uninit --no-siof --no-racerd --no-liveness \
    --no-inefficient-keyset-iterator --no-fragment-retains-view \
    --no-biabduction --debug -j 1 --bo-debug 3 \
    -- clang -c $1
else
  pushd $1
  $INFER_BIN analyze --api-misuse --no-starvation \
    --no-self-in-block --no-uninit --no-siof --no-racerd --no-liveness \
    --no-inefficient-keyset-iterator --no-fragment-retains-view \
    --no-biabduction -j 1
  popd
fi
