import torch
import torch.nn as nn
import torch.nn.functional as F


class CNNClassifier(nn.Module):
    def __init__(self,
                 n_words,
                 wordvec_dim=512,
                 drop_out=.5,
                 window_size=[5, 6, 7],
                 n_filters=[64, 64, 64]):
        super(CNNClassifier, self).__init__()

        self.wordvec_dim = wordvec_dim
        self.window_size = window_size
        self.n_filters = n_filters
        self.min_length = max(self.window_size)

        assert len(self.window_size) == len(self.n_filters), f"window와 filter의 갯수를 맞춰주세요,,\
        {len(self.n_filters)} != {len(self.window_size)}"

        self.emb = nn.Embedding(n_words, wordvec_dim)

        for window, filter_ in zip(window_size, n_filters):
            cnn = nn.Conv2d(in_channels=1,
                            out_channels=filter_,
                            kernel_size=(window, wordvec_dim))
            setattr(self, f'cnn-w{window}-f{filter_}', cnn)

        self.drop_out = nn.Dropout(drop_out)
        self.tanh = nn.Tanh()
        self.fc = nn.Sequential(
            nn.BatchNorm1d(sum(n_filters)),
            nn.ReLU(),
            nn.Linear(sum(n_filters), 2)
        )

    def forward(self, x):
        word_vec = self.emb(x)
        word_vec_pad = word_vec.unsqueeze(1)

        c = []
        for window, filter_ in zip(self.window_size, self.n_filters):
            cnn = getattr(self, f'cnn-w{window}-f{filter_}')
            cnn_out = self.tanh(cnn(word_vec_pad))
            drop_out = self.drop_out(cnn_out)
            c_i = F.max_pool1d(input=drop_out.squeeze(-1),
                               kernel_size=drop_out.size(-2)).squeeze(-1)
            c.append(c_i)

        cnn_result = torch.cat(c, dim=-1)
        logit = self.fc(cnn_result)
        return logit