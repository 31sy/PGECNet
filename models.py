import torch.nn as nn
from torch.nn import functional as F
import math
import torch.utils.model_zoo as model_zoo
import torch
import numpy as np
from torch.autograd import Variable
affine_par = True
import functools
import sys, os


#current_dir = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, os.path.join(current_dir, './inplace_abn'))
#from bn import InPlaceABNSync
from modules import InPlaceABN, InPlaceABNSync
BatchNorm2d = functools.partial(InPlaceABNSync, activation='none')


def outS(i):
    i = int(i)
    i = (i+1)/2
    i = int(np.ceil((i+1)/2.0))
    i = (i+1)/2
    return i



def conv3x3(in_planes, out_planes, stride=1):
    "3x3 convolution with padding"
    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride,
                     padding=1, bias=False)





class Bottleneck(nn.Module):

    expansion = 4

    def __init__(self, inplanes, planes, stride=1, dilation=1, downsample=None, fist_dilation=1, multi_grid=1):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
        self.bn1 = BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride,
                               padding=dilation*multi_grid, dilation=dilation*multi_grid, bias=False)
        self.bn2 = BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
        self.bn3 = BatchNorm2d(planes * 4)
        self.relu = nn.ReLU(inplace=False)
        self.relu_inplace = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.dilation = dilation
        self.stride = stride

    
    def _sum_each(self, x, y):
        assert(len(x)==len(y))
        z = []

        for i in range(len(x)):
            z.append(x[i]+y[i])
        return z

    def forward(self, x):

        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out = out + residual      
        out = self.relu_inplace(out)
        return out



class PSPModule(nn.Module):

    """
    Reference: 
        Zhao, Hengshuang, et al. *"Pyramid scene parsing network."*
    """

    def __init__(self, features, out_features=512, sizes=(1, 2, 3, 6)):
        super(PSPModule, self).__init__()

        self.stages = []
        self.stages = nn.ModuleList([self._make_stage(features, out_features, size) for size in sizes])
        self.bottleneck = nn.Sequential(
            nn.Conv2d(features+len(sizes)*out_features, out_features, kernel_size=3, padding=1, dilation=1, bias=False),
            InPlaceABNSync(out_features)
            )

    def _make_stage(self, features, out_features, size):
        prior = nn.AdaptiveAvgPool2d(output_size=(size, size))
        conv = nn.Conv2d(features, out_features, kernel_size=1, bias=False)
        bn = InPlaceABNSync(out_features)
        return nn.Sequential(prior, conv, bn)

    def forward(self, feats):

        h, w = feats.size(2), feats.size(3)
        priors = [F.upsample(input=stage(feats), size=(h, w), mode='bilinear',align_corners=True) for stage in self.stages] + [feats]
        bottle = self.bottleneck(torch.cat(priors, 1))
        return bottle




class GE_theoLayer(nn.Module):
    def __init__(self, channel, kernel_wh):
        super(GE_theoLayer, self).__init__()
        self.gather = nn.Sequential(
            nn.Conv2d(channel, channel, kernel_size=kernel_wh, stride=1, groups=channel, bias=False),
            BatchNorm2d(channel),
            nn.Sigmoid()
        )
    def forward(self, x):
        context_gather = self.gather(x) * x       

        return context_gather



class GE_4_theoLayer(nn.Module):
    def __init__(self, channel):
        super(GE_4_theoLayer, self).__init__()        
        self.gather = nn.Sequential(
            nn.Conv2d(channel, channel, kernel_size=3, stride=2, groups=channel,padding=2, bias=False),
            InPlaceABNSync(channel),
            nn.Conv2d(channel, channel, kernel_size=3, stride=2, groups=channel,padding=1, bias=False),
            BatchNorm2d(channel)
        )
        self.gather_sigmoid = nn.Sigmoid()


    def forward(self, x):
        h, w = x.size(2), x.size(3)
        context_gather = F.upsample(input=self.gather(x), size=(h, w), mode='bilinear',align_corners=True)
        context_gather_sigmoid = self.gather_sigmoid(context_gather) * x 
        return context_gather_sigmoid


class GE_8_theoLayer(nn.Module):
    def __init__(self, channel):
        super(GE_8_theoLayer, self).__init__()        
        self.gather = nn.Sequential(
            nn.Conv2d(channel, channel, kernel_size=3, stride=2, groups=channel,padding=2, bias=False),
            InPlaceABNSync(channel),
            nn.Conv2d(channel, channel, kernel_size=3, stride=2, groups=channel,padding=1, bias=False),
            InPlaceABNSync(channel),
            nn.Conv2d(channel, channel, kernel_size=3, stride=2, groups=channel,padding=1, bias=False),
            BatchNorm2d(channel)
        )
        self.gather_sigmoid = nn.Sigmoid()


    def forward(self, x):
        h, w = x.size(2), x.size(3)
        context_gather = F.upsample(input=self.gather(x), size=(h, w), mode='bilinear',align_corners=True)
        context_gather_sigmoid = self.gather_sigmoid(context_gather) * x 
        return context_gather_sigmoid

