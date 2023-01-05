#!/usr/bin/env bash

usage() {
  echo >&2 "Usage: ./$(basename "$0") -o OUT_DIR -t TIMEOUT"
}

PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"
INFER_DIR=$PROJECT_HOME/infer

OUT_DIR=$PROJECT_HOME/result
TIMEOUT=3600

while getopts ":p:o:t:i:" opt; do
  case $opt in
    o)
      OUT_DIR=$(readlink -e $OPTARG)
      ;;
    t)
      TIMEOUT=$OPTARG
      ;;
    \?)
      echo >&2 "Invalid option -$OPTARG"
      usage
      exit 1
      ;;
    :)
      echo >&2 "Option -$OPTARG requires an argument."
      usage
      exit 1
      ;;
  esac
done

if [ ! -d "$OUT_DIR" ]; then
  echo >&2 "Output directory is not exist!"
  usage
  exit 1
fi

echo "Vim"
./bin/run-infer.sh -p vim -v latest -i "--api-misuse-only -j 20 --api-misuse-max-fp 0 --api-misuse-max-set 1 --api-misuse-max-powloc 1 --api-misuse-max-trace-set 1 --skip-files src/vim9compile.c"
echo "redis"
./bin/run-infer-debian.sh -p redis -i "--api-misuse-only -j 10 --api-misuse-max-fp 0 --api-misuse-max-set 5 --api-misuse-max-powloc 5 --api-misuse-max-trace-set 10 "
echo "git"
./bin/run-infer.sh -p git -v latest -i " --api-misuse-only -j 20 --api-misuse-max-fp 0 --api-misuse-max-set 1 --api-misuse-max-powloc 1 --api-misuse-max-trace-set 1 --skip-functions cmd_blame"
echo "python"
./bin/run-infer.sh -p python -v latest -i "--api-misuse-only -j 10 --api-misuse-max-fp 0 --api-misuse-max-set 5 --api-misuse-max-powloc 5 --api-misuse-max-trace-set 10 --skip-functions _PyEval_EvalFrameDefault"
echo "php"
./bin/run-infer.sh -p php -v latest -i "--api-misuse-only -j 20 --api-misuse-max-fp 0 --api-misuse-max-set 1 --api-misuse-max-powloc 1 --api-misuse-max-trace-set 1"
echo "emacs"
./bin/run-infer.sh -p emacs -v latest -i "--api-misuse-only -j 10 --api-misuse-max-fp 0 --api-misuse-max-set 5 --api-misuse-max-powloc 5 --api-misuse-max-trace-set 10"
echo "openssl"
./bin/run-infer-debian.sh -p openssl -i "--api-misuse-only -j 10 --api-misuse-max-fp 0 --api-misuse-max-set 5 --api-misuse-max-powloc 5 --api-misuse-max-trace-set 10"
