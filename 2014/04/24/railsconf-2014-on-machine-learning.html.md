---
author: Steph Skardal
gh_issue_number: 972
tags: conference, rails, machine-learning
title: RailsConf 2014 on Machine Learning
---

This year at RailsConf 2014, there are workshop tracks which are focused sessions double or triple the length of the normal talk. Today I attended *Machine Learning for Fun and Profit* by [John Paul Ashenfelter](https://twitter.com/johnashenfelter). Some analytics tools are good at providing averages on data (e.g. Google Analytics), but averages don't tell you a specific story or context of your users, which can be valuable and actionable. In his story-telling approach, John covered several stories for generating data via machine learning techniques in Ruby.

### Make a Plan

First, one must formulate a plan or a goal for which to collect actionable data. More likely than not, the goal is to make money, and the hope is that machine learning can help you find actionable data to make more money! John walked through several use cases and examples code with machine learning and I'll add a bit of ecommerce context to each story below.

### Act 1: Describe your Users

First, John talked about a few tools used for describing your users. In the context of his story, he wanted to figure out what gender ratio of shirts to order for the company. He used the [sexmachine gem](https://github.com/bmuller/sexmachine ), which is based on census data, to predict the sex of a person based on a first name. The first name from all your users would be passed into this gem to segregate via gender, and from there you may be able to take action (e.g. order shirts with an estimated gender ratio).

Next, John covered geolocation. John wanted to how to scale support hours to customers using the product, likely a very common reason for geolocation for any SaaS or customer-centric tools. His solution uses [freegeoip.net](http://freegeoip.net/), Python and Go, and free [Maxmind data](http://www.maxmind.com/en/geolocation_landing). The example code is available [here](https://github.com/johnpaulashenfelter/railsconf2014-ml/tree/master/ex2_geolocation).

With these tools, gender assignment & geolocation reveals basic but valuable information about your users. In the ecommerce space, determining gender ratios and geolocation may help determine the target of marketing and/or product development efforts, for example targeting a specific marketing message to a female East Coast demographic.

### Act 2:  Clustering

In the next step, John talked about using machine learning to cluster users. The context John provided was to cluster users into three groups: casual users, super users and professional users, to potentially learn more about the super users and how to get more users in that group. An ecommerce story might be to cluster users in amount spent buckets which have rewards at higher levels, to incentivize users to spend more money to climb the hierarchy for more rewards. Here John used [ai4r](https://github.com/SergioFierens/ai4r) gem, which uses [k-means clustering](http://en.wikipedia.org/wiki/K-means_clustering) to group users. In as few words as possible, k-means clustering randomly creates X clusters (step 1), computes the center of each cluster (step 2), moves nodes if they are closer to a different cluster center (step 3), and repeats steps 2 & 3 until no nodes have been moved. The actual code is quite simple with the gem. Alternative clustering tools are [hierarchical clusterers](http://en.wikipedia.org/wiki/Hierarchical_clustering) or [divisive hierarchical clustering](https://www.google.com/search?q=divisive+hierarchical+clustering), which will yield slightly different results. John also mentioned that there are  much better numerical tools like Python, R, Octave/Matlab, and Mathematica.

### Act 3: Similarity

The third and final topic John covered was determining similarity between users, or perhaps finding other users similar to user X. The context of this was to understand how people collaborate and spread knowledge. In the ecommerce space, the obvious use-case here is building a product recommendation engine, e.g. recommending products to a user based on what they have bought, are looking at, or what is in their cart. John didn't dive into the specific linear algebra math here (linear algebra is hard!), but he provided [example code](https://github.com/johnpaulashenfelter/railsconf2014-ml/tree/master/ex4_similarity) using the [linalg](https://github.com/quix/linalg) gem that does much of the hard work for you.

### Conclusion

The conclusion of this workshop was again to share Ruby tools that can help solve problems about your user and business. It's very important to have a plan and/or goal to strive for and to determine actionable data analysis and metrics to help reach those goals.
