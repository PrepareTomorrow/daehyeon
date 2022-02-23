import torch.nn as nn
import torch.optim as optim

from pytorch_lightning import LightningModule

from model import CNNClassifier

from torchmetrics import Accuracy


class Classifier(LightningModule):
    def __init__(self,
                 model=None,
                 n_words=None,
                 lr=1e-4):
        super(Classifier, self).__init__()

        self.model = CNNClassifier(n_words=n_words)

        self.lr = lr
        self.loss_fn = nn.CrossEntropyLoss()
        self.metrics = Accuracy()

    def configure_optimizers(self):
        return optim.AdamW(params=self.model.parameters(),
                           lr=self.lr)

    def forward(self, x):
        return self.model(x)
    
    def step(self, batch, is_train=True):
        x, y = batch.text, batch.label
        y_hat = self(x)
        
        if not is_train:
            self.metrics(preds=y_hat, target=y)
        
        return self.loss_fn(y_hat, y)

    def training_step(self, batch, *args, **kwargs):
        loss = self.step(batch)
        self.log('train_loss_step', loss, on_step=True, on_epoch=False, prog_bar=False)
        self.log('train_loss_epoch', loss, on_step=False, on_epoch=True, prog_bar=False)
        return {'loss': loss}

    def validation_step(self, batch, *args, **kwargs):
        loss = self.step(batch)
        self.log('val_loss', loss, on_step=False, on_epoch=True, prog_bar=False)
        self.log('Accuracy', self.metrics, on_step=False, on_epoch=True, prog_bar=False)
        return {'loss': loss}