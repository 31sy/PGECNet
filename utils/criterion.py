import torch.nn as nn
# import encoding.nn as nn
import math
import torch.utils.model_zoo as model_zoo
import torch
import numpy as np
from torch.nn import functional as F
from torch.autograd import Variable
from .loss import DiscriminativeLoss, HNMDiscriminativeLoss, OhemCrossEntropy2d
 
class CriterionCrossEntropyEdgeParsingAL(nn.Module):
    def __init__(self, ignore_index=255):
        super(CriterionCrossEntropyEdgeParsingAL, self).__init__()
        self.ignore_index = ignore_index
        self.criterion = torch.nn.CrossEntropyLoss(ignore_index=ignore_index) 
          
    def forward(self, preds, target):
        h, w = target[0].size(1), target[0].size(2)
        
        input_labels = target[1].data.cpu().numpy().astype(np.int64)
        pos_num = np.sum(input_labels==1).astype(np.float)
        neg_num = np.sum(input_labels==0).astype(np.float)
        
        weight_pos = neg_num/(pos_num+neg_num)
        weight_neg = pos_num/(pos_num+neg_num)
        weights = (weight_neg, weight_pos)  
        weights = Variable(torch.from_numpy(np.array(weights)).float().cuda())
        
        scale_pred = F.upsample(input=preds[0], size=(h, w), mode='bilinear', align_corners=True)
        loss = self.criterion(scale_pred, target[0])
        
        scale_pred1 = F.upsample(input=preds[1], size=(h, w), mode='bilinear', align_corners=True)
        loss1 = self.criterion(scale_pred1, target[0])

        scale_pred2 = F.upsample(input=preds[2], size=(h, w), mode='bilinear', align_corners=True)
        loss2 = self.criterion(scale_pred2, target[0])
     
        scale_pred3 = F.upsample(input=preds[3], size=(h, w), mode='bilinear', align_corners=True)
        loss3 = F.cross_entropy(scale_pred3, target[1], weights )


        return loss+loss1+0.4*loss2+loss3

