---
author: Kamil Ciemniewski
gh_issue_number: 992
tags: elixir, erlang, functional-programming, haskell, ruby
title: "Elixir — a step in a never ending journey"
---

Every now and then a new programming language is born. In fact, since the not-so-distant introduction of early programming languages, we’ve got about 693 of them! (at least that’s what [Wikipedia](http://en.wikipedia.org/wiki/List_of_programming_languages) says).

Why can’t we settle for just one or at least just a handful? Creating a new programming language certainly isn’t the easiest task on earth. It’s one thing to have fun with syntax lexers, but completely different to provide all the tooling and libraries. In fact programming languages authors are being held hostage to their own creations. There’s always a multitude of things to do, which makes leading such a project basically a full-time job.

Why are those languages sprouting all the time then? The answer is simple: out of necessity.

### Pitfalls of computer programming

Most of today’s mainstream programmers choose object-oriented programming as their paradigm of choice. It solves the problems of procedural programming… we could say: in a classy way. You can find its advocates everywhere. In fact you don’t even need to search — they will yell at you from just about every corner of the Internet.

Truth be told it’s one of the things that makes producing new software possible. Some of today’s projects wouldn’t even be possible to create with procedural programming for the same cost. The tax of complex architecture would simply be too high. It’s especially true for commercial products when time and budget play a crucial role.

It’s equally true that this approach produces its own set of traps to fall into. Even though you’ve got a plethora of design patterns at your disposal ([http://www.oodesign.com/](http://www.oodesign.com/)) you will still fall into one of them.

The reason is that the whole concept is by its nature very bug-potent. There are a couple of things that gets us into trouble. One is the inability to quickly and clearly reason about the flow of programs. In object-oriented world the flow of a higher level action may be covered by a large nest of several objects' class definitions. In every class definition the result and all effects of methods may affect the results and effects of many other methods in different objects. Even at the level of one class the result and effects of a method call depends on the state of this object. This covers processes with a fog that cannot be cleared even after hours of testing and debugging. We have to pay the mental energy tax just because we're using the most widely applauded technology.

### Hello?… Real world here… You are a business!

In a computer programmer’s paradise there are no deadlines. There aren’t any troublemaking users either. You could just spend 10 years developing something you believe in, then get a Nobel Prize for how awesome it is and then shut the whole thing off before you break anything. You could make the code as clear as you like. Your programming heroes could stare at you from pictures of their books with a sense of amazement. All design patterns used. The code written in the Right Way.

There’s a newsflash for you though: you are a business! Even if you just work for a business you still have deadlines, no? You still have to deal with users and investors. And your realistic estimations almost never sound reasonable. Welcome to the real world.

Almost everything you do has a price tag. Time rules software projects — in fact there is no such thing as free time. But it’s not only about time — silly bugs can have profound impact on the perception of businesses. Will users go back to a web shop again after seeing a HTTP 500 error when trying to check out?

At the end of the day all we do is business. That makes certain features more important than others when it comes to choosing technologies. As far as my understanding goes the three of the most important factors are:

- time-to-market
- maintainability
- difficulty of shooting yourself in the foot

When I was learning Haskell a while ago I was mostly concerned about this third factor. Everyone knows how easy it is to shoot yourself in the foot with a dynamically typed programming language. At the same time having a very strict type system makes productivity drop like a rock. Haskell seemed to have a great solution to this dilemma. Being a functional language, it allows you to narrow or widen the range of types a function can operate on. It’s polymorphism Done Right. It doesn’t restrict functions to operate just on a certain branch of types like OOP languages make them. With type classes, you can also make them extensible in the future. I won’t give any examples - you can look them up in the Internet if you want. The message is simple: Haskell makes you productive **and** it makes your results correct at the same time.

All this holds true as with simple code. In real world, you’ll have lots of app specific type classes and lots of type aliases not to get crazy from reading function signatures. Also, the learning curve is pretty dramatic - for simple cases, it is sufficient to use [Monads](https://www.youtube.com/watch?v=ZhuHCtR3xq8&feature=kp). From all category theory, knowing Monads and Functors is all one needs to write very simple programs in Haskell. But when you need to create something more complex, you need to have a good understanding of the rest and spend a lot of the time on planning out the right architecture.

Looking at what it takes to achieve similar results, using [Yesod](http://www.yesodweb.com/) — Haskell’s most popular web framework as one can achieve in Rails — the time-to-market factor is ridiculously high. And what innovation that is if we get worse results? It is true that once your Haskell code is compiled — it’s very probable that it is in fact bug free. And you cannot say the same thing about any Ruby code even with thousands of lines of unit tests.

### Getting the competitive edge

About two years ago a new programming language was born. As it usually goes — it didn’t introduce any new paradigm. In fact it was built around ideas known from languages that have been around for almost 30 years now.

[Elixir](http://elixir-lang.org/) is a programming language built for the Erlang virtual machine. Its compiler produces exactly the same binaries that come from Erlang’s compiler. The two languages are very alike and libraries developed in one of them can easily be used in another. However, Elixir adds a couple of niceties that Erlang doesn’t have. It also features a nice and clean syntax that many Ruby programmers can immediately **get**.

Above all it enhances a developer’s toolbox with tools for increasing all three aspects of a good business technology. Being created by one of the most known Open Source contributor in the Rails world - Jose Valim, includes a great set of features, making Rails developers feel almost "at home". Because it is a functional language though, it reduces the number of potential bug kinds significantly. Its polymorphism model isn’t based on type classes, but on easy to grasp protocols. Thanks to philosophy inherited from Erlang, maintainability is at its heights.

Superficially, one might think of Elixir as of some kind of a marriage between Ruby and Haskell. Ruby being a very dynamic language — enhances developer’s productivity in many ways. Its syntax allows creation of custom DSLs that in turn boosts productivity even more. Haskell as a functional language makes the test &amp; fix part of projects **significantly** shorter. As with other functional languages — the resulting code tends to be very terse and easy to grasp just from looking at. In fact, there are some libraries which aren’t that well documented — but it’s not that hard to **get** what they do just from quickly skimming the code.

Elixir shares these benefits, but it takes developer’s productivity to the next level by introducing Lisp style macros. It also shares the same base infrastructure libraries that Erlang has, making it an amazing fit for developing highly available solutions. It is known that Erlang based solutions tend to have an insanely high rate of reliability. Joe Armstrong, an author of the Erlang language once said:

> *The AXD301 has achieved a NINE nines reliability (yes, you read that right, 99.9999999%). Let’s put this in context: 5 nines is reckoned to be good (5.2 minutes of downtime/year). 7 nines almost unachievable ... but we did 9.
>
>
>
> Why is this? No shared state, plus a sophisticated error recovery model.*

You can achieve the same with Elixir. Because it runs on the same virtual machine, it features the same hot code reloading ability. This means that you don’t have to shut off your application just to introduce some quick patches or enhancements. Thanks to the famous OTP library you can use so called supervisors too. They define strategies for dealing with failures — e.g automatically restarting a part of the app that has just crashed. It’s very inexpensive as in Erlang and Elixir, parts of applications are built around very lightweight processes. Processes do not share any memory with one another, making them very loosely coupled. They communicate with each other through so-called messages. They don’t need to know if a receiver process lives on the same machine or on some other in the network. All this makes writing highly scalable solutions a cinch.

### There’s no one right answer, but there will never be

This post is meant as an outline of a small part of what’s available outside of **The Mainstream**. Even though many ideas presented here were known to the programming world for long years, they never really get through to what is considered mainstream. I think we can be more ambitious than that. Collectively as developers we can do much better than how we’re doing now. And because of that I’m so excited about any project that tries to address real programming issues from a much deeper perspective than just a couple of syntax sugar niceties. It’s nice to have pleasant looking code, but it’s even nicer to have pleasing looking end results. I don’t think Elixir is the answer to all our troubles but at least it’s seems to steer in the right direction.

You can find its specifics, syntax, features, tutorials on its website: [http://elixir-lang.org/](http://elixir-lang.org/)
