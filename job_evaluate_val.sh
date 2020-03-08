#!/bin/bash
uname -a
#date
#env
date

DATA_DIRECTORY='/home/ubuntu/zsy/human-parsing/LIP'
DATA_LIST_PATH='./dataset/list/lip/valList.txt' 
NUM_CLASSES=20 
RESTORE_FROM='./snapshots_PGECNet/PGECNet_LIP_train.pth'
SAVE_DIR='./outputs_val_LIP/' 
INPUT_SIZE='473,473'
GPU_ID=0
echo $GPU_ID
echo ${RESTORE_FROM}
CUDA_VISIBLE_DEVICES=0 python -u evaluate.py --data-dir ${DATA_DIRECTORY} \
                   --data-list ${DATA_LIST_PATH} \
                   --input-size ${INPUT_SIZE} \
                   --is-mirror \
                   --num-classes ${NUM_CLASSES} \
                   --save-dir ${SAVE_DIR} \
                   --gpu ${GPU_ID} \
                   --restore-from ${RESTORE_FROM}
                           
echo ${RESTORE_FROM}


