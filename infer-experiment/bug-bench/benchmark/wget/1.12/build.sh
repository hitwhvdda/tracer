#!/usr/bin/env bash

./autogen.sh
./configure

MAKE_PARAMS="install -j"
SMAKE_I_DIR="sparrow/src/wget"

if [[ $1 == "sparrow" ]]; then
  $SMAKE_BIN --init
  $SMAKE_BIN $MAKE_PARAMS
  cp $SMAKE_I_DIR/*.i $SMAKE_OUT
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- $MAKE_PARAMS
  mv infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
