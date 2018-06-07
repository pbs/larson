#!/bin/bash
set -euo pipefail
IFS=$'\n\t\ '

cd "$( dirname "${BASH_SOURCE[0]}" )/.."

python setup.py sdist bdist_wheel
twine upload dist/*
