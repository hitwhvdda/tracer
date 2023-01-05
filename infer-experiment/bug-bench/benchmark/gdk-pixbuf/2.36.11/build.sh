#!/usr/bin/env bash

./autogen.sh

if [[ $1 == "sparrow" ]]; then
  echo "Sparrow not supported"
  exit 1
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- make $MAKE_PARAMS
  cp -r infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