class GE_16_theoLayer(nn.Module):
    def __init__(self, channel):
        super(GE_16_theoLayer, self).__init__()        
        self.gather = nn.Sequential(
            nn.Conv2d(channel, channel, kernel_size=3, stride=2, groups=channel,padding=2, bias=False),
            InPlaceABNSync(channel),
            nn.Conv2d(channel, channel, kernel_size=3, stride=2, groups=channel,padding=1, bias=False),
            InPlaceABNSync(channel),
            nn.Conv2d(channel, channel, kernel_size=3, stride=2, groups=channel,padding=1, bias=False),
            InPlaceABNSync(channel),
            nn.Conv2d(channel, channel, kernel_size=3, stride=2, groups=channel,padding=1, bias=False),
            BatchNorm2d(channel)
        )
        self.gather_sigmoid = nn.Sigmoid()


    def forward(self, x):
        h, w = x.size(2), x.size(3)
        context_gather = F.upsample(input=self.gather(x), size=(h, w), mode='bilinear',align_corners=True)
        context_gather_sigmoid = self.gather_sigmoid(context_gather) * x
        return context_gather_sigmoid


class PGEC_Module(nn.Module):

    def __init__(self, features, out_features=512):

        super(PGEC_Module, self).__init__()
        self.conv1 = nn.Sequential(nn.Conv2d(features, out_features, kernel_size=3, padding=1, dilation=1, bias=True),
                                   BatchNorm2d(out_features)
                                   )

        self.conv2 = nn.Sequential(GE_theoLayer(features,30),
                                   nn.Conv2d(features, out_features, kernel_size=1, padding=0, dilation=1, bias=False),
                                   BatchNorm2d(out_features))

        self.conv3 = nn.Sequential(GE_4_theoLayer(features),
                                   nn.Conv2d(features, out_features, kernel_size=1, padding=0, dilation=1, bias=False),
                                   BatchNorm2d(out_features))
       
        self.conv4 = nn.Sequential(GE_8_theoLayer(features),
                                   nn.Conv2d(features, out_features, kernel_size=1, padding=0, dilation=1, bias=False),
                                   BatchNorm2d(out_features))
        

        self.conv5 = nn.Sequential(GE_16_theoLayer(features),
                                   nn.Conv2d(features, out_features, kernel_size=1, padding=0, dilation=1, bias=False),
                                   BatchNorm2d(out_features))
        
        
        self.conv_bn_dropout = nn.Sequential(
            nn.Conv2d(out_features * 5, out_features, kernel_size=1, padding=0, dilation=1, bias=False),
            InPlaceABNSync(out_features),
            nn.Dropout2d(0.1)
            )
        

    def forward(self, x):
        if isinstance(x, Variable):
            _, _, h, w = x.size()
        elif isinstance(x, tuple) or isinstance(x, list):
            _, _, h, w = x[0].size()
        else:
            raise RuntimeError('unknown input type')

        feat1 = self.conv1(x) 
        feat2 = self.conv2(x)
        feat3 = self.conv3(x)
        feat4 = self.conv4(x)
        feat5 = self.conv5(x)
        
        if isinstance(x, Variable):
            out = torch.cat((feat1, feat2, feat3, feat4, feat5), 1)
        elif isinstance(x, tuple) or isinstance(x, list):
            out = self._cat_each(feat1, feat2, feat3, feat4, feat5)
        else:
            raise RuntimeError('unknown input type')

        output = self.conv_bn_dropout(out)
        return output  



class Edge_Module(nn.Module):
    def __init__(self, mid_fea, out_fea):

        super(Edge_Module, self).__init__()
        self.conv1 =  nn.Sequential(
            nn.Conv2d(256, mid_fea, kernel_size=1, padding=0, dilation=1, bias=False),
            BatchNorm2d(mid_fea),
            nn.ReLU(inplace=False)
            ) 

        self.conv2 =  nn.Sequential(
            nn.Conv2d(512, mid_fea, kernel_size=1, padding=0, dilation=1, bias=False),
            BatchNorm2d(mid_fea),
            nn.ReLU(inplace=False)
            )  

        self.conv3 =  nn.Sequential(
            nn.Conv2d(1024, mid_fea, kernel_size=1, padding=0, dilation=1, bias=False),
            BatchNorm2d(mid_fea),
            nn.ReLU(inplace=False)
            )

        self.conv4 = nn.Conv2d(mid_fea,2, kernel_size=3, padding=1, dilation=1, bias=True)
        self.conv5 = nn.Conv2d(out_fea*3,out_fea, kernel_size=1, padding=0, dilation=1, bias=True)

        
    def forward(self, x1, x2, x3):
        _, _, h, w = x1.size()
        edge1_fea = self.conv1(x1)
        edge1 = self.conv4(edge1_fea)
        edge2_fea = self.conv2(x2)
        edge2 = self.conv4(edge2_fea)
        edge3_fea = self.conv3(x3)
        edge3 = self.conv4(edge3_fea)        
        edge2_fea = F.upsample(edge2_fea, size=(h, w), mode='bilinear',align_corners=True)
        edge3_fea = F.upsample(edge3_fea, size=(h, w), mode='bilinear',align_corners=True) 

        edge2 = F.upsample(edge2, size=(h, w), mode='bilinear',align_corners=True)
        edge3 = F.upsample(edge3, size=(h, w), mode='bilinear',align_corners=True) 

        edge = torch.cat([edge1, edge2, edge3], dim=1)
        edge_fea = torch.cat([edge1_fea, edge2_fea, edge3_fea], dim=1)
        edge = self.conv5(edge)

        return edge, edge_fea

