---
author: Muhammad Najmi bin Ahmad Zabidi
title: 'Conference Recap: PyCon Asia Pacific (APAC) 2017 in Kuala Lumpur, Malaysia'
github_issue_number: 1345
tags:
- conference
- python
date: 2017-12-02
---
I got a chance to attend the annual PyCon APAC 2017 (Python Conference, Asia Pacific) which was hosted in my homeland, Malaysia. In previous years, Python conferences in Malaysia were held at the national level and this year the Malaysia’s PyCon committee worked hard on organizing a broader Asia-level regional conference.

### Highlights from Day 1

The first day of the conference began with a keynote delivered by Luis Miguel Sanchez, the founder of SGX Analytics, a New York City-based data science/data strategy advisory firm. Luis shared thoughts about the advancement of artificial intelligence and machine learning in many aspects, including demonstrations of automated music generation. In his talk Luis presented his application which composed a song using his AI algorithm. He also told us a bit on the legal aspect of the music produced by his algorithm.

![Luis Miguel Sanchez speaking](/blog/2017/12/pycon-apac-2017/luis.jpg)

<small>Luis speaking to the the audience. Photo from PyCon’s Flickr.</small>

Then I attended Amir Othman’s talk which discussed the data mining technique of news in the Malay and German languages (he received his education at a German tertiary institution). His discussion included the verification of the source of the news and the issue of the language structure of German and Malay, which have similarities with English. First, Amir mentioned language detection using **pycld2**. Amir shared the backend setup for his news crawler which includes RSS and Twitter feeds for input, Redis as a message queue, and Spacy and Polyglot for the “entity recognition”.

Quite a number of speakers spoke about **gensim**, including Amir, who used it for “topic modelling”. Amir also used TF/IDF (term frequency–inverse document frequency) which is a numerical statistic method that is intended to reflect how significant a word is to a document in a corpus. For the similarity lookup aspect, he used **word2vec** on the entire corpus. In the case of full-text search he used Elasticsearch.

Later I attended Mr. Ng Swee Meng’s talk in which he shared his effort in the **Sinar Project** to process the government of Malaysia’s publicly available documents using his Python code. He shared the method of characterization with the use of *bag of words* plus the use of stopwords which has similarity with the English language. Mr. Ng’s work focuses on Malay language documents so he found out that the Indonesian’s Malay language stopwords which are already available could be used to adapt to Malay. Ng also mentioned the use of gensim in his work.

### Highlights from Day 2

The second day’s talk began with a keynote from Jessica McKellar who was involved in the development of Ksplice, Zulip (co-founder), and Dropbox. She highlighted her involvement with San Quentin prison to help the convicts prepare for real-world opportunities after they get out. Jessica also mentioned diversity issues of men and women in computing, race diversity, and technical devices accessibility. Jessica mentioned that problems getting more people involved in computing is not due to lack of interest, but due to lack of access. She also praised the effort done by PyCon UK to help the visually impaired attendees attend a conference. If possible, a conference should be wheelchair friendly too.

![Me standing in the audience](/blog/2017/12/pycon-apac-2017/me.jpg)

<small>Me standing in the audience. Photo from PyCon’s Flickr.</small>

I found the talk by Praveen Patil entitled “Physics and Math with Python” really interesting. Praveen showed his effort to make teaching physics and mathematics interesting for students. Apart from the code snippets he also shared the electronic gadgets which were being used for the subjects.

The other talk which I attended was delivered by Hironori Sekine on the technologies being used by startups in Japan. Hironori mentioned that Ruby is widely used by the Japanese startups and many book publications for Ruby were published in the Japanese language. Other programming languages being used include Java, PHP, Scala, and Go. Python is starting to become more popular since last year as books in the local language started to be published.

### Conclusion

Overall I really appreciate the efforts of the organizer. Though it was the first ever APAC-based PyCon held in Malaysia, I felt that it was very well organized and I could not complain about anything. Thumbs up for the effort and hopefully I can attend next year’s event!
