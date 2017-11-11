---
author: Selvakumar Arumugam
gh_issue_number: 1113
tags: community, conference, ruby, rails
title: RubyConf India 2015
---

The 6th edition of RubyConf India 2015 was held at Goa (in my opinion, one of the most amazing places in India). The talks were spread over various topics, mainly related to Ruby generally and RoR.

Aaron Patterson (a core member of Ruby and Rails team) gave a very interesting talk about Pair Programming, benchmarking on Integration tests vs Controller tests and precompiling the view to increase the speed in Rails 5.

Christophe Philemotte presented a wonderful topic on "[Diving in the unknown depths of a project](https://speakerdeck.com/toch/rubyconf-india-2015-diving-in-the-unknown-depth-of-a-project)" with his experience of contributing to the Rails project. He mentioned that 85% of a developer’s time is spent on reading the code and 15% of the time is spent on writing the code. So he explained a work process plan to make use of the developer’s time effectively which should adopt well to any kind of development. Here is the list of steps he explained:

1. Goal (ex: bug fixing, implement new feature, etc… )
1. Map (ex: code repository, documentation, readme, etc…)
1. Equipment (ex: Editor, IDE) and Dive (read, write, run and use)
1. Next Task

Rajeev from ThoughtWorks talked about "[Imperative vs Functional programming](https://speakerdeck.com/rshetty01/functional-geekery-for-an-imperative-mind)" and interesting concepts in Haskell which can be implemented in Ruby, such as function composition, lazy evaluation, thunks, higher order functions, currying, pure functions and immutable objects.

Aakash from C42 Engineering talked about an interesting piece of future web components called "Shadow DOM" which has interoperability, encapsulation and portability features built-in. He also mentioned [polymer](https://www.polymer-project.org) as a project to develop custom Shadow DOM.

Vipul and Prathamesh from BigBinary showed an experimental project of "[Building an ORM with AReL](https://github.com/prathamesh-sonpatki/torm)" which is Torm (Tiny Object Relation Mapping) to gain more control over the ORM process in Rails.

Smit Shah from Flipkart gave a talk on "Resilient by Design" which follows some design patterns like 1. Bounding - change the default timeouts 2. Circuit breakers 3. Fail Fast

Christopher Rigor shared some awesome information about "[Cryptography for Rails Developers](https://speakerdeck.com/crigor/cryptography-for-rails-developers-rubyconfindia)". He explained some concepts like Public Key cryptography, symmetric cryptography, and SSL/TLS versions. He recommended we all use TLS 1.2 and AES-GCM on production to keep the application more secure.

Eleanor McHugh, a british hacker gave an important talk on "[Privacy is always a requirement](http://www.slideshare.net/feyeleanor/privacy-is-always-a-requirement)". The gist of the talk is to keep security tight by encrypt all transports, encrypt all passwords, provide two-factor authentication, encrypt all storage and anchor trust internally. The data won't by safe by privacy or trust or contract in the broken internet world.

Laurent Sansonetti who works for RubyMotion gave a demo of a Floppy bird game which he created using RubyMotion with code walkthrough. RubyMotion is used to develop native mobile applications for iOS, OS X and Android platforms. It provides features to use Objective-C API and Android API, and the whole build process is Rake-based.

Shadab Ahmed gave a wonderful demo on the 'aggrobot' gem, used to perform easy aggregations. aggrobot runs on top of ActiveRecord as well as working directly with database to provide good performance on query results.

Founder and CEO of CodeClimate Bryan Helmkamp spoke about "Rigorous Deployment" using a few wonderful tools. The ‘rollout’ gem is extensively helpful to deploy to specific users, specific branch deployment, etc… So there is no need of staging environment and it helps to avoid things like 'it works in staging, not production'

Erik Michaels-Ober gave an awesome talk on "[Writing Fast Ruby](https://speakerdeck.com/sferik/writing-fast-ruby)" (must-visit slides) with information about how to tweak regular code to improve the performance of the application. He also presented the Benchmark/IPS results of two versions of code with working logic and execution time. He mentioned as a rule-of-thumb that any performance improvement changes should require at least 12% improvement compare to current code.

The final presenter Terence Lee from the Ruby Security Team gave a talk on "Ruby & You" which summarised all the talks and gave information on the Ruby Security Team and its contribution to Ruby community. He suggested everyone to keep their Ruby version up-to-date so to get the latest security patches and avoid vulnerabilities. He also encouraged the audience to submit bug reports to the official [Ruby ticketing system](https://bugs.ruby-lang.org) because, quoting him, "Twitter is not bug tracker".

It was really fascinating to interact with like minded people and I was very happy to leave the conference with many new interesting ideas and input about Ruby and RoR along with some new techie friends.
