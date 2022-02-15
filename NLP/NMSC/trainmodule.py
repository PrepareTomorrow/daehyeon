import torch.nn as nn
import torch.optim as optim

from train import BertForClassification

from pytorch_lightning import LightningModule
from torchmetrics import Accuracy, Recall, Precision


class Classifier(LightningModule):
    def __init__(self,
                 weight='kykim/bert-kor-base',
                 n_classes=2):
        super().__init__()
        self.model = BertForClassification(weight=weight,
                                           n_classes=n_classes,
                                           freeze=True)
        self.loss_fn = nn.NLLLoss()

        self.accuracy = Accuracy()
        self.recall = Recall(num_classes=n_classes)
        self.pre = Precision(num_classes=n_classes)

    def forward(self, input_ids, attention_masks, token_type_ids):
        return self.model(input_ids, attention_masks, token_type_ids)

    def configure_optimizers(self):
        optimizer = optim.AdamW(self.model.clf.parameters(),
                                lr=self.lr)
        return optimizer

    def training_step(self, batch, *args, **kwargs):
        input_ids, attention_masks, token_type_ids, label = batch
        y_hat = self(input_ids, attention_masks, token_type_ids)
        loss = self.loss_fn(y_hat, label)

        self.log('train_loss', loss, on_step=True, on_epoch=False, prog_bar=False)
        self.log('train_loss_epoch', loss, on_step=False, on_epoch=True, prog_bar=False)
        return {'loss': loss}

    def validation_step(self, batch, *args, **kwargs):
        input_ids, attention_masks, token_type_ids, label = batch
        y_hat = self(input_ids, attention_masks, token_type_ids)
        loss = self.loss_fn(y_hat, label)

        self.accuracy(preds=y_hat, target=label)
        self.pre(preds=y_hat, target=label)
        self.recall(preds=y_hat, target=label)

        self.log('val_loss', loss, on_step=False, on_epoch=True, prog_bar=False)
        self.log('Accuracy', self.accuracy, on_step=False, on_epoch=True)
        self.log('Precision', self.pre, on_step=False, on_epoch=True)
        self.log('Recall', self.recall, on_step=False, on_epoch=True)
        return {'loss': loss}