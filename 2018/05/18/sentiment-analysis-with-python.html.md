---
author: Muhammad Najmi bin Ahmad Zabidi
title: "Sentiment Analysis with Python"
tags: python, natural-language-processing, social-networks
gh_issue_number: 1424
---

<img src="/blog/2018/05/18/sentiment-analysis-with-python/book-chair-chat-711009-crop.jpg" width="770" height="381" alt="people sitting around a table with smartphone and magazine"><br><a href="https://www.pexels.com/photo/group-of-people-reading-book-sitting-on-chair-711009/">Photograph by Helena Lopes, CC0</a>

I recently had the chance to spend my weekend enhancing my knowledge by joining a local community meetup in Malaysia which is sponsored by Malaysian Global Innovation & Creativity Centre (MaGIC). The trainer was Mr Lee Boon Kong.

### Anaconda and Jupyter Notebook

We started by preparing our Jupyter Notebook setup which is running on the Anaconda Python distribution. The installer is 500 MB in size but pretty handy when we started using it.

Anaconda comes with a graphical installer called “Navigator” so the user can install some packages for work. However it did not always work for me on some OSes, so I had to use its command-line based tool “conda”. Conda works like Linux-based package management tools such as apt, dnf, yum, and pacman, so to install a package I would just run `conda install <package name>`.

Jupyter uses a web browser to allow us to write the code directly in its cell. It is quite helpful for us to debug the code or if we just want to execute it segment by segment independently.

### Creating Twitter’s API key

First we need to head to [apps.twitter.com](https://apps.twitter.com/).

The following items are needed:

* Consumer Key (API key)
* Consumer Secret (API secret)
* Access Token
* Access Token Secret

### Using Tweepy, NLTK and TextBlob

```python
from textblob import TextBlob
import tweepy
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
consumer_token = '<put your token here>'
consumer_secret = '<put your secret here>'
access_token = '<put your access token here>'
access_secret = '<put your access secret here>'
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
public_tweets = api.search("Avengers Infinity War", lang='en')
print("number of tweets extracted: " + str(len(public_tweets)))
for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    print("\n")
```

If we want to increase the number of tweets to be displayed and analyzed, just change this line to:

```
public_tweets = api.search("avengers", count=100, result_type='recent', lang='en')
```

### Analyzing Sentiment Score Results

The sentiment score that we got is summarized as follows:

* < 0 - Negative sentiment
* 0 - Neutral
* > 0 - Positive sentiment

By default, the code above uses the English-based library. As a Malaysian, I could not analyze tweets in the Malay language yet. Efforts by the local community are being made to create the Malay-based language corpus for NLTK.

### Looking at the TextBlob Component

The Natural Language Processing (NLP) library’s TextBlob did the sentiment processing task.

I did some reading in [TextBlob’s documentation](https://textblob.readthedocs.io/en/dev/). So for example if I declare:

```
text = '''
I love to read!
'''
```

I get a sentiment polarity value of 0.5 (positive).

While if I put

```
text = '''
I hate to read!
'''
```

I get a sentiment polarity value of -1.0 (negative).

### Summary

Overall I am quite satisfied with what I learned during the session. It is good to have one day spent on a technical workshop like this in which we could be super focused on the content without any external distraction.

Kudos to Mr Lee for his effort to teach us about data analysis with Python. Till we meet again, hopefully!
