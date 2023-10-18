---
title: "Middleware: Is that still a thing?"
author: Richard Templet
date: 2022-05-26
tags:
  - development
  - integration
  - architecture
  - api
github_issue_number: 1865
---

![Photo looking from ground level up at concrete and crushed stone building against a blue sky with some white clouds](/blog/2022/05/middleware-is-that-still-a-thing/20220401-013133.webp)

<!-- photo by Jon Jensen -->

The simple answer to the question in the title is simply, yes! Despite the term being many decades old and well past its hype peak, middleware is still very much a thing and has become a key part of the technical landscape that is critical in day-to-day functioning of systems.

So there are still some questions to be answered: What is middleware? What does it do? And maybe most importantly: Why do we care?

### What is it?

In its simplest meaning, middleware is an application that sits between other applications and shuffles data between them. There is normally one system requesting the information and the middleware figures out where to get that requested data and makes the request to another system.

An easy example of this is buying something at a retail store using your credit or debit card. When you swipe your card, the business makes a request to a service (some middleware) to ask if there's enough room on the card for that purchase. Then that system makes a request to the appropriate bank or card holding company to ask the same question. The bank or card holding company replies with either a yes or no and that answer is then relayed back to the terminal where you swiped your card.

You might be thinking, “Why do we need the middleware? Just have the terminal ask the right bank!” Well, that’s a benefit of middleware: The terminal software doesn’t need to have all the same logic coded into it to know whether or how to talk to Visa or Mastercard as well as Citibank or Capital One or Bank of America to get the answer. It just talks to the middleware and lets it figure all of that out. This way you can have many different types of terminals or credit card taking applications available but only one middleware application needs to have the smarts and authorization to know where and how to get the answer.

The term middleware is most often used to describe business systems internal to a company. It is a subset of the broader concept "API" (application programming interface), which includes services provided for external users, either the general public or specific authorized customers or business partners. If a service is used directly by humans of the general public, it is typically called SaaS (software as a service).

### What does it do?

As I explained in the example above, the simplistic definition of middleware is an application that shuffles data between two systems. In reality, middleware is sometimes way more complicated than that!

In that example of a credit card charge terminal, using middleware also allows for the retailer to set centralized company-wide rules for fraud screening, add or remove supported payment methods, or change which payment gateway is used, without having to update each terminal individually.

Middleware also can do data manipulation and mapping between two systems. Let’s consider a more complicated case like booking a cross-country flight.

You’ve probably used sites like Google Flights or Expedia to search for ticket costs. You go to their site, put in your starting airport(s) and your destination airport(s), select the dates when you’d like to travel, and maybe check the box saying you’ve got some wiggle room on when you leave and come back. After that you click the search button and within a few seconds, you’ve got tons of flight options to sort through! The search results can be sorted by price, number of stops, and airlines, to name a few.

So taking a step back to marvel at what just happened, how do you think they got that much data from that many sources so quickly? Well, the answer is middleware.

At some point, a middleware system made a request to each of the airlines to ask for their available flights with their dates, costs, amenities, etc. and stored that information on their own system to be used for your search. There are many different ways that data could be captured. We won’t delve into all that excitement, but what we do know is some system (middleware) had to fetch this data from each of the airlines and store it to be used for your search. It has to organize and store that data in a way that makes sense to the search engine to use so you can get back your search results in a speedy fashion.

There’s a good chance that the data from American Airlines will differ in its structure and data points compared to Delta. It’s the middleware’s job to take each of those data feeds and organize and store them somewhere for the search engine to use. In this part of the example, the middleware is taking a request to fetch the Delta flight data, turning that request into a request to another system for the data then doing whatever data manipulation and storage of that data to satisfy the search engine.

### Why do we care?

The main reason that we care is we’ve become used to having a single location (website, application etc.) that allows us access to data from multiple places.

In our credit card example, there are many different types of credit cards we can use to check out at our local gas station. Having them require us to only use a Shell gas card would be bad for their business! We’ve grown accustomed to being able to use our Visa, Mastercard, American Express, or Shell gas card at that same gas station. This is all made possible due to middleware behind the scenes doing the hard work.

In many cases, the function of gathering data from many sources in one place, keeping it current, and allowing it to be searched, sorted, etc. is not just one means to an end, but it actually *is* the whole business! It is why services like Google Flights and Expedia exist.

Middleware can serve many other purposes even when only used internally by a single company:

* **authentication** — making sure who- or whatever made a request is supposed to be able to
* **authorization** — making sure the kind of request being made is one this user is allowed to
* **auditing** — logging or sampling traffic in middleware is often more comprehensive and convenient than at each service individually
* **rate-limiting** — ensuring the user is not using too many resources too fast, or that one service isn’t overused and interfering with access to other services
* **caching** — storing answers to frequent requests to reuse for a limited time, reducing the number of live requests to busy internal applications and databases
* **billing** — tracking usage so it can be paid for or at least each user’s usage is fairly recorded
* **fault-tolerance** — retrying a request if an internal system is temporarily unavailable, or rerouting requests to a different system, to shield users from outages
* **load balancing** — spreading requests across multiple services to allow greater total throughput
* **translation** — modern APIs typically use JSON to structure their data, and middleware can translate between a nice JSON interface and older systems using a variety of more complex and archaic data formats
* **migrations** — transparently moving from an old system to a newer one, possibly in phases or temporarily for testing, without users having to change anything or even be aware

In closing, while middleware isn’t commonly mentioned or even thought about, it is a very important part of what makes the technological world function.
