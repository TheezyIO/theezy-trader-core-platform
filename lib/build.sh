#!/bin/bash

pip install -r requirements.txt

function copy_lib {
  cp -R ../lib "../packages/$1/lib"
}

if [ -f ../packages/portfolio/search/__main__.py ]; then
  copy_lib portfolio/search
fi

if [ -f ../packages/portfolio/view/__main__.py ]; then
  copy_lib portfolio/view
fi

if [ -f ../packages/portfolio/create/__main__.py ]; then
  copy_lib portfolio/create
fi
