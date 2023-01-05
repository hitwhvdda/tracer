#!/usr/bin/env bash

./configure

MAKE_PARAMS="-j"

if [[ $1 == "sparrow" ]]; then
  $SMAKE_BIN --init
  $SMAKE_BIN $MAKE_PARAMS
  mv sparrow/src/jtag/*.i $SMAKE_OUT
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- make $MAKE_PARAMS
  cp -r infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
