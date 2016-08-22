import theano
import theano.tensor as T
import numpy as np

from layers import *

def numpy_floatX(data):
    return np.asarray(data, dtype=theano.config.floatX)

class LSTM_LR_model(object):
    def __init__(self, x, y, mask, emb, word_size=100, hidden_size=400, out_size=2, prefix='model_'):

        self.embedd_layer = Embedding_layer(
            x=x,
            emb=emb,
            word_size=word_size,
            prefix='embedd_layer_'
        )

        self.lstm_layer = LSTM_layer(
            x=self.embedd_layer.output,
            in_size=word_size,
            hidden_size=hidden_size,
            prefix='lstm0_',
            mask=T.transpose(mask)
        )

        self.lr_layer = LogisticRegression(
            x=self.lstm_layer.output,
            y=y,
            in_size=hidden_size,
            out_size=out_size
        )

        self.output = self.lr_layer.y_d

        self.error = self.lr_layer.error

        self.loss = self.lr_layer.loss

        self.params = dict(self.embedd_layer.params.items()+
                           self.lstm_layer.params.items()+
                           self.lr_layer.params.items()
                           )