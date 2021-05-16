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

[pretrained model](https://pan.baidu.com/s/1QVYDbcsr7mspHZHII0c0aQ)(MM:ydtv)

[imagenet pretrained resnett101](https://pan.baidu.com/s/1QVYDbcsr7mspHZHII0c0aQ)(MM:ydtv)

## Evaluation<br>
bash job_evaluate_val.sh<br>

## Training<br>
bash job_train_ge_multi.sh<br>

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
