---
author: Wojtek Ziniewicz
title: 'wroc_love.rb 2017 part 2: The Elixir Hype'
github_issue_number: 1293
tags:
- clojure
- conference
- elixir
- rails
- ruby
- scalability
date: 2017-03-21
---

One of the main reasons I attend [wroc_love.rb](https://wrocloverb.com/) almost every year, is that it’s a great forum for confronting ideas. It’s almost a tradition to have at least 2 very enjoyful discussion panels during this conference. One of them was devoted to [Elixir](http://elixir-lang.org/) and why the Ruby [1] community is so hyping about it.

#### Why Elixir is “sold” to us as “new better Ruby” while its underlying principles are totally different? Won’t it result in Elixir programmers that do not understand Elixir (like Rails programmers that do not know Ruby)?

 **Panelists discussed briefly the history of Elixir:**

Jose Valim (who created Elixir) was working on threading in Rails and he was searching for better approaches for threading in web frameworks. He felt like lots of things were lacking in Erlang and Elixir is his approach for better Exceptions, better developer experience.

**Then they jumped to Elixir’s main goals which are:**

- Compatibility with Erlang (all datatypes)
- Better tooling
- Improving developers’ experience

**After that, they started speculating about problems that Elixir solves and RoR doesn’t:**

Ruby on Rails addresses many problems in ways that may be somehow archaic to us in the ever-​scaling world of 2017. There are many approaches to it, e.g. “actor model” which is implemented in Ruby by Celluloid, in Scala with Akka and also Elixir and Phoenix (Elixir’s rails-like framework) has its own actor model.

Phoenix (“Rails for Elixir”) is just an Elixir app—​unlike Rails, it is not separate from Elixir. Moreover Elixir is exactly the same language as Erlang so:

Erlang = Elixir = Phoenix

Great comment:

<blockquote class="twitter-tweet" data-lang="en">
<div dir="ltr" lang="en">
Elixir is same as Erlang but not really <a href="https://twitter.com/hashtag/wrocloverb?src=hash">#wrocloverb</a></div>
— Daria Woznicka (@DWoznicka) <a href="https://twitter.com/DWoznicka/status/843102967339384832">March 18, 2017</a></blockquote>

**Then a discussion followed during which panelists speculated about the price of the jump from Rails to Elixir:**

The Java to Rails jump was caused by business/​productivity. There’s no such jump for Phoenix/​Elixir. Elixir code is more verbose (less instance variables, all args are passed explicitly to all functions).

### My conclusions

A reason why this discussion was somehow shallow and pointless was that those two worlds have different problems. Great comment:

<blockquote class="twitter-tweet" data-lang="en">
<div dir="ltr" lang="en">
Ruby guys focus on business. Elixir guys on technical aspects <a href="https://twitter.com/hashtag/wrocloverb?src=hash">#wrocloverb</a></div>
— Michał Łomnicki (@mlomnicki) <a href="https://twitter.com/mlomnicki/status/843106473358049280">March 18, 2017</a></blockquote>

Elixir solves a lot of technical problems with scaling thanks to [Erlang’s](https://www.erlang.org/) virtual machine. Such problems are definitely only a small part of what typical Ruby problem-​solvers deal with on a daily basis. Hearing Elixir and Ruby on Rails developers talk past each other was probably the first sign of the fact that there’s no hyping technology right now. Each problem can be addressed by many tech tools and frameworks.

[1] Wrocloverb describes itself as a “best Java conference in Ruby world”. It’s deceiving:

<blockquote class="twitter-tweet" data-lang="en">
<div dir="ltr" lang="en">
<a href="https://twitter.com/hashtag/wrocloverb?src=hash">#wrocloverb</a> was great Clojure conference :)<br />
Thanks for all organizers and speakers!</div>
— Jakub Cieślar (@jcieslar_) <a href="https://twitter.com/jcieslar_/status/843596752926269443">March 19, 2017</a></blockquote>
