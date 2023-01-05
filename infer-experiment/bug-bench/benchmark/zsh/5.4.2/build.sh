#!/usr/bin/env bash

./Util/preconfig
./configure --with-tcsetpgrp

MAKE_PARAMS="-j"

if [[ $1 == "sparrow" ]]; then
  $SMAKE_BIN --init
  $SMAKE_BIN $MAKE_PARAMS
  mv sparrow/src/zsh/*.i $SMAKE_OUT
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- make
  cp -r infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
