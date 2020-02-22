
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


# In[47]:

import http.client
import json

conn = http.client.HTTPSConnection("api-hoaxy.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "api-hoaxy.p.rapidapi.com",
    'x-rapidapi-key': "8bd7508073mshe5c51e555173ee1p1a803ajsnebd7566cb65b"
    }

conn.request("GET", "/articles?sort_by=relevant&use_lucene_syntax=true&query=Bernie+Sanders+Is+A+Nazi", headers=headers)

res = conn.getresponse()
data = res.read()
JSON = json.loads(data.decode("utf-8"))

for item in JSON["articles"]:
    print(item["title"])
    print(item["site_type"])
    print(item["score"])


# In[ ]:



