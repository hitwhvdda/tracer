#!/usr/bin/env bash

./autogen.sh
./configure

MAKE_PARAMS="-j"

if [[ $1 == "sparrow" ]]; then
  echo "Not implemented"
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture --keep-going -- make $MAKE_PARAMS
  cp -r infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
