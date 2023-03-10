#!/usr/bin/env bash

cp unix/Makefile .

MAKE_PARAMS="generic -j"
SMAKE_I_DIR="sparrow/unzip"

if [[ $1 == "sparrow" ]]; then
  $SMAKE_BIN --init
  $SMAKE_BIN $MAKE_PARAMS
  cp $SMAKE_I_DIR/*.i $SMAKE_OUT
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- make $MAKE_PARAMS
  cp -r infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
