#!/bin/bash 

# model="mars"
model="reinvent"

nohup python -u run.py ${model} \
    --n_jobs 16 --task tune --n_runs 100 --wandb online \
    --oracles zaleplon_mpo perindopril_mpo > tune_${model}.out 2>&1 &

# CUDA_VISIBLE_DEVICES=2
