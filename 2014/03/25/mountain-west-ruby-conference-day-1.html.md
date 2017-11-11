---
author: Mike Farmer
gh_issue_number: 951
tags: conference, ruby, rails
title: Mountain West Ruby Conference, Day 1
---

<table align="center" cellpadding="0" cellspacing="0" class="tr-caption-container" style="float: right; margin-left: 1em; text-align: right;"><tbody>
<tr><td style="text-align: center;"><img border="0" src="/blog/2014/03/25/mountain-west-ruby-conference-day-1/image-0.jpeg" style="margin-left: auto; margin-right: auto;"/></td></tr>
<tr><td class="tr-caption" style="text-align: center;">MWRC Notes</td></tr>
</tbody></table>

It’s that magical time of year that I always look forward to, March. Why March? Because that’s when [Mike Moore](https://twitter.com/blowmage) organizes and puts on the famed [Mountain West Ruby Conference](http://mtnwestrubyconf.org/) in Salt Lake City, Utah. This conference is always a personal pleasure for me due to the number of incredible people I get to meet and associate with there. This year was no exception in that regard. It was simply fantastic to meet up with old friends and catch up on all their latest and greatest projects and ideas.

In writing a summary of day 1 here, I’d like to focus on just three talks that you will definitely want to go watch over on [confreaks](http://www.confreaks.com/) as soon as they are up. All the talks were great, but these three were exceptional and you won’t want to miss them.

## A Magical Gathering

The opening keynote started off with a bang of entertainment and just plain geeking out with [Aaron Patterson](https://twitter.com/tenderlove). Aaron holds the peculiar position of being on both Ruby core and Rails core teams. Aaron’s code is probably used by more people than just about anyone in the Ruby community. Everyone that knows and loves Ruby and Ruby on Rails is indebted to this genius and generous coder. But Aaron is more than just a coder. Other than Matz himself, I don’t think anyone has influenced the culture of Ruby more than Aaron. Matz wants all of us to be nice (MINASWAN: Matz is nice and so we are nice) and Aaron just wants us to just love what we do and love the people that we work with ([#fridayhug](https://twitter.com/search?q=%23fridayhug) with [@tenderlove](http://tenderlovemaking.com/)).

Aaron gave an entertaining talk on how he built an app that reads “[Magic, the Gathering Cards](http://www.wizards.com/Magic/Summoner/)”. Turns out Aaron was a big fan of the game several years ago and had accumulated quite a stash of cards (2600+). He recently gained an interest in the game again and wanted to see what he had as far as the quality of the cards. To accomplish this task, he built an app that uses a webcam to take a picture of the card. Then he compared it with a database that he scraped from the Gatherer website. He then used a bunch of Ruby libraries and other tools to do an image comparison and “teach” his app how to match the cards. In the end, this talk was not only extremely entertaining but introduced me to a whole bunch of tools that I never knew existed. Here’s a list of tools and sites referenced in his talk:

- [OpenCV](https://github.com/ruby-opencv/ruby-opencv) for cropping and straightening images
- [Magic the Gathering Gatherer](http://gatherer.wizards.com/Pages/Default.aspx) for getting card data
- [MTG JSON](http://mtgjson.com/) for getting card data in JSON format (easier than scraping)
- [Phashion](https://github.com/westonplatter/phashion) Ruby gem for comparing similar images and generating a hamming distance between the two

## Unpacking Technical Decisions

The next talk that impressed me was [Unpacking Technical Decisions](https://speakerdeck.com/sarahmei/unpacking-technical-decisions-mountain-west-ruby-conf-2014) by [Sarah Mei](http://www.sarahmei.com/blog/). Sarah gracefully walked us through a very difficult technical decision that all web developers seem to face these days, “What JavaScript framework should I use?” Although the question was based on JavaScript and not Ruby, the principles that were discussed could be related to any project.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/03/25/mountain-west-ruby-conference-day-1/image-1-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/03/25/mountain-west-ruby-conference-day-1/image-1.png"/></a></div>

Sarah broke our decision making questions into a quadrant system, aptly named The Mei System. The quadrants were identified as Accessibility, Interface, Popularity, and Activity. Then we looked at three of the more common JavaScript Frameworks [Ember](http://emberjs.com/), [Angular](http://angularjs.org/), and [Backbone](http://backbonejs.org/). Using the quadrant Sarah pointed out how any one of the frameworks could work based on the project we are working on and the people that will be working on the project. The conclusion was that none of these frameworks are the “best” framework in the large, but it is possible to make a good decision on what framework would be best for your project.

## Don’t

The last talk I want to mention here was the final talk for the day by [Ernie Miller](http://erniemiller.org/) titled “Don’t”. The premise for the talk is that we all make mistakes. Some are harder to handle than others. Ernie’s goal was to help us avoid some of the same mistakes that he made. This was a very candid look at Ernie’s past that was both entertaining and moving. Ernie presented us with mistakes in of a wide variety from programming mistakes to life mistakes. To conclude this blog post, I present to you the list of Ernie’s “Don’t” mistakes.

- Don’t overestimate how much time you have. Do thank someone who’s had a positive impact on your life.
- Don’t forget your choices have consequences.
- Don’t fall in love with metaprogramming.
- Don’t put your code in buckets (meaning god objects). Do find a real home for your code and give it a proper name.
- Don’t hitch your cart to someone else’s cart (couple your code to gems).
- Don’t think of your app as a “Rails App”.
- Don’t assume too much how other will use your code.
- Don’t use ActiveRecord Callbacks. Do use super!
- Don’t mistake the illusion of accomplishment for the real thing (addictive gaming).
- Don’t accept counter-offers.
- Don’t take a job for the money.
- Don’t assume it’s too late.
- Don’t get too comfortable. Do work at a job that pushes you and holds you accountable.
- Don’t try to be someone you’re not.
- Don’t be afraid.
- Don’t be afraid to say no.
- Don’t be afraid to share.
- Don’t be afraid to speak.
- Don’t be afraid to stretch.
