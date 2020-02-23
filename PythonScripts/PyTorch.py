import pandas as pd
import torch
import torchtext
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

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
gTrainList, gTestList = torch.utils.data.random_split(gList, [18000, 4140])


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

net = Net()

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)


def trainModel():
    for epoch in range(2):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(pRealTrain, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
            if i % 2000 == 1999:  # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0

    print('Finished Training')
trainModel()