#!/bin/sh
set -eu

ZIPNAME="carles-matoses.zip"
FILES="Assigment2-part1.ipynb low_low_resolution.nii.gz"

for f in $FILES; do
    if [ ! -e "$f" ]; then
        echo "Error: '$f' not found in $(pwd)" >&2
        exit 2
    fi
done

# create or overwrite zip
zip -r "$ZIPNAME" $FILES

echo "Created '$ZIPNAME' containing: $FILES"