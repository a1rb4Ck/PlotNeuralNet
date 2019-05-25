#!/usr/bin/env bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

bash -c "python main.py"
bash -c "$BASEDIR/../../../tikzmake.sh main"