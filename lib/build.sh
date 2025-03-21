#!/bin/bash

function install_function {
  cp -R ../lib "../packages/$1/lib"
  pip install -r "../packages/$1/lib/requirements.txt"
}

if [ -f ../packages/account-balance/deposit/__main__.py ]; then
  install_function account-balance/deposit
fi

if [ -f ../packages/account-balance/view/__main__.py ]; then
  install_function account-balance/view
fi

if [ -f ../packages/portfolio/search/__main__.py ]; then
  install_function portfolio/search
fi

if [ -f ../packages/portfolio/view/__main__.py ]; then
  install_function portfolio/view
fi

if [ -f ../packages/portfolio/create/__main__.py ]; then
  install_function portfolio/create
fi

if [ -f ../packages/portfolio/update/__main__.py ]; then
  install_function portfolio/update
fi

if [ -f ../packages/portfolio/contribute/__main__.py ]; then
  copy_lib portfolio/contribute
fi

if [ -f ../packages/portfolio/follower/__main__.py ]; then
  copy_lib portfolio/follower
fi

if [ -f ../packages/portfolio/member/__main__.py ]; then
  copy_lib portfolio/member
fi

if [ -f ../packages/stock/details/__main__.py ]; then
  copy_lib stock/details
fi

if [ -f ../packages/stock/search/__main__.py ]; then
  copy_lib stock/search
fi

if [ -f ../packages/stock/transaction/__main__.py ]; then
  copy_lib stock/transaction
fi

if [ -f ../packages/stock/purchase/__main__.py ]; then
  copy_lib stock/purchase
fi

if [ -f ../packages/stock/sell/__main__.py ]; then
  copy_lib stock/sell
fi

if [ -f ../packages/stock/dailyprice/__main__.py ]; then
  copy_lib stock/dailyprice
fi