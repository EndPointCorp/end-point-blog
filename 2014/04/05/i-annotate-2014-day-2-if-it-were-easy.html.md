---
author: Steph Skardal
gh_issue_number: 957
tags: conference, javascript
title: 'I Annotate 2014 Day 2: If it were easy, we would have already solved it'
---

### H2O & Annotator

Yesterday I gave my talk on Integrating Annotator with H2O, which covered the specific implementation details of integrating the open source JavaScript based tool Annotator into [H2O](https://cyber.law.harvard.edu/research/h2o), including a history of annotation and highlights of some of the challenges. I’ll update the link here to my slides when they are available on the I Annotate conference website.

Anyways...

### Version Control

One of the interesting recurring topics of the conference was the concept of version control, version control of text and other multi-media content, and how to present a user interface for version control that makes sense to non-developers (or those not familiar with code based version control). A simple example of what I mean by the problem of version control on the web is described in the following Facebook scenario:

- User A updates status on Facebook
- User B comments on User A’s status
- User C comments on User A’s status, with reference or comment to User B’s status
- User B edits original comment
- User C’s comment no longer is applicable given the context, and doesn’t make sense to users who have not seen User B’s original comment

Facebook doesn’t do anything about this scenario now, other than allow the ability to delete or edit comments. They’ve only recently introduced the ability to edit comments, so while they are aware of this problem, I don’t expect them to build out a complex solution to address this challenge. But if they were to address it, can you imagine both the technical implementation and [intuitive] user interface implementation that would be easily adopted by the masses? If it were easy, it would have already been solved and we wouldn’t be talking about it now!

Apply this Facebook use case to content both off and on the web. In the context of this conference, this is:

- ebooks, PDFs, file types exportable to offline use
- images, video, audio: all mentioned during this conference
- all of the text on the internet

While the above types of content may change at various levels of frequency (e.g. text on the web tends to be more easily and frequently changed than video and audio productions), recording and presenting annotations tied to one piece of content in one state (or version) is very challenging. In text, [Annotator](http://annotatorjs.org/) ties annotations to a specific [Range](https://www.w3.org/TR/2000/REC-DOM-Level-2-Traversal-Range-20001113/ranges.html) of content, so if any of the markup changes, the annotation range may no longer be accurate. [Hypothes.is](https://web.hypothes.is/) has implemented an approach to mitigate this problem (I’m hesitant to describe it as a “solution”) with fuzzy matching, and work is being done to include this work into Annotator. I’m excited to where this goes because I think for this concept of annotation and social discussion around dynamic content [on the web] to work, version control is something that has to be elegantly handled and intuitive in use.
