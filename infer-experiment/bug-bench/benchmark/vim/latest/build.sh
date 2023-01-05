#!/usr/bin/env bash

./configure

MAKE_PARAMS="-j"

if [[ $1 == "sparrow" ]]; then
  echo "Not implemented"
elif [[ $1 == "infer" ]]; then
  bear make $MAKE_PARAMS
  $INFER_BIN capture --compilation-database compile_commands.json
  cp -r infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
