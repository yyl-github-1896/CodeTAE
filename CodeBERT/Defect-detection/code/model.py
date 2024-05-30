import torch
import torch.nn as nn
import torch
from torch.autograd import Variable
import copy
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss, MSELoss
from torch.utils.data import SequentialSampler, DataLoader
import numpy as np

class RobertaClassificationHead(nn.Module):
    """Head for sentence-level classification tasks."""

    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        classifier_dropout = (
            config.classifier_dropout if config.classifier_dropout is not None else config.hidden_dropout_prob
        )
        self.dropout = nn.Dropout(classifier_dropout)
        self.out_proj = nn.Linear(config.hidden_size, config.num_labels)

    def forward(self, features, **kwargs):
        x = features[:, 0, :]  # take <s> token (equiv. to [CLS])
        x = self.dropout(x)
        x = self.dense(x)
        x = torch.tanh(x)
        x = self.dropout(x)
        x = self.out_proj(x)
        return x
    
class Model(nn.Module):   
    def __init__(self, encoder,config,tokenizer,args):
        super(Model, self).__init__()
        self.encoder = encoder
        self.config=config
        self.tokenizer=tokenizer
        self.args=args
        self.query = 0
    
        
    def forward(self, input_ids=None,labels=None):
        outputs=self.encoder(input_ids,attention_mask=input_ids.ne(1))[0]
        # print('input_ids.shape: {}, attention_mask.shape: {}, outputs.shape: {}'.format(input_ids.shape, input_ids.ne(1).shape, outputs.shape)) # test
        logits=outputs
        prob=F.sigmoid(logits)
        if labels is not None:
            labels=labels.float()
            loss=torch.log(prob[:,0]+1e-10)*labels+torch.log((1-prob)[:,0]+1e-10)*(1-labels)
            loss=-loss.mean()
            return loss,prob
        else:
            return prob

    def get_results(self, dataset, batch_size=16):
        '''Given a dataset, return probabilities and labels.'''

        eval_sampler = SequentialSampler(dataset)
        eval_dataloader = DataLoader(dataset, sampler=eval_sampler, batch_size=batch_size,num_workers=4,pin_memory=False)

        self.eval()
        logits=[] 
        labels=[]
        for batch in eval_dataloader:
            inputs = batch[0].to("cuda")       
            label=batch[1].to("cuda") 
            with torch.no_grad():
                lm_loss,logit = self.forward(inputs,label)
                logits.append(logit.cpu().numpy())
                labels.append(label.cpu().numpy())
                
        logits=np.concatenate(logits,0)
        labels=np.concatenate(labels,0)

        probs = [[1 - prob[0], prob[0]] for prob in logits]
        pred_labels = [1 if label else 0 for label in logits[:,0]>0.5]

        return probs, pred_labels


class Model_sub(nn.Module):
    def __init__(self, encoder):
        super(Model_sub, self).__init__()
        self.encoder = encoder

    def forward(self, input_ids=None):
        outputs = self.encoder.roberta(input_ids= input_ids,attention_mask=input_ids.ne(1))[0]
        return outputs

 
class Model_for_sim(nn.Module):   
    def __init__(self, encoder,config,tokenizer,args):
        super(Model_for_sim, self).__init__()
        self.encoder = encoder
        self.config=config
        self.tokenizer=tokenizer
        self.args=args
        self.query = 0
    
        
    def forward(self, input_ids=None,labels=None):
        logits=self.encoder(input_ids,attention_mask=input_ids.ne(1))[0]
        outputs=self.encoder.roberta(input_ids,attention_mask=input_ids.ne(1))[0]
        # print('input_ids.shape: {}, attention_mask.shape: {}, outputs.shape: {}'.format(input_ids.shape, input_ids.ne(1).shape, outputs.shape)) # test
        # print('outputs.shape: ',outputs.shape) #torch.Size([1, 510, 768])
        prob=F.sigmoid(logits)
        if labels is not None:
            labels=labels.float()
            loss=torch.log(prob[:,0]+1e-10)*labels+torch.log((1-prob)[:,0]+1e-10)*(1-labels)
            loss=-loss.mean()
            return loss,prob, outputs
        else:
            return prob, outputs