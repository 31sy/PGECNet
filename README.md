# PGECNet
This respository includes a PyTorch implementation of PGECNet. 

Requirements:
python 3.6
PyTorch 0.4.1

Compiling
InPlace-ABN have a native CUDA implementation, which must be compiled with the following commands:

cd libs
sh build.sh
python build.py

Note the CUDA kernels need to update accoding to your own gpu.

Dataset and pretrained model
Plesae download [LIP](http://sysu-hcp.net/lip/overview.php) dataset

[pretrained model](https://tjueducn-my.sharepoint.com/personal/zhangsanyi_tju_edu_cn/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fzhangsanyi%5Ftju%5Fedu%5Fcn%2FDocuments%2FPGECNet%5Fcode%2Fsnapshots%5FPGECNet%2FPGECNet%5FLIP%5Ftrain%2Epth&parent=%2Fpersonal%2Fzhangsanyi%5Ftju%5Fedu%5Fcn%2FDocuments%2FPGECNet%5Fcode%2Fsnapshots%5FPGECNet&originalPath=aHR0cHM6Ly90anVlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC96aGFuZ3NhbnlpX3RqdV9lZHVfY24vRVl1UG5VS0gtMlJFaU1IMmQ4S043dVVCMVpKalJDT2NSNXBZNHMwdVVGRnRUdz9ydGltZT1UYWNreTFMSDEwZw)

Evaluation
bash job_evaluate_val.sh

If this code is helpful for your research, please cite the following paper:

@article{PGEC2019,
  title={Human Parsing with Pyramidical Gather-Excite Context},
  author={Sanyi Zhang, Guo-jun Qi, Xiaochun Cao, Zhanjie Song, Jie Zhou},
  journal={TCSVT, under review},
  year={2020}
}
