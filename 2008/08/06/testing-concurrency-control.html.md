---
author: Ethan Rowe
gh_issue_number: 38
tags: testing, perl
title: Testing Concurrency Control
---

When dealing with complex systems, unit testing sometimes poses a bigger implementation challenge than does the system itself.

For most of us working in the web application development space, we tend to deal with classic serial programming scenarios: everything happens in a certain order, within a single logical process, be it a Unix(-like) process or a thread. While testing serial programs/modules can certainly get tricky, particularly if the interface of your test target is especially rich or involves interaction with lots of other widgets, it at least does not involve multiple logical lines of execution. Once concurrency is brought into the mix, testing can become inordinately complex. If you want to test the independent units that will operate in parallel, you can of course test each in isolation and presumably have simple “standard” serial-minded tests that are limited to the basic behaviors of the independent units in question. If you need to test the interaction of these units when run in parallel, however, you will do well to expect Pain.

One simple pattern that has helped me a few times in the past:

- identify what it is that you need to verify
- in your test script, fork at the relevant time (assuming a Unix-like OS, which is what you’re using, isn’t it?)
- in the child process(es), perform the logic that ought to bring about the conditions you want to verify, then exit
- in the parent process, verify the conditions

A more concrete example: I designed a little agent containing the logic to navigate a simple RESTful interface for rebuilding certain resources. The agent would be invoked (thus invoking the relevant resource rebuild) in response to certain events. In order to keep demand on the server made by the agent throttled to a reasonable extent, I wanted some local concurrency control: the agent would not attempt to rebuild the same resource in parallel, meaning that while one agent requests a rebuild and subsequently waits for the rebuild to complete, a parallel agent request would potentially block. Furthermore, while one agent is rebuilding, any number of agents could potentially launch in parallel, all but one of which would immediately return having done nothing, with the remaining agent blocking on the completion of the original. Upon the original agent’s completion, the waiting agent issues its own rebuild. Therefore, on one machine running the agent (and we only ran the agent from one machine, conveniently), no more than one agent rebuild should ever occur at any given time. Furthermore, for any n agents launched at or around the same time for some n >= 2, the actual rebuild in question should happen exactly twice.

This is actually easier to test than it is to explain. An agent that performs the rebuild issues an HTTP request to a configurable URL (recall that the agent navigates a RESTful interface). So our test can create a temporary HTTP server, point the agent at it, and validate the number of requests received by the server. In pseudocode, it ends up being something like this:

- get a free port on the loopback interface from the operating system
- in a loop, have the test script fork n times for some n > 2
- in each child process, sleep for a second or two (to give the parent process time to complete its preparations), then instantiate the agent, pointed at the loopback interface and appropriate port, and invoke the agent. The child process should exit normally after the agent returns, or die if an exception occurs
- in the parent process, after all the forking is done, launch a local web server on loopback interface with the OS-provided port (I used HTTP::Server since I was doing all of this in Perl)
- as requests come in to that server, push them onto a stack
- deactivate the server after some modest period of time (longer than the interval the children slept for)
- reap the child processes and gather up their exit values
- the test passes if: the server received exactly two requests to the correct URL (which you check in the stack) and all n child processes exited normally

This example is hardly a common case, but it illustrates a way of approaching these kinds of scenarios that I’ve found helpful on several occasions.
