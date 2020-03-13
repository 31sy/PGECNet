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
Plesae download LIP dataset

pretrained model : 
Evaluation
bash job_evaluate_val.sh

If this code is helpful for your research, please cite the following paper:

@article{PGEC2019,
  title={Human Parsing with Pyramidical Gather-Excite Context},
  author={Sanyi Zhang, Guo-jun Qi, Xiaochun Cao, Zhanjie Song, Jie Zhou},
  journal={TCSVT, under review},
  year={2020}
}
