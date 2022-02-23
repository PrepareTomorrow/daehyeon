from torch.utils.data import Dataset
from pytorch_lightning import LightningDataModule
from konlpy.tag import Mecab

from torchtext.legacy import data
from torchtext.legacy.data import TabularDataset, Iterator


class NMSCtorchtextDataModule(LightningDataModule):
    def __init__(self,
                 batch_size=256,
                 max_length=64):
        super().__init__()
        self.tokenizer = Mecab()
        self.batch_size = batch_size
        self.ID = data.Field(sequential=False,
                             use_vocab=False,
                             is_target=False)
        self.TEXT = data.Field(sequential=True,
                               use_vocab=True,
                               tokenize=self.tokenizer.morphs,
                               lower=False,
                               batch_first=True,
                               fix_length=max_length)
        self.LABEL = data.Field(sequential=False,
                                use_vocab=False,
                                is_target=True)
        self.train_data, self.val_data = TabularDataset.splits(path='./dataset',
                                                               train='ratings_train.txt',
                                                               test='ratings_test.txt',
                                                               format='tsv',
                                                               fields=[('id', self.ID),
                                                                       ('text', self.TEXT),
                                                                       ('label', self.LABEL)],
                                                               skip_header=True)
        self.TEXT.build_vocab(self.train_data, min_freq=5)

    def __len__(self):
        return len(self.TEXT.vocab)

    def train_dataloader(self):
        return Iterator(dataset=self.train_data,
                        batch_size=self.batch_size,
                        shuffle=True)

    def val_dataloader(self):
        return Iterator(dataset=self.val_data,
                        batch_size=self.batch_size,
                        shuffle=False)
