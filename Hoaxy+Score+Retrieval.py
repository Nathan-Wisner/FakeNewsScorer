
# coding: utf-8

# In[228]:

import http.client
import json
from urllib.parse import urlparse


conn = http.client.HTTPSConnection("api-hoaxy.p.rapidapi.com")

verifyHeaders = {
    'x-rapidapi-host': "adverifai-api.p.rapidapi.com",
    'x-rapidapi-key': "8bd7508073mshe5c51e555173ee1p1a803ajsnebd7566cb65b"
    }

hoaxiHeaders = {
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

    conn.request("GET", "/articles?sort_by=relevant&use_lucene_syntax=false&query=" + title, headers=hoaxiHeaders)

    res = conn.getresponse()
    data = res.read()
    JSON = json.loads(data.decode("utf-8"))
    getMean(JSON)
    printScores(JSON)

#Finds fact checking for the article or similar articles
def createCheckUpdate(headline):
    checkUrl = "https://adverifai-api.p.rapidapi.com/fact_check"
    checkQuerystring = {"headline": headline}
    checkResponse = requests.request("GET", checkUrl, headers=verifyHeaders, params=checkQuerystring)
    checkData = checkResponse.text
    checkJSON = json.loads(checkData)
    printCheckInformation(checkJSON)

def printCheckInformation(checkJSON):
    for item in (checkJSON["fakeRef"]):
        print(item["title"] + " found on " + item["domain"])
        print(getVerifyScore(item["score"]) + "% fake probability")
        print()
    
#Finds the score given by adverifi for the given claim
def createScoreUpdate(headline):
    scoreUrl = "https://adverifai-api.p.rapidapi.com/fake_ref"
    scoreQuerystring = {"headline":headline}
    scoreResponse = requests.request("GET", scoreUrl, headers=verifyHeaders, params=scoreQuerystring)
    scoreData = scoreResponse.text
    scoreJSON = json.loads(scoreData)
    printCheckInformation(scoreJSON)

#Finds the descriptions for the domain to check if it is a source of any suspision
def createDescriptUpdate(URL):
    descUrl = "https://adverifai-api.p.rapidapi.com/source_check"
    descQuerystring = {"url":URL}
    descResponse = requests.request("GET", descUrl, headers=verifyHeaders, params=descQuerystring)
    descData = descResponse.text
    descJSON = json.loads(descData)
    printDescription(descJSON)
    
def printDescription(descJSON):
    descList = list(descJSON["fakeDescription"].split(','))
    
    for item in descList:
        item = item.replace(" ", "")
        print(item)
    
def getDomain(URL):
    parsed_uri = urlparse(URL)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return result

def getVerifyScore(score):
    score = int(score)
    score = score / 10
    result = str(round(score, 2))
    return result
    
def main():
    URL = "https://www.infowars.com/caught-meryl-streep-applauds-pizzagate-pedophile/"
    headline = "CAUGHT! MERYL STREEP APPLAUDS PIZZAGATE PEDOPHILE"
    
    print("Related fact checked articles")
    createCheckUpdate(headline)
    print()
    print("This headline was found at these websites: ")
    createScoreUpdate(headline)
    print()
    print(getDomain(URL) + " is known for the following: ")
    createDescriptUpdate(URL)
    
main()


# In[96]:

get_ipython().system('pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html')
    
import torch

