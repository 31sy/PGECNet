# PGECNet
This respository includes a PyTorch implementation of PGECNet. 

## Requirements:<br>
python 3.6<br>
PyTorch 0.4.1<br>

## Compiling<br>
InPlace-ABN have a native CUDA implementation, which must be compiled with the following commands:<br>

cd modules<br>
sh build.sh<br>
python build.py<br>

Note the CUDA kernels need to update accoding to your own gpu.<br>

## Dataset and pretrained model<br>
Plesae download [LIP](http://sysu-hcp.net/lip/overview.php) dataset<br>

[pretrained model](https://tjueducn-my.sharepoint.com/personal/zhangsanyi_tju_edu_cn/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fzhangsanyi%5Ftju%5Fedu%5Fcn%2FDocuments%2FPGECNet%5Fcode%2Fsnapshots%5FPGECNet%2FPGECNet%5FLIP%5Ftrain%2Epth&parent=%2Fpersonal%2Fzhangsanyi%5Ftju%5Fedu%5Fcn%2FDocuments%2FPGECNet%5Fcode%2Fsnapshots%5FPGECNet&originalPath=aHR0cHM6Ly90anVlZHVjbi1teS5zaGFyZXBvaW50LmNvbS86dTovZy9wZXJzb25hbC96aGFuZ3NhbnlpX3RqdV9lZHVfY24vRVl1UG5VS0gtMlJFaU1IMmQ4S043dVVCMVpKalJDT2NSNXBZNHMwdVVGRnRUdz9ydGltZT1UYWNreTFMSDEwZw)

## Evaluation<br>
bash job_evaluate_val.sh<br>

## Acknowledgment  
This project is created based on the [CE2P](https://github.com/liutinglt/CE2P).

If this code is helpful for your research, please cite the following paper:

<p>
@article{PGEC2019,<br>
  title={Human Parsing with Pyramidical Gather-Excite Context},<br>
  author={Sanyi Zhang, Guo-jun Qi, Xiaochun Cao, Zhanjie Song, Jie Zhou},<br>
  journal={IEEE Transactions on Circuits and Systems for Video Technology(TCSVT)},<br>
  year={2020}<br>
}
  </p>
