#!/usr/bin/env bash


for pidx in 1
do
    for eidx in 13
    do
        python crop.py -pidx $pidx -eidx $eidx
    done
done
