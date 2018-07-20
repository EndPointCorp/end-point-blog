---
author: Ethan Rowe
gh_issue_number: 321
tags: testing
title: Getting Started with Unit Testing
---



So, you’re not writing tests.

And it’s not like you don’t want to, or think they’re a bad idea. It just seems so hard to get started. The hurdles to clear feel like such an impediment. It Just Couldn’t Possibly Be Productive To Start Testing Right Now, Not When My Really Important Project Needs to Get Finished in a Timely Manner.

Maybe you’re working on a legacy project, on an application built on an old framework that isn’t particularly friendly towards unit testing. To get testing, you’ll need to wrestle with so many things, it just doesn’t make sense to even try, right?

After a few years of using test-driven development (TDD) pretty consistently, I’m convinced that unit testing can and should be a more widespread practice. More importantly, after learning a lot of lessons over those few years, I think it’s well within any dedicated individual’s grasp. Care to hear about it? (Don’t answer that.)

<a href="/blog/2010/06/23/getting-started-with-unit-testing/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5486027089737016530" src="/blog/2010/06/23/getting-started-with-unit-testing/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 320px; height: 62px;"/></a>

## Digression the First: Why You Should Write Tests, In Case You Require Convincing (and if you’re not writing them, then you clearly require convincing)

The code you write is for something, and that something is for *somebody*. Somebody cares that the stuff you wrote does what it’s supposed to.

It follows that when you implement stuff, you tell the relevant Somebody about it. You tell them “hey, this is ready.” Or “hey, this is finished; check it out.”

Are you a liar?

Well, is it really ready, or isn’t it?

How do you *know* it’s ready? How can you claim that it works, that it’s worth Somebody’s time to check out or pay for or otherwise revel in?

Oh... you *tested* your work. I see. How did you test it?

Wait, you what? You went into a REPL client for your language of choice and called a bunch of functions? And you visually verified their results?

That sounds like a little bit of programming followed by a little manual inspection. As if you knew what results to look for given a particular set of inputs. Right?

So, wouldn’t it be nearly as simple to have put that little check into a script, called it a test, and then been able to re-run that test at any time in the future?

Oh... I see. This is only part of what you needed to do. The other stuff is really high-level, you have to submit some stuff in a form and be sure that the data you get back looks right. So you tested through a browser. So, you feel like you can’t write a test for that because you don’t want to go set up Selenium or whatever and deal with the unpleasant prospect of testing actual HTTP/HTML applications?

Well, wait a sec... even if you have a form submission and some data to inspect, you still know how the data you should get back should be *structured* for a given set of inputs, right? Couldn’t you write a test script for that piece, and at least have the foundational data layer stuff covered?

Oh..., so this is all in one big long hairy unmaintainable hacky script and the logic isn’t split out that way. I see.

Wait... aren’t you changing said script to do this work? Aren’t you already in there making changes? You are? Well, aren’t you—​as a sentient, sane human being capable of rational thought—​fully empowered to refactor pieces of this code, since you’re already changing it?

Right, you could refactor things instead of maintaining the status quo. So, couldn’t you, say, move the data processing piece into a function and test the inputs and outputs of that function? Or better yet, move the data stuff into a separate module specific to data abstraction for the relevant portion of your system, and test that module?

I understand that it isn’t perfect, that it’s not capturing the full stack of concerns, but it’s capturing the core behaviors of what you’re doing, right?

Isn’t that possible and in fact not particularly hard?

Doesn’t that really not impose all that much additional time on what you’re already doing?

Wouldn’t it be better if you started doing that *right now* and slowed the relentless accumulation of technical debt?

So, wait... why aren’t you writing tests?

## All Software Engineers are Liars, But Tests Make You Less of One

<a href="/blog/2010/06/23/getting-started-with-unit-testing/image-1-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="You lie!" border="0" id="BLOGGER_PHOTO_ID_5486028712806750242" src="/blog/2010/06/23/getting-started-with-unit-testing/image-1.jpeg" style="float:right; margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 268px; height: 320px;"/></a>

