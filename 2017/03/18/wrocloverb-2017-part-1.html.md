---
author: Wojtek Ziniewicz
gh_issue_number: 1292
tags: distributed-computing, machine-learning, message-queues, ros, ruby, spree, ecommerce, conference
title: Wrocloverb 2017 part 1
---

Wrocloverb is a single-track 3-day conference that takes place in Wrocław (Poland) every year in March.

Here's a subjective list of most interesting talks from the first day

## # Kafka / Karafka (by Maciej Mensfeld)

[Karafka](https://github.com/karafka/karafka) is another library that simplifies Apache Kafka usage in Ruby. It lets Ruby on Rails apps benefit from horizontally scalable message busses in a pub-sub (or publisher/consumer) type of network.

**Why [Kafka](https://kafka.apache.org/) is (*probably*) better message/task broker for your app:**

- broadcasting is a real power feature of kafka (http lacks that)

- author claims that its easier to support it  rather than ZeroMQ/RabbitMQ

- it's namespaced with topics (similar to [Robot Operating System](http://www.ros.org/))

- great replacement for [ruby-kafka](https://github.com/zendesk/ruby-kafka) and [Poseidon](https://github.com/bpot/poseidon)

> Karafka [https://t.co/g9LQZiAV4i](https://t.co/g9LQZiAV4i) microframework to have [#rails](https://twitter.com/hashtag/rails?src=hash)-like development performance with [#kafka](https://twitter.com/hashtag/kafka?src=hash) in [#ruby](https://twitter.com/hashtag/ruby?src=hash) [@maciejmensfeld](https://twitter.com/maciejmensfeld) [#wrocloverb](https://twitter.com/hashtag/wrocloverb?src=hash)
>
> — Maciek Rząsa (@mjrzasa) [17 marzo 2017](https://twitter.com/mjrzasa/status/842771868239192064)

## # Machine Learning to the Rescue (Mariusz Gil)

This talk was devoted to Machine Learning success (and failure) story of the author.

Author underlined that Machine Learning is a **process**and proposed following **workflow**:

1. define a problem
1. gather you data
1. understand your data
1. prepare and condition the data
1. select & run your algorithms
1. tune algorithms parameters
1. select final model
1. validate final model (test using production data)

Mariusz described few ML problems that he has dealt with in the past. One of them was a project designed to estimate cost of a code review. He outlined the process of tuning the input data. Here's a list of what comprised the input for a code review estimation cost:

- number of lines changed
- number of files changed
- [efferent](https://en.wikipedia.org/wiki/Efferent_coupling) coupling
- [afferent](https://en.wikipedia.org/wiki/Coupling_(computer_programming)) coupling
- number of classes
- number of interfaces
- inheritance level
- number of method calls
- lloc metric
- lcom metric (whether single responsibility pattern is followed or not)

## # Spree lightning talk by [sparksolutions.co](http://sparksolutions.co/)

One of the lightning talks was devoted to Spree. Here's some interesting latest data from the Spree world:

- number of contributors of spree - 700
- it's very modular modular
- it's api driven
- it's one of the biggest repos on github
- very large number of extensions
- it drives thousands of stores worldwide
- [Spark Solutions](http://sparksolutions.co/) is a maintainer
- Popular companies that use spree: Go Daddy, Goop, Casper, Bonobos, Littlebits, Greetabl
- it support rails 5, rails 4.2 and rails 3.x

Author also released newest 3.2.0 stable version during the talk:

> releasing spree 3.2.0 live during lightning talk [#wrocloverb](https://twitter.com/hashtag/wrocloverb?src=hash) [pic.twitter.com/9oPcB5CTfB](https://t.co/9oPcB5CTfB)
>
> — Wojciech Ziniewicz (@fribulusxax) [17 marzo 2017](https://twitter.com/fribulusxax/status/842800094915301376)
