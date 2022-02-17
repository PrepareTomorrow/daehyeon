import torch.nn as nn
from collections import OrderedDict

from transformers import AutoModel


# Weight Init 설정을 위한 헬퍼함수를 선언합니다.
def weight_he_init(layers):
    init_fn = nn.init.kaiming_uniform
    for layer in layers:
        if isinstance(layer, nn.Linear):
            init_fn(layer.weight)


def weight_xavier_init(layers):
    init_fn = nn.init.xavier_uniform
    for layer in layers:
        if isinstance(layer, nn.Linear):
            init_fn(layer.weight)


class BertForClassification(nn.Module):
    def __init__(self,
                 weight='kykim/bert-kor-base',
                 n_classes=2,
                 freeze=True):
        super(BertForClassification, self).__init__()
        
        if weight is None or n_classes is None:
            raise NotImplementedError('Please check the parameters')
        
        self.model = AutoModel.from_pretrained(weight)

        if freeze:
            for param in self.model.parameters():
                param.require_grad = False
        
        self.clf = nn.Sequential(
            OrderedDict({
                'batch-norm': nn.BatchNorm1d(768),
                'relu': nn.ReLU(),
                'fc': nn.Linear(768, n_classes)
            })
        )
        self.activation = nn.LogSoftmax()

    def forward(self, input_ids, attention_mask, token_type_ids):
        x = self.model(input_ids=input_ids,
                       attention_mask=attention_mask,
                       token_type_ids=token_type_ids)
        x = self.clf(x.pooler_output)
        y_hat = self.activation(x)
        return y_hat