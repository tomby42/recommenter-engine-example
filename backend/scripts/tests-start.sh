#! /usr/bin/env bash
set -e
set -x

python app/tools/tests_pre_start.py

bash scripts/test.sh "$@"
