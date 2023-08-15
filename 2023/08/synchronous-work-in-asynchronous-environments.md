---
author: "Vincent Martin"
title: "Synchronous work in asynchronous work environments"
github_issue_number: 0
date: 2023-08-15
tags:
- remote-work
- tips
- vscode
---

<!-- TODO photo -->

(Co-authored by [Trevor Slocum](/team/trevor-slocum/).)

As a team that spans the globe, asynchronous communication is a necessity for
us. While we do use email, of course, we use internal text chat rooms for
communication more frequently. These asynchronous tools are useful to have
around, but they may not be the best fit for sharing an idea or some other
information with others. Sometimes we need to speak with someone in a voice or
video conference, or even share our screen and work together to solve a problem.
In this article we will share some of the things we have learned while working
in these situations.

### Solving problems together

When pair programming, we solve problems together. This usually takes the form
of one person sharing their screen, while the other watches and provides
guidance and feedback, but it also takes other forms which we will refer to
later. Having someone critique our work in real-time as we try to solve complex
problems can be stressful. This is an entirely natural reaction to the situation,
and happens to everyone who engages in pair programming and other collaborative work.

If you find yourself feeling this way, our advice is to take a brief pause and
talk it out with your co-worker. Taking a few minutes to clear your head and
get your feelings off of your chest is really all it takes. In the moment, it
can be hard to see that our teammate is just trying to help us. Once we have
shared how we are feeling, we already start to see and understand the situation
more clearly.

Another important point is that working together is inherently a teaching and
learning activity. Because we were not extruded from a cloning machine, we all
have different ideas and perspectives. By virtue of interacting with each other,
particularly on anything which one can acquire a level of understanding and
proficiency, we share things that we have picked up along the way, and pick up
things that others share along the way.

Pair programming at its best is two friendly engineers enjoying the challenge
of building something or solving a problem together while expanding their
individual understandings of the problem domain and building trust as a team.
Everyone benefits, so try to relax and have fun!

### Technical Aspects

With all the mental aspects of pair programming addressed, you can now get to
programming with your co-worker. While a software developer may share their
screen, as mentioned previously, it's also possible to share an entire
development environment. This allows your teammate to see and edit the entire
repository of source code in real-time, from the comfort of their own editor
running on their computer. These shared environments allow you to follow each
other's cursor and also see what each person has highlighted, or work
independently in different files. This approach also has the advantage of not
relying on video compression to share code.

![A screenshot demonstrating the initial step of sharing with others using VSCode.](/blog/2023/08/synchronous-work-in-asynchronous-environments/vscode.png)<br>
Using the VSCode Live Share plugin

VSCode offers a plugin called "Live Share" which can be installed to allow the
users to collaborate in real time on a project. The project itself lives on
one of the users' computer, for example if you wanted to pair a program with a
friend, you would initiate the session on your computer and send your friend
the provided web link, which they would use to attach to your session. This
feature not only allows you to share your code, but also allows you to share
useful tools like the in-editor debugger. [This page](https://code.visualstudio.com/learn/collaboration/live-share)
provides information to help you get started with VSCode's Live Share plugin.

![A screenshot demonstrating the initial step of sharing with others using IntelliJ IDEA.](/blog/2023/08/synchronous-work-in-asynchronous-environments/intellij.png)<br>
Using the IntelliJ Code With Me plugin

The IntelliJ family of editors (e.g. IDEA) offer a similar plugin called "Code
With Me." This plugin provides additional features such as allowing more than
two users to connect at the same time. Actual live editing of code is limited
to five users at the moment, however, you can have more if you operate in a
"Teacher-Student" scenario where you can present code real time with a large
number of your teammates by enabling "force others to follow you mode."
[This page](https://www.jetbrains.com/help/idea/code-with-me.html) provides
information to help you get started with IntelliJ's Code With Me plugin.

### The flow

Pair programming can be quite effective, but the social aspect can cause
participants to burn out pretty quick. It can sometimes be hard to focus and
socialize for hours at a time. Because of this we have found it quite
important to take breaks. The question is, when do you take these breaks?

Breaking apart and coming back together later is another workflow that we have
had a lot of success with. A scenario which demonstrates this is the following;
Imagine you and your co-worker are working on a task, you both come to a problem
which neither of you knows how to solve, finding the solution will require a bit
of research, reading and trial and error. A few solutions will have to be tried!

Oftentimes this is a good hint to both of you that you should take a break from
the problem and work on it independently, bringing all of your findings together
at a later time. This essentially breaks up the serial nature of pair programming
and makes it parallel. In other words, pair programming is not always done together.

### Wrapping it up

Once you are finished working on a problem together, it's time to commit the work.
If you're using [git](https://git-scm.com), only one author will be attributed by
default (whoever runs the command `git commit`). This means that if/when we find
a bug in this code later, and need to identify who authored the code responsible
for it to explain why the code was written this way, we might only see half of
the picture (or worse).

Adding a co-authored-by line (such as the one below) at the end of a git commit
message is the de-facto standard for attributing multiple authors to a git commit.
This is not officially supported by git, but many third-party git tools recognize
this line, such as GitHub and GitLab, and this practice is followed by many programmers.

```
Co-authored-by: Chuck Person <chuck@eccojams.opn>
```

Even when a git tool does not recognize this line, other tools such as `grep`
can be used to extract this information.

Note that you must add a blank line before adding any `Co-authored-by` lines. For example:

```
Add fizz, fix buzz

We need to include fizz in order for buzz to function properly.

Co-authored-by: Chuck Person <chuck@eccojams.opn>
Co-authored-by: Ramona Langley <ramona@floralshoppe.mpl>
```

Happy coding!
