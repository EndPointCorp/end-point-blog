---
author: "Kevin Campusano"
title: "Code Reviews"
tags:
- software engineering
- software quality
- code reviews
---

# Code Reviews

Last week, a few End Point team members and I came together to prepare a presentation on code reviews for the whole company. We went through the basics of "what", "why" and "how". We also, and perhaps most interestingly, went over several recommendations that we've discovered after years of doing code reviews in a variety of teams and project scales. A series of "lessons learned" so to speak.

I thought it'd be useful to capture that discussion in written form. Let's start with the basics.

# What is a code review?

[Wikipedia's article on code reviews](https://en.wikipedia.org/wiki/code_review
) says that a code review is...

> A **software quality assurance** activity in which **one or several people** check a program mainly by viewing and **reading parts of its source code**, and they do so **after implementation** or as an interruption of implementation.

Which is frankly a lot of words to say "having somebody look at the code you've written". This definition however, touches on a few aspects that give us good insight into what code reviews are and what their purpose is.

First up, it tells us that code reviews are a software quality assurance activity. That is, their main goal is to make sure that the code that's being produced is good quality.

Second, it tells us that they are carried out by one or several people. Revealing to us that code reviews are a team exercise. It's the opposite of coding in isolation. Coding becomes a communal task, with input from other team members.

It also tells us, maybe unsurprisingly, that the main focus of the review is the code itself. As the main deliverable artifact of the software development process, we should strive to make it as good as possible.

Finally, it tells us when code reviews should happen: when implementation is done, or there's a logical interruption of it. Meaning, once a feature is done, a user story is complete, a bug fixed. I.e. when there's a cohesive chunk of code that has been written.

# Why should we do code reviews?

So why are code reviews important? The answer is that they provide many benefits.

First and foremost, code reviews can help improve the code's internal quality. Productive discussion around an implementation can help improve maintainability and readability of the code when reviewers, with a fresh set of eyes, spot the potential for such improvements where the original author may have missed them.

Also, and just as important, external quality of the code can be improved. Reviewers can help find bugs or other types of defects like security and performance issues.

Code reviews can also serve as a knowledge sharing tool. Code written by team members of more seniority or who are more knowledgeable about the code area, domain or a specify tool or library, can be exemplary for other team members. They can learn about these when conducting reviews. This has the added perk that it reduces the situations where a single person holds the knowledge of a given system component or code area. Likewise, code review feedback provided by such expert can have the same effect.

Another great benefit they can bring to the table is the distribution of code ownership among all of the team members, not only the author of the code in question. When projects have strong code review habits, the code becomes something that the whole team is producing, as every line that gets to production has been seen by, and incorporated input from, many of the members of the team. Everybody owns and can feel pride about the final product.

Finally, reviewers can sometimes just come up with better and/or simpler solutions than the ones the original author implemented. They can come up with these given their fresh perspective and maybe their experience with similar problems in other domains. Code reviews allow for these to be incorporated before the time comes to ship the code.

# What should reviewers look for?

