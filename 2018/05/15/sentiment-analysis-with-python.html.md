---
author: Muhammad Najmi Ahmad Zabidi 
title: "Sentiment Analysis with Python"
tags: python, data analysis, twitter 
gh_issue_number: 1416 
---

I had a chance spending my weekend enhancing my knowledge by joining a local community meetup in Malaysia which is sponsored by Malaysian Global Innovation & Creativity Centre (MaGIC). The trainer was Mr Lee Boon Kong.

### Anaconda and Jupyter Notebook

We started by preparing our Jupyter Notebook setup which is running on Anaconda Python distribution. The installer is 500MB in size but pretty handy when we started using it. Anaconda comes with a graphical based installed which is called "Navigator" if the user wants to install some packages for work. However it is not always working when I tried it on different OS platform - so I have to use its command line based tool called as "conda". Conda works like Linux-based package management tool (for e.g: apt, dnf, yum, pacman) - so if I decided to install a package I would just run `conda install <package name>`.

Jupyter uses a web browser to allow us to write the code directly in its cell. It is quite helpful for us to debug the code or if we just want to execute it segment by segment independently.  

### Creating Twitter's API key
First we need to head to [this url](https://apps.twitter.com/).

The following items are needed:

* Consumer Key (API Key).
* Consumer Secret (API Secret).
* Access Token.
* Access Token Secret.

### Using Tweepy, NLTK and TextBlob

```python
from textblob import TextBlob
import tweepy
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
consumer_token='<put your token here>'
consumer_secret='<put your secret here>'
access_token='<put your access token here>'
access_secret='<put your access secret here>'
auth=tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api=tweepy.API(auth)
public_tweets=api.search("Avengers Infinity War", lang='en')
print("number of tweets extracted:" + str(len(public_tweets)))
for tweet in public_tweets:
print(tweet.text)
analysis=TextBlob(tweet.text)
print(analysis.sentiment)
print("\n")
```

### Analyzing Tweepy's Sentiment Score Results
The sentiment score that we got is summarized as follows:

* 0 - Neutral
* Negative - Negative sentiment
* Positive - Positive sentiment

By default, the code above uses the English-based library. As a Malaysian, I could not analyze the Malay language based tweet yet. Efforts by the local community are being done to create the Malay-based language corpus for NLTK.  

### Summary
In overall I am quite satisfied with I learned during the session. It is good to have one day spent on a technical workshop like this in which we could be super focus on the content without any external distraction. Kudos to Mr Lee for his effort to teach us on Data Analysis with Python. Till we meet again, hopefully!

---

