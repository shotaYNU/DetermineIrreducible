#!/bin/sh

mkdir -p ./results/layouts
mkdir -p ./results/images

files="./results/datas/graph*.json"
for filepath in $files; do
ext=(`basename $filepath | sed 's/^.*\.\([^\.]*\)$/\1/'`)
if [ $ext = "json" ]; then
    name=(`basename $filepath | sed 's/\.[^\.]*$//'`)
    python layout_graph.py "$filepath" "./results/layouts/$name.json"
    python convert_to_eps.py "./results/layouts/$name.json" "./results/images/$name.eps"
    echo "layouted $name"
fi
done