Simply put, reviewers should look at every aspect of the code and offer suggestions for improvements where they see fit. [Google's recommended practices](https://google.github.io/eng-practices/review/#look_for) compile a somewhat comprehensive list of the elements that reviewers should look for:

- Design: Is the code well-designed and appropriate for the system?
- Functionality: Does the code implement the requirements correctly?
- Complexity: Could the code be made simpler? Is it understandable?
- Tests: Does the code have correct and well-designed automated tests?
- Naming: Are clear names for variables, classes, methods, etc. being used?
- Comments: Are the comments clear, useful and necessary?
- Style: Does the code follow the project’s style guide?
- Documentation: Did the relevant documentation also get updated? Any public interface documentation or OpenAPI files for example.

When it comes to code style, something to note is that this is where tools like linters are prettiers can be implemented to great effect. Early in the project, if the team decides on the style, such a tool can be setup to automate the process of making sure that all code that gets written complies with the style guide. Some code repositories even allow for such tools to be automatically run upon every push. This makes style guide compliance not even a concern for the reviewers, because the tooling always makes sure that the code does comply.

# Who should be reviewing code, and asking for their code to be reviewed?

Everybody in the team should be regularly reviewing code and having their code reviewed. Regardless of seniority or experience in the specific project area, domain, framework or language. More "junior" team members benefit from reviewing code by learning new techniques, principles, technologies, and the code base itself. More "senior" team members can provide valuable input that improves the code base and other team members' skills.

We also have to realize that the distinction between "junior" and "senior" can often be flexible and blurry. Most teams have people with a variety of skill sets and experience; so everybody has the ability to offer good insight. One can always be a "senior" in one aspect of the project, and a "junior" in another.

Even if a single reviewer can be good enough, it is beneficial to include as many reviewers as possible. Lest we fall into the trap of overloading a small number of individuals by having them be in charge of most or all of the reviews. Also, like I mentioned before, two great benefits that code reviews offer are knowledge sharing and code ownership. The more people you have regularly reviewing code, the bigger they impact will they have in these two aspects.

That said, it is always better to have somebody more experienced in the area of the code that's changing be among the reviewers.

# When should code be reviewed?

As Wikipedia's definition revealed, it is ideal for code reviews to be done when implementation is done on a feature; before merging the new code into the main development branch. Most modern software development that uses a git based code repository (like [GitHub](https://github.com/) or [GitLab](https://about.gitlab.com/)), uses the [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) mechanism. The developer creates a Pull Request when they are done implementing a feature or fixing a bug. The PR compiles all the changes (a series of commits) and turns them into a nice digestible package. This adds great visibility to the changes and makes them very easy to review before merging. Ideally, no patch makes it into the system without first being reviewed.

> GitLab uses Merge Request instead of Pull Request. Same concept, different terminology.

Code reviews can also happen before the implementation is strictly done. Maybe the developer wants to get the team's input on a specific function, method, class, component or approach. If the developer asks for it specifically, it can always happen at any point in their development process.

Something to note is that [pair programming](https://en.wikipedia.org/wiki/Pair_programming) can expedite the review process. Pair programming is essentially closing the code review feedback loop, compressing it to its fastest form. In pair programming, code effectively gets reviewed as soon as it is written, bit by bit. If the team has more than two developers though, there's still great value in having the other team members, the ones not involved in the pair programming activity, review the code.

# Some recommendations

Now that we've gone over the basics, let's discuss some of the recommendations and pitfalls to avoid, inspired by our experience in conducting code reviews over the years.

## Try to keep pull requests in a manageable size

Bigger patches make code reviews harder to perform because of the sheer volume of code that the reviewers need to parse through. This makes it so the reviews are less useful also, as the size deters reviewers from really gaining a thorough understanding of the changes which prevents them from being able to offer good insight.

So we feel like it is best to keep them as small as possible. This desire to keep things small may need to affect the overall software development process upstream. For example, making sure user stories/change requests are granular enough so that they can be fulfilled with a reasonable amount of code changes. Consider splitting bigger features into smaller, bite sized issues to make this possible.

## Make sure the pull request is cohesive

PRs are better when their size is manageable, but also we need to make sure that they contain all they need to allow the reviewers to understand them completely and as a whole. There's no need to split the changes artificially (for example, between back end and front end) if ultimately, they need to be pushed together to fulfill the requirement that's being worked on, and leave the system in a working state.

## If you would like a preliminary review, ask specific questions

Sometimes we want to get early reviews even before the implementation is complete or we're at a logical interruption point. For such cases, a good practice is to come to the reviewers with a specific question that we'd like them to focus on.

Sometimes it can lead to waste of time if the intent of the review is not explicitly communicated. Without this context, when given a set of incomplete changes, the reviewer could mistakenly do a thorough review on code that's not yet ready and not even address the specific aspects that the developer is asking for help with.

The reviewer then ends up leaving a lot of feedback on aspects of the code that are not really ready for review yet. The developer may already intend to continue iterating on such areas, maybe even in the same direction that the reviewer's comments suggest. This situation renders a lot the feedback unnecessary.

## Pair programming has code reviews baked in

If the development team is small, and works closely together by the means of pair programming, we should remember that the activity of pair programming includes code review as soon as the code is being written. Code that's written by a pair of developers, can be considered already reviewed.

If there are other team members, it is always useful to have them look at the code as well.

## Code reviews work well asynchronously

So we should not try to force it into a synchronous process. Publicly available cloud-hosted git repositories like GitHub and GitLab include great tools for reviewing pull/merge requests. We should use them to their full potential. There's no need for a conference call or an in person meeting where everybody blocks a chunk of time to dedicate it to reviewing a PR. Everybody can do it on their own at their convenience.

## Give code reviews high priority

That said, we have to make sure to give code review a high priority within our day to day tasks. It is counterproductive to let pull requests sit for a long time when a few minutes to an hour of our time can mean that a user story/ticket can move forward through the process. If you work by organizing your increments via sprints, remember that the goal is to complete the most stories as a team. Reviewing a pull request is actively supporting that goal, even if it isn't one of the stories/issues you're particularly working on.

## Make sure your PRs get the attention they need

We should never just "fire and forget" a pull request. If it so happens that any of our patches are taking too long to be seen by other people, we don't just abandon them and think that they are somebody else's problem now, that our work is done. In these cases we should feel free to reach out to the reviewers and bring the PRs to their attention.

To this end, we should leverage all the communication tools available, even outside of the code repository or code review tool. Meaning chat, phone, issue tracking system, etc.

## Get as many reviewers as you can

A single reviewer on a pull request can be enough. However, it is always beneficial to try and get as many eyes as possible into a change. It improves ownership and it allows for more effective knowledge sharing. It also has the potential for more improvements on the code base, as more people, with varying strengths look at the code and offer their feedback.

Also try to avoid having a single person be the gatekeeper of merges. Like I said, everybody can and should participate in the activity of code reviews. Sometimes having a gatekeeper this may be desirable if, for example, CI/CD is in place in such a way that merges produce automatic production deployments. But we can always try to make sure that code that reaches the gatekeeper is already reviewed by other team members by the time it does. That way we avoid overloading them and eliminate the potential bottleneck or single point of failure.

Publicly available git repositories like GitHub and GitLab provide settings that allows specifying which users can commit to certain branches. If a process like that is needed, it can be done with help of such tools while still having PRs that many team members can review and discuss.

## Don’t let the perfect be the enemy of the good

If the PR isn't "perfect" or not "as good as it could be", but it does not worsen the code base, and implements the changes competently, maybe there's no need to block it. Code reviews are important, but it also is important to try and maintain the momentum on delivery. So it is a good idea to consider that when reviewing. There often has to be a balancing act between deadlines, paying off and incurring in technical debt, and what is "good enough".

In the same train of thought, it is useful to clearly label code review comments. Specifying whether the reviewer considers each comment as a question, a simple nitpick, or an actually important change.

## Top-down imposition of process is often inconvenient

Code reviews don't need to include a ton of software process overhead. Regardless of your process style, it can be a very lightweight practice and done at the developers' discretion. It can be as simple as sending a diff file to a fellow developer and asking them for feedback. The tools available today make them very accessible and easy to do. As such, they can become very effective when the team itself manages and conducts them; as opposed to having it come to them as a hard requirement from management. Even a practice as beneficial as code reviews can be soured by a bad, overly strict, or dogmatic implementation.

# That's all for now

At the end of the day, the concept of code reviews is simple: To have somebody else look at our code, in hopes that what eventually makes it to production is as good quality as possible. In this article though, we've discussed many more aspects to clearly explain the promise of code reviews. We've given some details on how to conduct them, who are involved, and what benefits we can get from them. We also captured a series of recommendations that we have learned through experience.

If you're not into the habit yet, hopefully this article convinced you to give it a try!
