#!/bin/bash
uname -a
#date
#env
date

DATA_DIRECTORY='../LIP'
DATA_LIST_PATH='./dataset/list/lip/trainList.txt'
RESTORE_FROM='./dataset/MS_DeepLab_resnet_pretrained_init.pth'
SNAPSHOT_DIR='./snapshots/'
LR=7e-3
BATCHSIZE=18
STEPS=250000
SAVE_PRED_EVERY=1000
GPU_IDS='0,1'
INPUT_SIZE='473,473'
NUM_CLASSES=20  
STARTITERS=0
 
CUDA_VISIBLE_DEVICES=0,1 python -u train_ge.py --data-dir ${DATA_DIRECTORY} \
                          --data-list ${DATA_LIST_PATH} \
                          --input-size ${INPUT_SIZE} \
                          --num-classes ${NUM_CLASSES} \
                          --random-mirror \
                          --random-scale \
                          --gpu ${GPU_IDS} \
                          --learning-rate ${LR} \
                          --batch-size ${BATCHSIZE} \
                          --num-steps ${STEPS} \
                          --start-iters ${STARTITERS}\
                          --restore-from ${RESTORE_FROM} \
                          --snapshot-dir ${SNAPSHOT_DIR} \
                          --save-pred-every ${SAVE_PRED_EVERY}