Every software engineer will claim that something works and find that it doesn’t work for the Relevant Somebody. Thus, every engineer will lie in making the claim that something is “done”.

At least if you’re writing tests as you go, addressing some subset of the core of your work, you can speak with greater confidence about what works and what doesn’t. You will still be wrong. You will write imperfect tests. You won’t be able to cover everything. You will miss certain corner cases.

You will still lie. But you’ll lie less often, with less profundity.

## Getting Started: It is the Biggest Challenge

The single biggest obstacle to getting going with unit tests is... getting going with unit tests.

Seriously. I don’t think I’ve encountered any other area of software engineering that suffers as much as testing from inertia and excuse-mongering and whatever else. Something about it invites people to let any inconvenience or potential hurdle balloon into a solution-killing problem.

While certain aspects of unit testing undoubtedly pose significant challenges and, occasionally, do not present any particularly clean way out, for any given programming problem there is likely at least *some* aspect that can be productively tested with a minimum of fuss.

So, at a minimum, start there. In a festering code-pile with no obvious place to gain a testing foothold, there will still be such places: simple pieces of functionality in which the outputs are purely dependent upon the inputs and the logic in between, with no side effects, no external dependencies.

Some principles to start your testing life with:

1. The right thing to start on is whatever you’re working on *right now*. Do it. Now.
 
1. To get moving, find some aspect of your code that is simple, self-contained, with clear expectations for inputs and outputs. Test that stuff. It’s the easiest to test.
 
1. Adapt your design and coding style to maximize the places that are simple, and self-contained, with clear expectations for inputs and outputs. This will maximize the testability of your code. It will also very possibly improve the organization of your code, as well.
 
1. Don’t worry about perfection and worry instead about getting some meaningful tests. If you’re just started testing, the first tests you write are probably going to be pretty weak anyway. Just saying. That’s how it is. Learning takes time. That’s what change looks like.
 
1. The language you’re using almost certainly has some basic, common, standard testing framework. In Perl you’ve got Test::More. In Ruby you’ve got Test::Unit. In Python you’ve got the unittest module. Etc. They’re not hard to learn, and you don’t need to learn the whole thing to get started. Just write a script that pulls this stuff in and uses the basic assertions. Don’t write a custom test script that doesn’t build on something standard, because you’ll be reducing productivity and missing out.
 
1. Test the interface, not the implementation. This is something that can take some acclimation, depending on your mindset. The purpose of the test is to show that the subject adheres to its contract: given input A, you get output A’. Under *foo* conditions, your widget tastes green. And so on. The purpose is almost certainly not to show that the subject implements something in a particular manner.
 
1. Start small. Start with something that has very clear expectations and a modest interface (one or two arguments, for instance, as opposed to arbitrarily complex arguments of nested data structures).
 
1. Things that depend on shared/global state are messier to test. So are things that depend on side-effects (a database call, for instance, where you’re less interested in the return value for a given set of interests and more interested in what happens in an external service as a side-effect of your call). Unless your framework gives you ways to deal with them in a testing situation (like Rails does with the database, for instance), maybe you don’t want to start your first set of tests dealing with such stuff.
 
1. Adapt your design and coding style to avoid reliance on shared/global state or side-effects. If such things are key to what you’re doing, then design so the global state or side-effects are accessed through an interface you control. We’ll get more into this subject in a subsequent posting. 
 
1. Remember that it isn’t that hard: if you can clearly, definitively express the expected behavior in prose or speech, then you can express it in code.
 
1. Remember that if it’s hard, you’re probably designing it poorly: if you find that you cannot express the expected behavior clearly, then you need to step back and reconsider the design.
 

This article will be the first in a series over the next few days. Next time, I’ll look at some concrete examples.


