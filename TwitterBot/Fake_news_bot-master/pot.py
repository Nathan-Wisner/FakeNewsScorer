import tweepy
import json
import re
import random

# Authenticate to Twitter
auth = tweepy.OAuthHandler("xqslgSygms4vFIJEkFSziOGqf", "asDdYRmB5hPrwF3sQx9Bwkh8ZGHqZ61qHftOPHSLWgOSF387uL")
auth.set_access_token("709929871892328448-gXGg7xlTKqLygDulQcRU4STkpEIz1gQ", "EokEp7r0Yxh3ZVV9W5m8O4FxlADucJlRphQcEn9dVUE6r")

# Create API object
api = tweepy.API(auth)

# Create a tweet
#api.update_status("Hello hackathon!")

mentions = api.mentions_timeline()

mentionList = mentions[0]
json_str = json.dumps(mentionList._json)

url = re.search("(?P<url>https?://[^\s]+)", json_str).group("url")
url = url[:len(url) - 2]
print(url)

print(random.randint(1, 250))


