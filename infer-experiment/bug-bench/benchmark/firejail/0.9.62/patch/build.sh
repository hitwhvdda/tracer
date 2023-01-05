#!/usr/bin/env bash

CC=clang ./configure

if [[ $1 == "sparrow" ]]; then
  echo "TODO: $1"
  exit 1
elif [[ $1 == "infer" ]]; then
  # only capture src/firejail because Infer does not work well with multiple functions with the same name (e.g., main)
  $INFER_BIN capture -- make src/firejail/firejail -j
  cp -r infer-out $OUT
elif [[ $1 == "codeql" ]]; then
  $CODEQL_BIN database create --language=cpp --command="make" codeql-db
  cp -r codeql-db $OUT
else
  echo "Unknown build target"
  exit 1
fi
