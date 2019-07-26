#!/usr/bin/env bash


for pidx in 97
do
    for eidx in {1..16}
    do
        python render.py -pidx $pidx -eidx $eidx
    done
done