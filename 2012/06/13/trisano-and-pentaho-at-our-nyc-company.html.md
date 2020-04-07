---
author: Jon Jensen
gh_issue_number: 626
tags: java, open-source, rails, epitrax, ruby, development
title: TriSano and Pentaho at our NYC company meeting
---

Josh Tolley just spoke to us about the [TriSano](https://web.archive.org/web/20120723110816/http://www.trisano.com/) open source project he works on. It helps track and report on public health events, using data at least partly gathered from doctors following special legal reporting requirements to look for epidemics.

<a href="https://www.flickr.com/photos/80083124@N08/7183675839/"><img alt="Josh Tolley speaking at End Point office" height="375" src="/blog/2012/06/13/trisano-and-pentaho-at-our-nyc-company/image-0.jpeg" width="500"/></a>

A lot of this is about data warehousing. Public health officials collect a lot of data and want to easily report on it. Typically they use SPSS. Need to filter the data before doing analysis.

And what is a data warehouse? Store all your data in a different way that’s efficient for querying broken down by time (OLAP). Such queries don’t usually work very well in normal transactional (OLTP) database.

Dimension tables: E.g. different public health departments, sex, disease. Fact tables: Contains the numbers, facts that you may do math aggregation against, and links to dimension tables. The key to the whole process is deciding what you want to track.

Pentaho is what we use for the query interface. To get done what we need to do, we have to make use of unpublished APIs, using JRuby to interface between Pentaho (Java) and TriSano, a Rails app. Postgres is the database.

Brian Buchalter then took over and delved more into the TriSano Rails side of the project.

<a href="https://www.flickr.com/photos/80083124@N08/7368955894/"><img alt="Brian Buchalter speaking at End Point office" height="500" src="/blog/2012/06/13/trisano-and-pentaho-at-our-nyc-company/image-1.jpeg" width="375"/></a>

Let’s talk about the challenge of maintaining Rails applications. Getting them to work today is fine. Getting them to be flexible and change over time is a challenge. The early benefit of Rails was organizational: Having empty directories to put things into. But starting to use standard classic object oriented patterns is finally happening more in Rails.

Brian recommended Sandi Metz’s [talk about the path to better design](https://vimeo.com/26330100), and her upcoming book, [Practical Object Oriented Design in Ruby](https://www.amazon.com/Practical-Object-Oriented-Design-Ruby/dp/0321721330).

Ruby lets you open a class anytime, anywhere, and do whatever you want to it: “monkey patching.” For example, plugins hijacking public methods. It can cause trouble. He strongly recommends watching the video [Capability vs. Suitability by Gary Bernhardt](https://www.youtube.com/watch?v=NftT6HWFgq0), presented at MountainWest Ruby Conf 2012.

Practical limits unveil over time as people customize in ways you don’t expect. For example, a 1300-question form that takes 4 minutes to load. Add arbitrary limits up front so that people understand there’s a design limit rather than a “bug” of bad performance or UI due to unforeseen use cases.

Software is supposed to be easy to change. That’s what people like, and that’s what our employment is all about. But antipatterns emerge that make change harder over time.

How do we work with our clients when there’s technical debt accumulated that will make further development increasingly expensive and troublesome? How do we estimate with imperfect information? Important to keep yourself from losing focus by diving into implementation details.

If you see part of your app that needs to be implemented but has no classes, just helper calls, double your estimate.

If you see lots of conditional blocks in your code, double your estimate. All the additional logic paths greatly increase complexity and make it harder to test.

Don’t Repeat Yourself (DRY) is of course needed. But refactoring code is not (just) about removing duplication: It’s about making code easier to modify forever.

Refactoring needs to be built into the development cycle, or else we end up forever dealing with first-implementation code, simply moving on to the next project.

Comprehensive tests that take 75 minutes to run won’t get run by developers very often! The project automatically runs tests on check-in, but getting the result back takes too long. Would be good to speed up tests.

Lots of good topics to follow up on here.
