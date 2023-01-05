#!/usr/bin/env bash

./configure

if [[ $1 == "sparrow" ]]; then
  $SMAKE_BIN --init
  $SMAKE_BIN -j
  cp sparrow/src/a2ps/*.i $SMAKE_OUT
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- make -j
  cp -r infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
