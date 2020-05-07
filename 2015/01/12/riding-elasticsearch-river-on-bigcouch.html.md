---
author: Brian Gadoury
gh_issue_number: 1067
tags: couchdb, elasticsearch, rails
title: 'Riding the Elasticsearch River on a CouchDB: Part 1'
---

As you may guessed from my perfect tan and rugged good looks, I am Phunk, your river guide. In this multi-part series, I will guide us through an exploration of [Elasticsearch](https://www.elastic.co/), its [CouchDB/BigCouch River plugin](https://github.com/elastic/elasticsearch-river-couchdb), its source, the [CouchDB document store](http://couchdb.apache.org/), and the surrounding flora and fauna that are the Ruby on Rails based tools I created to help [the DPLA](https://dp.la/) project manage this ecosystem.

Before we get our feet wet, let’s go through a quick safety briefing to discuss the terms I’ll be using as your guide on this trip. Elasticsearch: A schema-less, JSON-based, distributed RESTful search engine. The River: An Elasticsearch plugin that automatically indexes changes in your upstream (heh) document store, in real-time. CouchDB: The fault-tolerant, distributed NoSQL database / document store. DPLA: The Digital Public Library of America open source project for which all this work was done.

Let’s put on our flotation devices, don our metaphor helmets and cast off.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2015/01/12/riding-elasticsearch-river-on-bigcouch/image-0-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2015/01/12/riding-elasticsearch-river-on-bigcouch/image-0.jpeg"/></a></div>

In an Elasticsearch + River + CouchDB architecture, all things flow from the CouchDB. For the DPLA project, we wanted to manage (create, update and delete) documents in our CouchDB document repository and have those changes automagically reflected in our Elasticsearch index. Luckily, CouchDB publishes a real-time stream (heh) of updates to its documents via its cleverly named “_changes” feed. Each change in that feed is published as a stand-alone JSON document. We’ll look at that feed in more detail in a bit.

The River bridges (heh) the gap between CouchDB’s _changes feed and Elasticsearch index. The plugin runs inside Elasticsearch, and makes a persistent TCP connection to CouchDB’s _changes endpoint. When a new change is published to that endpoint, the River passes the relevant portions of that JSON up to Elasticsearch, which then makes the appropriate change to its index. Let’s look at a simple timeline of what the River would see from the _changes feed during the creation of a new document in CouchDB, and then an update to that document:

A document is created in CouchDB, the _changes feed emits:

```javascript
{
  "seq":1,
  "id":"test1",
  "changes":[{"rev":"1-967a00dff5e02add41819138abb3284d"}],
  "doc":{
    "_id":"test1",
    "_rev":"1-967a00dff5e02add41819138abb3284d",
    "my_field":"value1"
  }
}
```

That same document is updated in CouchDB, the _changes feed emits:

```javascript
{
  "seq":2,
  "id":"test1",
  "changes":[{"rev":"2-80647a2a9498f5c124b1b3cc1d6c6360"}],
  "doc":{
    "_id":"test1",
    "_rev":"2-80647a2a9498f5c124b1b3cc1d6c6360",
    "my_field":"value2"
  }
}
```

It’s tough to tell from this contrived example document, but the _changes feed actually includes the entire source document JSON for creates and updates. (I’ll talk more about that in part 2.) From the above JSON examples, the River would pass the inner-most document containing the _id, _rev and my_field data up to Elasticsearch. Elasticsearch uses that JSON to update the corresponding document (keyed by _id) in its search index and voila, the document you updated in CouchDB is now updated in your Elasticsearch search index in real-time.

We have now gotten our feet wet with how a document flows from one end to the other in this architecture. In part 2, we’ll dive deeper into the DevOps-heavy care, feeding, monitoring and testing of the River. We’ll also look at some slick River tricks that can transform your documents before Elasticsearch gets them, and any other silly River puns I can come up with. I’ll also be reading the entire thing in my best [David Attenborough](http://www.bbc.co.uk/nature/collections/p0048522) impression and posting it on SoundCloud.
