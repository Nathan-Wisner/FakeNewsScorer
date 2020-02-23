import tweepy
import json
import re
import random
import time
from io import StringIO
import csv
import sqlite3
from sqlite3 import Error
from Hoaxy import getScore, createDescriptUpdate, getDomain
from newspaper import Article

# Authenticate to Twitter and create API object
auth = tweepy.OAuthHandler("xqslgSygms4vFIJEkFSziOGqf", "asDdYRmB5hPrwF3sQx9Bwkh8ZGHqZ61qHftOPHSLWgOSF387uL")
auth.set_access_token("709929871892328448-gXGg7xlTKqLygDulQcRU4STkpEIz1gQ", "EokEp7r0Yxh3ZVV9W5m8O4FxlADucJlRphQcEn9dVUE6r")
api = tweepy.API(auth)

#Initalize database connection
con = sqlite3.connect('twitter.db')
cursor = con.cursor()

# Makes sql database connection
def connectToSQLDatabase():
    try:
        con = sqlite3.connect("twitter.db")
        print("Database Connection established")
    except Error:
        print("error")

def createTables():
    # Tweet table
    cursor.execute("CREATE TABLE tweets(tweet_id INTEGER PRIMARY KEY);")
    cursor.execute("CREATE TABLE stats(articleTitle VARCHAR(50), articleURL VARCHAR(75), tweetCount INTEGER, "
                   "PRIMARY KEY(articleTitle, articleURL))")
    con.commit()

def dropTables():
    cursor.execute("DROP TABLE tweets")
    cursor.execute("DROP TABLE stats")
    con.commit()

def insertID(tweet_id):
    cursor.execute("INSERT INTO tweets (tweet_id) VALUES (?)", [tweet_id])
    con.commit()

def idExists(tweet_iD):
    cursor.execute("SELECT * FROM tweets")
    for x in cursor:
        if tweet_iD == x[0]:
            return True
    return False

def getHeadlineFromUrl(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.title

def printDescList(newDict):
    list = newDict["fakeDescription"]
    return list

def runBot():
    while True:
        mentions = api.mentions_timeline()
        mention_list = mentions[0]
        tweet_id = mention_list._json["id"]
        expanded = mention_list._json["entities"]["urls"][0]["expanded_url"]
        json_str = json.dumps(mention_list._json)
        url = re.search("(?P<url>https?://[^\s]+)", json_str).group("url")
        url = url[:len(url) - 2]

        # Checks if the tweet_id has been seen already
        if not idExists(tweet_id):
            insertID(tweet_id)

            scoring = getScore(expanded)
            domain = getDomain(expanded)
            description = createDescriptUpdate(expanded)

            if "fakeDescription" in description:
                api.update_status('Article has a ' + str(scoring) + '% chance of being false ' + expanded + " \n \n This may be because " + domain + " is known for " + str(printDescList(description)))
            else:
                api.update_status('Article has a ' + str(scoring) + '% chance of being false ' + expanded)
                print(tweet_id)
            print(expanded)
        else:
            print("ID %d already seen", tweet_id)

        time.sleep(15)

def main():
    runBot()

if __name__ == "__main__":
    main()
