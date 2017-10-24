#!/usr/bin/env bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <adobe.xml> <poppler.xml> <adobe.pdf>"
    exit 1
fi

./extract_dtc.py $1
./extract_parts.py $1
./extract_indexes.py $2
./extract_numbers.py $2
./extract_phrases.py $3
