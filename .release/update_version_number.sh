#!/bin/bash

# This script has to be called from the root of the repository

if [[ $# -eq 0 ]] ; then
    echo "Usage: $0 <VERSION_NUMBER>"
    exit 0
fi

VERSION=${1}

# # RidgeRun Microservices Utils v
sed -i "s/# RidgeRun Microservices Utils v[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+/# RidgeRun Microservices Utils v${VERSION}/g" README.md
#version="a.b.c"
sed -i "s/version=\"[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+\"/version=\"${VERSION}\"/g" setup.py
# release = 'a.b.c'
sed -i "s/release = '[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+'/release = '${VERSION}'/g" docs/source/conf.py
# Welcome to RRMS-Utils documentation va.b.c
sed -i "s/Welcome to RRMS-Utils documentation v[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+/Welcome to RRMS-Utils documentation v${VERSION}/g" docs/source/index.rst
