#!/usr/bin/env bash

./configure

if [[ $1 == "sparrow" ]]; then
  $SMAKE_BIN --init
  $SMAKE_BIN -j
  cp sparrow/src/cflow/*.i $SMAKE_OUT
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- make -j
  mv infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
