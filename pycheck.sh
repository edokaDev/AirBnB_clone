#!/usr/bin/env bash

pycodestyle `find ./ -type f -name "*.py" -exec echo {} \; | sed 's/ /\/\//'`
pydocstyle `find ./ -type f -name "*.py" -exec echo {} \; | sed 's/ /\/\//'`
