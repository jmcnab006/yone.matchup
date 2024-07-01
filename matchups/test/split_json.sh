#!/bin/bash

# Split a JSON into multiple files. Uses jq.

# Usage
# ./split_json.sh /path/to/json/file

file="$1"

#jq . -cr 'keys[] as $k | "\($k)\t\(.[$k])"' "$file"  | awk -F\\t '{ file=$1".json"; print $2 > file; close(file); }'
#jq -r 'keys[] as $k | "\($k)\t\(.[$k])"' "$file" | awk -F\\t '{ file=$1".json"; print $2 > file; close(file); }'
#jq -r 'keys[] as $k | "\($k)\t\(.[$k])"' "$file" #| awk -F\\t '{ file=$1".json"; print $2 system( jq .) > file; close(file); }'
#jq -r 'keys[] as $k | "\($k)\t\(.[$k])"' "$file" | awk -F\\t '{ f=$1".json"; printf "%s", $2 | "jq" > f; }'
jq -r 'keys[] as $k | "\($k)\t\(.[$k])"' "$file" | awk -F\\t '{ f=$1".json"; print $2 | "jq >" f; }'
