#!/usr/bin/env bash

root_path=$(realpath $(dirname $(realpath $0))/../)

export CONFIG_FILE=$root_path/config.json
export FLASK_APP=$root_path/dream/server/__init__.py

python3.6 -m flask run -h 0.0.0.0 -p 10000
