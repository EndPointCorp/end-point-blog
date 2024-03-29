---
author: Tim Case
title: 3 common misconceptions about Ruby on Rails
github_issue_number: 899
tags:
- rails
date: 2013-12-16
---



### 1) Rails is easy to learn.

Rails has a steep learning curve and that’s never going away. From the beginning it was conceived of as an advanced tool for experienced web developers and having a low cost of entry for beginners is not part of the Rails way. Rails makes web development faster by depending on conventions that the developer needs to learn and utilize. There are a lot of these conventions and for a beginner the cost of learning them will be extremely low throughput initially. However, the investment pays off much later down the road when the throughput skyrockets due to familiarity with the framework. Another overlooked thing that makes Rails development hard to learn is that there is a lot more to learn than just Ruby and Rails, there’s also things like source code management, databases, front end servers, testing and while these subjects are common to web development in general, you’ll still need to learn the “Rails way” to approaching these satellite concerns that make up a typical production application. Brook Riggio created this [fantastic chart](https://dgosxlrnzhofi.cloudfront.net/custom_page_images/production/64/page_images/Rails_Competencies.png?1386276348) that shows all the subjects that a Rails dev needs to be familiar with in the excellent article [“Why Learning Rails is Hard”](https://www.codefellows.org/blogs/this-is-why-learning-rails-is-hard), one look at the sheer number of items should illustrate why it takes a long time to learn Rails.

### 2) Rails is equally suited for all types of web apps.

To the extent that your web project veers away from being a dynamic website backed by a relational database with a page-centric design, or to put it another way to the extent that your app is different than Basecamp by 37signals is the extent to which you will be moving out of the sweet spot for developer productivity with Rails. What distinguishes Ruby on Rails from other web frameworks is that it was initially created by extracting it from a real world application rather than developing the framework first. The real world application it was extracted from is Basecamp by 37signals and even to this day the continued development of new Rails features is driven primarily by 37signals’ need to “solve our own problems.” While the web app landscape is evolving to include JavaScript layers that open up the possibilities for new client side architectures, it should be noted that Rails itself is optimized for building HTML pages and displaying them and any other type of architecture that works with Rails is working orthogonal to this goal.

### 3) Rails means you are working with Ruby and Ruby is slow.

Twitter is still sometimes cited as Ruby on Rails’ biggest failure. Twitter was originally developed in Rails and shortly after its creation Twitter went through a phase where rapid growth of the site caused a major implosion of the site’s ability to support the growth and the site was often down during a time that was known as the “Fail Whale” era. The solution to fixing Twitter’s massive scaling problems was to strip out Rails as the engine of the site and introduce a massive messaging infrastructure made up of a multitude of different technologies. Rails was still a part of the infrastructure but only in a very superficial way serving up the web pages for the Twitter web client. This led some to the idea that Twitter was proof that Rails can’t scale and anything “serious” should be done in a different technology. What the Twitter naysayers missed understanding is that the massive messaging behemoth that is Twitter was way outside of what Rails is designed to handle. More importantly however is that the ethos of the Ruby on Rails community is the “right tool for the right job”, and that includes using non-Ruby and non-Rails technologies to support whatever solution you are after. If Java makes it go faster, then use Java. There’s no reason why it has to be in Ruby, and while you might choose to use a Java search engine rather than a Ruby one chances are that Ruby still can act as an excellent “glue language” connecting your Java search engine to other technologies much like the Twitter messaging infrastructure was laid below Rails displaying pages in the web client. Rails devs should be comfortable using things outside of Ruby. A final comment on the Twitter controversy is that it’s not likely Twitter would have ever come into existence without Rails because the low investment needed to try out an idea is precisely how Twitter came to be, and that in itself should be an example of one of Ruby on Rails’ greatest successes.


