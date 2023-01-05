#!/usr/bin/env bash

PROJECT_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"
cd $PROJECT_HOME
mkdir -p benchmark

pushd benchmark

if [[ ! -d grpc-1.31.1 ]]; then
  git clone -b v1.31.1 https://github.com/grpc/grpc grpc-1.31.1
  pushd grpc-1.31.1
  git submodule update --init
  mkdir -p cmake/build && pushd cmake/build
  infer compile -- cmake ../..
  infer capture -- make -j
  popd
  popd
fi

if [[ ! -d protobuf-3.13.0 ]]; then
  git clone -b v3.13.0 https://github.com/protocolbuffers/protobuf protobuf-3.13.0
  pushd protobuf-3.13.0
  git submodule update --init --recursive
  ./autogen.sh
  ./configure
  infer capture -- make
  popd
fi

if [[ ! -d fontdiff-0.2.3 ]]; then
  git clone --recursive -b v0.2.3 https://github.com/googlefonts/fontdiff fontdiff-0.2.3
  pushd fontdiff-0.2.3
  ./src/third_party/gyp/gyp -f make --depth . --generator-output build src/fontdiff/fontdiff.gyp
  pushd build
  infer capture -- make
  popd
  popd
fi

if [[ ! -d googletest-1.10.0 ]]; then
  git clone -b release-1.10.0 https://github.com/google/googletest googletest-1.10.0
  pushd googletest-1.10.0
  mkdir mybuild
  pushd mybuild
  infer compile -- cmake -Dgtest_build_samples=ON ..
  infer capture -- make
  popd
  popd
fi

if [[ ! -d flatbuffers-1.12.0 ]]; then
  git clone -b v1.12.0 https://github.com/google/flatbuffers flatbuffers-1.12.0
  pushd flatbuffers-1.12.0
  infer compile -- cmake .
  infer capture -- make
  popd
fi
