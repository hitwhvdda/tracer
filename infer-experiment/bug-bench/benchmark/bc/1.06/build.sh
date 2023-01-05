#!/usr/bin/env bash

./configure

if [[ $1 == "sparrow" ]]; then
  $SMAKE_BIN --init
  $SMAKE_BIN -j
  cp sparrow/bc/bc/*.i $SMAKE_OUT
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- make -j
  mv infer-out $OUT
elif [[ $1 == "codeql" ]]; then
  $CODEQL_BIN database create --language=cpp --command="make" codeql-db
  mv codeql-db $OUT
else
  echo "Unknown build target"
  exit 1
fi