class Decoder_Module(nn.Module):

    def __init__(self, num_classes):
        super(Decoder_Module, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(512, 256, kernel_size=1, padding=0, dilation=1, bias=False),
            BatchNorm2d(256),
            nn.ReLU(inplace=False)
            )
        self.conv2 = nn.Sequential(
            nn.Conv2d(256, 48, kernel_size=1, stride=1, padding=0, dilation=1, bias=False),
            BatchNorm2d(48),
            nn.ReLU(inplace=False)
            )
        self.conv3 = nn.Sequential(
            nn.Conv2d(304, 256, kernel_size=1, padding=0, dilation=1, bias=False),
            BatchNorm2d(256),
            nn.ReLU(inplace=False),
            nn.Conv2d(256, 256, kernel_size=1, padding=0, dilation=1, bias=False),
            BatchNorm2d(256),
            nn.ReLU(inplace=False)
            )

        self.conv4 = nn.Conv2d(256, num_classes, kernel_size=1, padding=0, dilation=1, bias=True)

    def forward(self, xt, xl):
        _, _, h, w = xl.size()

        xt = F.upsample(self.conv1(xt), size=(h, w), mode='bilinear',align_corners=True)
        xl = self.conv2(xl)
        x = torch.cat([xt, xl], dim=1)
        x = self.conv3(x)
        seg = self.conv4(x)
        return seg, x  

 
class ResNet_Edge_GE_multi(nn.Module):
    def __init__(self, block, layers, num_classes):
        self.inplanes = 64
        super(ResNet_Edge_GE_multi, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3,
                               bias=False)
        self.bn1 = BatchNorm2d(64, affine = affine_par)

        self.relu = nn.ReLU(inplace=False)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1, ceil_mode=True) # change
        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2, dilation=1)
        self.layer4 = self._make_layer(block, 512, layers[3], stride=1, dilation=2, multi_grid=(1,1,1))
        self.layer5 = PGEC_Module(2048, 512)
        self.edgelayer = Edge_Module(256, 2) 
        self.layer6 = Decoder_Module(num_classes)
        self.layer7 = nn.Sequential(
            nn.Conv2d(1024, 256, kernel_size=1, padding=0, dilation=1, bias=False),
            BatchNorm2d(256),
            nn.ReLU(inplace=False),
            nn.Conv2d(256, num_classes, kernel_size=1, padding=0, dilation=1, bias=True)
            ) 
        self.dsn = nn.Sequential(
            nn.Conv2d(1024, 256, kernel_size=3, stride=1, padding=1),
            BatchNorm2d(256),
            nn.ReLU(inplace=False),
            nn.Conv2d(256, num_classes, kernel_size=1, stride=1, padding=0, bias=True)
            )         

    def _make_layer(self, block, planes, blocks, stride=1, dilation=1, multi_grid=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion,
                          kernel_size=1, stride=stride, bias=False),
                BatchNorm2d(planes * block.expansion,affine = affine_par))

        layers = []
        generate_multi_grid = lambda index, grids: grids[index%len(grids)] if isinstance(grids, tuple) else 1
        layers.append(block(self.inplanes, planes, stride,dilation=dilation, downsample=downsample, multi_grid=generate_multi_grid(0, multi_grid)))
        self.inplanes = planes * block.expansion
        print(multi_grid)
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes, dilation=dilation, multi_grid=generate_multi_grid(i, multi_grid)))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x1 = self.maxpool(x)
        x2 = self.layer1(x1)
        x3 = self.layer2(x2)
        x4 = self.layer3(x3)
        x_dsn = self.dsn(x4)
        x5 = self.layer4(x4)
        edge, edge_fea = self.edgelayer(x2,x3,x4)
         
        x5 = self.layer5(x5)

        out1,x = self.layer6(x5, x2)
        
        x = torch.cat([x, edge_fea], dim=1) 
        
        out2 = self.layer7(x)         
        return out1, out2, x_dsn, edge    
             
def Res_CE2P_GE_multi(num_classes=20):

    model = ResNet_Edge_GE_multi(Bottleneck,[3, 4, 23, 3], num_classes)

    return model

