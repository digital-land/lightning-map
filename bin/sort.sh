#!/bin/sh
head -1 "$1"
cat "$@" | grep -v "^@timestamp" | sort
