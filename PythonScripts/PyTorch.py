import pandas as pd
import torch
import torchtext
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
import time
from torch.utils.data.dataset import random_split

import torch
import torchtext
from torchtext.datasets import text_classification
NGRAMS = 2
import os
if not os.path.isdir('./.data'):
    os.mkdir('./.data')
#train_dataset, test_dataset = text_classification.DATASETS['AG_NEWS'](
#   root='./.data', ngrams=NGRAMS, vocab=None)
BATCH_SIZE = 16
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


pRealTrain = []
pFakeTrain = []
gRealTrain = []
gFakeTrain = []
newsFakeTrain = []


def parseFiles():
    newsFake = pd.read_csv("news_sample.csv")
    poliReal = pd.read_csv("politifact_real.csv")
    poliFake = pd.read_csv("politifact_fake.csv")
    gosiFake = pd.read_csv("gossipcop_fake.csv")
    gosiReal = pd.read_csv("gossipcop_real.csv")

    pRealFrame = poliReal[['news_url', 'title', 'tweet_ids']]
    pFakeFrame = poliFake[['news_url', 'title', 'tweet_ids']]
    gFakeFrame = gosiFake[['news_url', 'title', 'tweet_ids']]
    gRealFrame = gosiReal[['news_url', 'title', 'tweet_ids']]
    newsFrame = newsFake[['url', 'title', 'type']]

    pRealList = pRealFrame.values.tolist()
    pFakeList = pFakeFrame.values.tolist()
    gRealList = gRealFrame.values.tolist()
    gFakeList = gFakeFrame.values.tolist()
    newsList = newsFrame.values.tolist()

    createList(pRealList, pRealTrain)
    createList(pFakeList, pFakeTrain)
    createList(gRealList, gRealTrain)
    createList(gFakeList, gFakeTrain)
    createList(newsList, newsFakeTrain)

    printSize(pRealList)
    printSize(pFakeList)
    printSize(gRealList)
    printSize(gFakeList)
    printSize(newsList)

    global pList, gList
    pList = pRealList + pFakeList
    gList = gRealList + gFakeList


def createList(list, trainList):
    for item in list:
        trainList.append([item[0], item[1]])


def printSize(list):
    print(len(list))


parseFiles()
pTrainList, pTestList = torch.utils.data.random_split(pList, [756, 300])
printSize(gList)
train_dataset, test_dataset = torch.utils.data.random_split(gList, [18000, 4140])


import numpy as np
from sklearn.datasets import make_classification
from torch import nn
import torch.nn.functional as F
from skorch import NeuralNetClassifier


X, y = make_classification(1000, 20, n_informative=10, random_state=0)
print(X)
print(y)
X = X.astype(np.float32)
y = y.astype(np.int64)

class MyModule(nn.Module):
    def __init__(self, num_units=10, nonlin=F.relu):
        super(MyModule, self).__init__()

        self.dense0 = nn.Linear(20, num_units)
        self.nonlin = nonlin
        self.dropout = nn.Dropout(0.5)
        self.dense1 = nn.Linear(num_units, 10)
        self.output = nn.Linear(10, 2)

    def forward(self, X, **kwargs):
        X = self.nonlin(self.dense0(X))
        X = self.dropout(X)
        X = F.relu(self.dense1(X))
        X = F.softmax(self.output(X))
        return X


net = NeuralNetClassifier(
    MyModule,
    max_epochs=10,
    lr=0.1,
    # Shuffle training data on each epoch
    iterator_train__shuffle=True,
)

net.fit(X, y)
y_proba = net.predict_proba(X)