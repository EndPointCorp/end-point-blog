---
author: Muhammad Najmi Ahmad Zabidi
title: "Conference Recap: Pycon Asia Pacific (APAC) 2017 in Kuala Lumpur, Malaysia"
tags: conference, Malaysia
---
*(Disclaimer: All pictures inside this post are originally from Pycon APAC's Flickr public account)*

I got a chance to attend the annual Pycon APAC 2017 (Python Conference, Asia Pacific) which was fortunately hosted in my homeland, Malaysia. In the previous years, Python conferences in Malaysia were held at the national level and this year the Malaysia's Pycon committee worked hard on organizing the APAC level conference.

### Highlights from Day 1

The first day of the conference began with a keynote delivered by Luis Miguel Sanchez, the founder of SGX Analytics, a NYC based Data Science/Data Strategy advisory firm. Luis shared thoughts about the advancement of artificial intelligence and machine learning in many aspects; which included demonstrations of automated music generation. In his talk Luis presented his application which intelligently composed a song with his AI algorithm. He also told us a bit on the legal aspect of the music produced by his algorithm.

![Luis spoke in front of the audience. Pic taken from Pycon's Flickr](/2017/11/28/pycon-apac-2017/luis.jpg)

Then, I attended Amir Othman's talk which discussed the data mining technique of news in the Malay language and Germany (he received his education at a German tertiary institution). His discussions included the verification of the source of the news and the issue of the language structure of Germany and Malay language (which have similarities with the English language). First, Amir mentioned about the language detection, in which he used **pycld2** to do that. Amir shared the backend setup for his news crawler which includes RSS/Twitter feed for input, the use of Redis for message queue, Spacy and Polyglot for the "entity recognition". I found quite a number of speakers spoke about **gensim** including Amir in which he used it for "topic modelling". Amir also used TF/IDF (term frequency–inverse document frequency) which is a numerical statistic method that is intended to reflect how significant a word is to a document in a corpus. For the similarity lookup aspect, he used **word2vec** on the entire corpus. In the case of full-text search he used ElasticSearch to do that.

Later I attended Mr Ng Swee Meng's talk in which he shared his effort in *Sinar Project* to process the government of Malaysia's publicly available document by his Python codes. He shared the method of characterization with the use of *bag of words* plus the use of stopwords which has similarity with the English language. Mr Ng's work is focusing on Malay language related documents so he found out the the Indonesian's Malay language stopwords which is already available could be use to adapt with Malaysian's Malay language. Ng also mentioned the use of *gensim* in his work.

### Highlights from Day 2
The second day's talk was started with a keynote from Jessica McKellar who was involved in the development of Ksplice, Zulip (co-founder) and Dropbox. She highlighted her involvement with San Quentino prison to help the convicts preparing for the real world opportunities when they get out from that place. Jessica also mentioned about the diversity issue (gender - men and women in computing, race diversity and technical devices accessibility). Jessica mentioned that the issue of getting more people involved in the computing not due to lack of interest, but due to lack of access. She also praised the effort done by Pycon UK (which should be an example to any conference) to help the visually impaired attendees to attend a conference, plus if possible, a conference should be a wheel chair friendly event too.

<a href="/2017/11/28/pycon-apac-2017/me.jpg"><img src="/2017/11/28/pycon-apac-2017/me.jpg"/></a>

I found a talk by Praveen Patil with a title of "Physics and Math with Python" was really interesting. In his talk Praveen showed his effort to make the teaching process of Physics and Mathematics become interesting. Apart from the code snippets he also shared the electronic gadgets which were being used for the subjects.

The other talk which I attended was delivered by Hironori Sekine on the nature technologies that being used by startups in Japan. Hironori mentioned that Ruby is widely used by the Japanese startup and many book publications for Ruby were published in the local language. The other programming languages that being used including Java, PHP, Scala and Go. Python is starting to become more popular starting 2016 and books in the local language started to be published.

### Conclusion
In overall I really appreciate the efforts that were being done by the organizer. Though it was the first ever APAC-based Pycon being held in Malaysia, I personally felt that it was very organized and I could not complain anything bad about it. Thumbs up for the effort and hopefully I could attend the similar event next year!
