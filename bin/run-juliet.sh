#!/usr/bin/env bash

set -e

PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"
JULIET_DIR=$PROJECT_HOME/juliet-test-suite-c
INFER_DIR=$PROJECT_HOME/infer

TEST_FILE=$1

COMPILE_CMD="clang -I juliet-test-suite-c/testcasesupport -D INCLUDEMAIN $JULIET_DIR/testcasesupport/io.c $TEST_FILE"

$INFER_DIR/infer/bin/infer run --api-misuse-only -- $COMPILE_CMD
