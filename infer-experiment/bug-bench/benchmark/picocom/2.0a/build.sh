#!/usr/bin/env bash

if [[ $1 == "sparrow" ]]; then
  echo "TODO: $1"
  exit 1
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- make
  cp -r infer-out $OUT
elif [[ $1 == "codeql" ]]; then
  $CODEQL_BIN database create --language=cpp --command="make" codeql-db
  cp -r codeql-db $OUT
else
  echo "Unknown build target"
  exit 1
fi
