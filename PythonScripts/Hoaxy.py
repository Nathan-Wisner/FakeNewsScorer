# coding: utf-8

# In[ ]:

import http.client
import json
import requests
import pandas as pd
import torch
import torchtext
from urllib.parse import urlparse
from URL import getHeadline

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
    if (score < median - (median) * .03):
        return 40 + score / median
    if (score > median - (median * .01) and score < median):
        return 45 + score / median
    if (score > median + (median) and score < median + (median * .01)):
        return 75 + score / median
    if (score > median + (median * .02) and score < median + (median * .4)):
        return 80 + score / median
    elif (score < median + (median * .4)):
        return 85 + score / median
    else:
        return 90 + score / median


def categorizeMedian(median):
    if (median < 50):
        return median
    if (median > 50 and median < 85):
        return 45
    if (median > 100 and median < 150):
        return 65
    if (median > 150 and median < 200):
        return 85
    if (median > 200):
        return 92


def getMean(JSON):
    counter = 0
    totalScore = 0
    for item in JSON["articles"]:
        if (item["site_type"] == "claim"):
            counter = counter + 1
            totalScore = totalScore + int(item["score"])
    return totalScore / counter


def printScores(JSON):
    mean = getMean(JSON)
    print(mean)
    for item in JSON["articles"]:
        print(item["title"])
        print(categorizeScore(item["score"], mean))
        print()


def getHeadlineScore(title):
    title = title.replace(" ", "+")
    title = title.replace("_", "+")
    title = title.replace("-", "+")
    title = title.replace(u"\u2019", "-")

    conn.request("GET", "/articles?sort_by=relevant&use_lucene_syntax=false&query=" + title, headers=hoaxiHeaders)

    res = conn.getresponse()
    data = res.read()
    JSON = json.loads(data.decode("utf-8"))
    mean = getMean(JSON)
    return categorizeMedian(mean)


# Finds fact checking for the article or similar articles
def createCheckUpdate(headline, URL):
    checkUrl = "https://adverifai-api.p.rapidapi.com/fact_check"
    checkQuerystring = {"headline": headline}
    checkResponse = requests.request("GET", checkUrl, headers=verifyHeaders, params=checkQuerystring)
    checkData = checkResponse.text
    checkJSON = json.loads(checkData)
    printCheckInformation(checkJSON, URL, headline)


def printCheckInformation(checkJSON, URL, headline):
    maxScore = []
    description = createDescriptUpdate(URL)
    print(description)
    for item in (checkJSON["fakeRef"]):
        if "fakeDescription" in description:
            itemScore = float(getRoundedScore(item["score"])) + float(len(description["fakeDescription"]) * 10)
        else:
            itemScore = float(getRoundedScore(item["score"]))
        maxScore.append(itemScore)
    return max(maxScore)


# Finds the score given by adverifi for the given claim
def createScoreUpdate(headline, URL):
    scoreUrl = "https://adverifai-api.p.rapidapi.com/fake_ref"
    scoreQuerystring = {"headline": headline}
    scoreResponse = requests.request("GET", scoreUrl, headers=verifyHeaders, params=scoreQuerystring)
    scoreData = scoreResponse.text
    scoreJSON = json.loads(scoreData)
    return printCheckInformation(scoreJSON, URL, headline)


# Finds the descriptions for the domain to check if it is a source of any suspision
def createDescriptUpdate(URL):
    print(URL)
    descUrl = "https://adverifai-api.p.rapidapi.com/source_check"
    descQuerystring = {"url": URL}
    descResponse = requests.request("GET", descUrl, headers=verifyHeaders, params=descQuerystring)
    descData = descResponse.text
    print(descData)
    descJSON = json.loads(descData)
    print(descJSON)
    return dict(descJSON)


def printDescription(descJSON):
    descList = list(descJSON)
    return descList


def getDomain(URL):
    parsed_uri = urlparse(URL)
    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return result


def getRoundedScore(score):
    score = int(score)
    score = score / 10
    result = str(round(score, 2))
    return result


def getVerifyScore(headline, URL):
    score = createScoreUpdate(headline, URL)
    if (score > 100):
        score = 99.9
    return score


def getScore(URL):
    headline = getHeadline(URL)
    verifyScore = getVerifyScore(headline, URL)
    #hoaxyScore = getHeadlineScore(headline)
    print(verifyScore)
    #print(hoaxyScore)

    return verifyScore