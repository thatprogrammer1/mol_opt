#!/bin/bash 

model="smiles_lstm_hc"

nohup python -u run.py ${model} \
    --n_jobs 16 --task tune --n_runs 50 --wandb online \
    --oracles zaleplon_mpo perindopril_mpo > tune_${model}.out 2>&1 &

# CUDA_VISIBLE_DEVICES=0
