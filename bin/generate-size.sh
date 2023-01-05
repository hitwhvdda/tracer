#!/bin/bash

find_target() {
  num_dir=$(ls -d */ | wc -l)
  if [[ $num_dir == "1" ]]; then
    cd $(ls -d */)
  else
    exit 1
  fi
}

apt update
apt source $1

find_target

rm -rf .pc

echo get-size-start
timeout 10 wc -l $(find . -name "*.[ch]")
echo get-size-ch
timeout 10 wc -l $(find . -name "*.cpp")
echo get-size-cpp
timeout 10 wc -l $(find . -name "*.cc")
echo get-size-cc
timeout 10 wc -l $(find . -name "*.vala")
echo get-size-vala
