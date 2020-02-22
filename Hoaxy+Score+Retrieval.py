
# coding: utf-8

# In[6]:

import requests

url = "https://api-hoaxy.p.rapidapi.com/tweets"

querystring = {"ids":"%5B29317%2C 68363%5D"}

headers = {
    'x-rapidapi-host': "api-hoaxy.p.rapidapi.com",
    'x-rapidapi-key': "8bd7508073mshe5c51e555173ee1p1a803ajsnebd7566cb65b"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


# In[7]:

import http.client

conn = http.client.HTTPSConnection("api-hoaxy.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "api-hoaxy.p.rapidapi.com",
    'x-rapidapi-key': "8bd7508073mshe5c51e555173ee1p1a803ajsnebd7566cb65b"
    }

conn.request("GET", "/tweets?ids=%255B29317%252C%2068363%255D", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# In[155]:

import http.client
import json

conn = http.client.HTTPSConnection("api-hoaxy.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "api-hoaxy.p.rapidapi.com",
    'x-rapidapi-key': "8bd7508073mshe5c51e555173ee1p1a803ajsnebd7566cb65b"
    }

def categorizeScore(score, median):
    if(score < median - (median) * .03):
        return "Likely True"
    if (score > median - (median * .01) and score < median):
        return "Possibly True"
    if (score > median + (median) and score < median + (median * .01)):
        return "Possibly False"
    if (score > median + (median * .02) and score < median + (median * .4)):
        return "Likely False"
    elif (score < median + (median * .4)):
        return "Very Likely False"
    else:
        return "False"

def getMean(JSON):
    counter = 0
    totalScore = 0
    for item in JSON["articles"]:
        if(item["site_type"] == "claim"):
            counter = counter  +1
            totalScore = totalScore + int(item["score"])
    return totalScore / counter

def printScores(JSON):
    mean = getMean(JSON)
    print(mean)
    for item in JSON["articles"]:
        print(item["title"])
        print(categorizeScore(item["score"], mean))
        print()
        #print(item["score"])

def getHeadlineScore(title):

    title = title.replace(" ", "+")
    title = title.replace("_", "+")
    title = title.replace("-", "+")

    conn.request("GET", "/articles?sort_by=relevant&use_lucene_syntax=false&query=" + title, headers=headers)

    res = conn.getresponse()
    data = res.read()
    JSON = json.loads(data.decode("utf-8"))
    getMean(JSON)
    printScores(JSON)
getHeadlineScore("Moon landing")


# In[94]:

import requests

url = "https://api-hoaxy.p.rapidapi.com/latest-articles"

querystring = {"domains":'[infowars.com]',"past_hours":"100"}

headers = {
    'x-rapidapi-host': "api-hoaxy.p.rapidapi.com",
    'x-rapidapi-key': "8bd7508073mshe5c51e555173ee1p1a803ajsnebd7566cb65b"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


# In[96]:

get_ipython().system('pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html')
    
import torch


# In[98]:

import torch, torchtext


# In[ ]:



