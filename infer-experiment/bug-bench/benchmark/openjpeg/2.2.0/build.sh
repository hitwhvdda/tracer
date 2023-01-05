#!/usr/bin/env bash

cmake -DCMAKE_BUILD_TYPE=Release

MAKE_PARAMS="-j"

if [[ $1 == "sparrow" ]]; then
  $SMAKE_BIN --init
  $SMAKE_BIN $MAKE_PARAMS
  mv sparrow/src/openjpeg/*.i $SMAKE_OUT
elif [[ $1 == "infer" ]]; then
  $INFER_BIN compile -- cmake ..
  $INFER_BIN capture -- make $MAKE_PARAMS
  cp -r infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
