#!/usr/bin/env bash

echo "CONFIG_CMD_NFS=y" >>configs/qemu-x86_64_defconfig
make qemu-x86_64_defconfig

if [[ $1 == "sparrow" ]]; then
  echo "Sparrow not supported"
  exit 1
elif [[ $1 == "infer" ]]; then
  $INFER_BIN capture -- make $MAKE_PARAMS
  cp -r infer-out $OUT
else
  echo "Unknown build target"
  exit 1
fi
