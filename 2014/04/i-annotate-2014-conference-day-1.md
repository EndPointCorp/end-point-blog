---
author: Steph Skardal
title: 'I Annotate 2014 Conference: Day 1'
github_issue_number: 956
tags:
- conference
- javascript
date: 2014-04-04
---

I’m here in San Francisco for the second annual [I Annotate](http://iannotate.org/2014/) conference. Today I’m presenting my work on the [H2O](https://h2o.law.harvard.edu/) project, but in this post I’ll share a couple of focus points for the conference thus far, described below.

### What do we mean by Annotations?

Annotation work is off the path of End Point’s ecommerce focus, and annotations means different things for different users, so to give a bit of context: To me, an annotation is markup tied to single target content (image, text, video). There are other interpretations of annotations, such as highlighted text with no markup (ie flagging some target content), and cases where annotations are tied to multiple pieces of target contents.

### Annotations in General

One of the focuses of yesterday’s talks was the topic of how to allow for the powerful concept of annotations to succeed on the web. [Ivan Herman](https://www.ivan-herman.net/professional/index.html) of the W3C touched on why the web has succeeded, and what we can learn from that success to help the idea of annotations. The web has been a great idea, interoperable, decentralized, and open source and we hope that those concepts can translate to web annotations to help them be successful. Another interesting topic [Tom Lehman](https://en.wikipedia.org/wiki/Genius_(website)) of RapGenius touched on was how the actual implementation of annotation doesn’t matter, but rather it’s the community in place to encourage many high quality annotations. For RapGenius, that means offering a user hierarchy that awards users access such as as moderators, editors, contributors, layering on a point-based ranking system, and including encouraging posting RapGenius annotated content in other sites. This talk struck a chord with me, because I know how hard it is to get high quality content for a website.

### Specific Use Cases of Annotator

Yesterday’s talks also covered several interesting use cases of [Annotator](http://annotatorjs.org/), an open source JavaScript-based tool that aims to be the reference platform for web annotations that has been commonly adopted in this space, which is what we are using in H2O. Many of the people attending the conference are using Annotator and interested in its future and capabilities. Some highlights of implementation were:

- [RapGenius](https://genius.com/): Aforementioned, contains active community of annotating lyrics.
- SocialBook: A classroom and/or “book club” application for interactive discussions and annotations of books.
- [FinancialTimes](https://www.ft.com/): From my understanding, annotations are the guide to how content is aggregated and presented in various facets of the BBC website.
- [annotationstudio.org](http://www.annotationstudio.org/): collaborative web-based annotation tools under development at MIT which has similarities to H2O.
- [AustESE](http://www.itee.uq.edu.au/eresearch/projects/austese): Work being done in Australia for scholarly editing, includes a Drupal plugin implemented using Annotator with several plugins layered on top, including image annotation, categorization, threaded discussions.
- [hypothes.is](https://web.hypothes.is/): Hypothes.is uses tool built on top of annotator, featuring several advanced features such as image annotation, bookmarklet annotation implementation, and real time stream updates with search.

After the morning talks, we broke into two longer small group sessions, and I joined the sessions to delve into deeper issues and implementation details of Annotator, as well as the challenges and needs associated with annotation the law. I’ll share my presentation and more notes from today’s talks. Stay tuned!
