#!/bin/bash

function copy_lib {
  cp -R ../lib "../packages/$1/lib"
}

if [ -f ../packages/portfolio/search/__main__.py ]; then
  copy_lib portfolio/search
fi

if [ -f ../packages/portfolio/view/__main__.py ]; then
  copy_lib portfolio/view
fi
