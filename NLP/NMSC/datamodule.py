from torch import tensor
import torch.cuda as cuda
from torch.utils.data import Dataset, DataLoader

from pytorch_lightning import LightningDataModule

from transformers import AutoTokenizer


# BERT 토크나이저 등을 설정해주기 위해 Dataset 모듈을 선언합니다.
class BERTDataset(Dataset):
    def __init__(self,
                 data_dir='./dataset',
                 weight='kykim/bert-kor-base',
                 is_train=True,
                 max_len=None):
        super(BERTDataset, self).__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(weight)

        if is_train:
            mode = 'train'
        else:
            mode = 'test'
        with open(f'{data_dir}/ratings_{mode}.txt', 'r') as d:
            self.data = d.readlines()[1:]
            d.close()

        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item, label = self.data[idx].split('\t')[1:]
        encoded_sent = self.tokenizer.encode_plus(text=item,
                                                  add_special_tokens=True,
                                                  max_length=self.max_len,
                                                  truncation=True,
                                                  pad_to_max_length=True,
                                                  return_attention_mask=True,
                                                  return_token_type_ids=True
                                                  )

        input_ids = tensor(encoded_sent.get('input_ids'))
        attention_masks = tensor(encoded_sent.get('attention_mask'))
        token_type_ids = tensor(encoded_sent.get('token_type_ids'))

        return input_ids, attention_masks, token_type_ids, tensor(int(label)).long()
    

# Lightning Data Module을 선언합니다.
class BERTDataModule(LightningDataModule):
    def __init__(self,
                 weight='kykim/bert-kor-base',
                 batch_size=64,
                 max_len=128):
        super(BERTDataModule, self).__init__()
        self.trainset = BERTDataset(weight=weight,
                                    max_len=max_len)
        self.valset = BERTDataset(weight=weight,
                                  is_train=False,
                                  max_len=max_len)
        self.batch_size = batch_size
        self.num_workers = cuda.device_count() * 4

    def train_dataloader(self):
        return DataLoader(dataset=self.trainset,
                          batch_size=self.batch_size,
                          num_workers=self.num_workers,
                          shuffle=True,
                          pin_memory=True,
                          drop_last=True)

    def val_dataloader(self):
        return DataLoader(dataset=self.valset,
                          batch_size=self.batch_size,
                          num_workers=self.num_workers,
                          shuffle=False,
                          pin_memory=True,
                          drop_last=True)
