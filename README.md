# FakeNewsScorer

This repository contains a collection of projects for the FakeNews hackathon project. Within the root folder, 
there is a folder containg each project which willcbe discuessed in greater detail below.

## Projects explained


#### PythonScripts folder

Contains project work for the Python Twitter bot including data sets used, PyTorch files, SQLite database instances, and files for 
making API calls to Hoaxy, AdVerify, and our own PyTorch classifier. 

Training data sets: <br/>
[Fake News Net](https://github.com/KaiDMML/FakeNewsNet) <br/>
[Fake News Corpus](https://github.com/several27/FakeNewsCorpus)


#### TwitterBot/Fake_news_bot

Contains work specific to earlier versions of the Twitter bot which uses SQLite3, Python, and uses the Tweepy API for making 
the Twitter API easier to use.

The main premise of this bot is that it will post a status update about the probabliity of any article that is tweeted at the bot. 
This is done by running the bot in a continous polling loop backed by a SQLite database to keep an index of already tweeted articles as
well as statitics.

#### Website/Fake-news-check-master

Contains a ReactJS website which displays the bot's Twitter feed along with text boxes which are intended to check articles directly 
from the site. More importnatly, the website is inteded to display analytics on current fake news. 

The backend is running off NodeJS, Mongoose, and Express but wasn't fully implemented. Additional time was spent deploying the website 
onto AWS 

### Deployment

Python Scripts folder and Twitter Bot: Running locally backed by a SQLite database.
ReactJS website: Deployed suceesfully onto AWS

