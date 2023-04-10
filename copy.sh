#!/bin/bash

# Usage:
# ./copy.sh dport@pi

USERNAMEHOST=$1
DEST=$2

if [ -z "$USERNAMEHOST" ]; then
    echo "Please provide a username and host, e.g. dport@pi"
    exit 1
fi

if [ -z "$DEST" ]; then
    DEST='/opt/amaranta_record'
fi

rsync --exclude .git --exclude myvenv --exclude __pycache__ -avz . $USERNAMEHOST:$DEST
