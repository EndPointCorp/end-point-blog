---
author: "Kevin Campusano"
title: "Automated Testing with Symfony"
tags: testing, automated-testing, unit-testing, functional-testing, symfony, phpunit, php
---

![Banner](auomated-testing-with-symfony/banner.png)
https://stackoverflow.com/questions/61400/what-makes-a-good-unit-test

# An introduction to automated testing by example with the Symfony framework

Testing is an immense topic in software engineering. A lot has been written and a lot of experience has been collected about it by the greater software development community. There are many types of testing that can be done, many techniques and approaches, filosofies and strategies.

With a big topic such as this, it would be futile to try to touch on every aspect of it in an article like this. Instead, I'll try to take a pragmatic approach and discuss a testing strategy that I've found success with in the past, and the amount of testing with which I feel confortable putting code into production. This article could also serve as a sort of introduction to automated testing, where we use the Symfony framework as a vehicle to explore various types of testing without really diving too deep into edge cases or framework specifics (and still, making sure we have a running, competent test suite at the end), while leaning more into the concepts and design decissions behind them.

So we're going to talk about automated testing, which in its own right is a very important part of the bigger discipline of software testing; and a topic that, as a developer (and as such, responsible for implementing this type of tests), I'm passionate about.

Let's get started.

## What we're going to be talking about

For web applications, as far as automated tests go, there are three categories which I think are essential to have and complement each other very well:

- Unit tests: This is the most low level and, in my opinion, the most important type of developer tests. Unit tests don't only make sure that the system does what it is supposed to do, but also that it is correctly factored, where individual components are decoupled. They need to be that way because unit tests focus on exercizing specific classes and methods running in complete isolation, which becomes harder if the class you want to test is very tighly coupled with its dependencies/collaborators. These tests validate the behavior of basic programing constructs like classes and the algorithms within them.

- Integration tests: These tests go one level of abstraction higher when compared to unit tests. They test how the system interacts with external components. In this article, we're going to use integration level tests to validate functionality that has to do with interaction with a database and an external REST API. 

- Functional tests: These are the tests at the highest level of abstraction. These try to closely mimic the user experience of the system by interacting with it as a user would. In terms of a web application, this means making HTTP requests, clicking buttons, filling out and submitting forms, inspecting HTML results, etc.

If we can build an automated tests suite that provides good coverage, and exercizes the system at these three levels, I would feel very confident that it can work properly in production. An added bonus is that with tests like these, we would have a live documentation of the system, the features it provides and, to an extent, how it works.

Virtually all serious software development ecosystems have at least one automated testing framewoek or library which we can leverage to write our tests. For our purposes in this article, we're going to be using the Symfony PHP framework which integrates beatifully with PHPUnit to provide developers with an effective, and even fun way to write tests.

## Getting to know the System Under Test

In order to help illustrate the topic by showing practical examples, I've prepared a simple weather app. The app is very straigt forward. It only offers one feature: it will allow the user to see the current weather of a given city in the US. It does this by presenting a form where people can type in a city and state, submit it, and get their information back.

The app obtains this information by contacting the OpenWeatherMap Web API. It also stores all queries in a database for posterity.

The site is a typical Symfony web app. It uses the MVC pattern and Domain Driven Design concepts like entities, repositories and services. Here's a diagram explaining the static structure of the app:

STATIC DIAGRAM HERE

The front end, as you'll see, is super simple. Not really any client side JavaScript logic to speak of (stay tuned for another blog post about unit testing JavaScript front ends!). So this is more of an old-school, backend only app. Good enough for what we're trying to do here though.

So our only use case is the current wearther request. We do have, however, a couple alternate scenarios within that use case. First, if the user types in an invalid US state code, the app will show a validation error. Second, if the user inputs a city that does not exist (or, more specifically, one that the OpenWeatherMap Web API can't find), the app will show another error message.

To get a better idea of how the classes interact with each other, here's an sequence diagram detailing how the app serves the main weather query scenario:

SEQUENCE DIAGRAM HERE

As you can see, the controller receives the request and calls upon the service class to validate the input and retrieve the information for the city specified by the user. Then, the service takes care of orchestrating the domain model objects like entities, repositories and other services in order to fulfill the request and return back the weather information that eventually gets rendered with the template.

You can explore the source code for our demo app here: LINK TO SOURCE CODE HERE. The interesting files are under the `src` and `template` directories. contents should be self explanatory: `src/Controller` contains our controller, `src/Service` contain the service classes, and so on.

If you want to run it, you can do so by:

1. Cloning the git repo with `git clone REPOSITORYURL`.
2. Install dependencies with `composer install`.
3. Initialize the database with `bin/console doctrine:schema:create`.
4. Fire up the application with `composer serve`.
5. Go to `localhost:3000`.

You should now be able to see something like this:

SCREENSHOT OF APP HERE

<!-- There's a slight mental mapping that we need to do when we talk about our three-tier testing conceptual model and Symfony's. In the Symfony world, they talk about two types of tests: unit tests and functional tests. That's the distiction that the frameworks makes implementation wise. In terms of our conceptual categorization that we did earlier, Symfony's "unit tests" are the same as the "unit tests" that we described. Our other two catergories: integration and functional, fall into the "functional" type of Symfony tests. We'll see how that pans out shortly. -->
