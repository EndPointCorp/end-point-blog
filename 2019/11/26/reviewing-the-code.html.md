---
title: "Reviewing the Code"
author: Kürşat Kutlu Aydemir
tags: development
gh_issue: 1573
---

![Magnifying glass](/blog/2019/11/26/reviewing-the-code/review_magnifier.png)

<!-- Photo from https://pixabay.com/illustrations/magnifying-glass-search-to-find-1019982/ -->

Code review is analysis of source code of a software project by reading the code itself or sometimes using automated tools to analyze it, and it is part of the Software Quality Assurance (SQA) activities which define the quality assurance of the whole software development lifecycle. As we go through the flow of a code-review, we’ll understand what to assure by doing code review. Code review lifecycle covers the guidelines and the code review process itself.

### Code review guidelines

#### Preparing for code review

- Pick the right reviewers. The reviewer should be an experienced software architect. Sometimes, less experienced groups can join the review team. Communication is also important, since frequent round table code review meetings with the developers are not usually productive.
- Let authors annotate the code before review indicating which files have precedence for review. Annotation by the developers to orient the reviewer so they know where changes have taken place and where to review is a good practice.
- Request code review. Requesting code review just before testing is another good practice.

#### Tips for reviewer during the code review
- Review small pieces of code at a time, for instance around 400 lines of code.
- Review for around 60 minutes at a time.
- Set goals and metrics.
- Use [SMART criteria](https://en.wikipedia.org/wiki/SMART_criteria):

>- Specific: target one area clearly and precisely.
>- Measurable: quantify progress toward success by using metrics.
>- Actionable: ready to start and possible to accomplish.
>- Relevant: connected to what’s being done, considered, and/or resourced.
>- Timely: occurring at a favorable or useful time and opportune.

- Measure inspection rate and defect rate.
- Use checklists.


### Code review flow

Regardless of what programming language is used to develop, code review should cover the following common areas:

- Maintainability
- Reusability
- Performance
- Security
- Bug analysis
- Knowledge sharing

Other practices can also be reviewed, like extensibility or OOP (Object Oriented Programming) software design patterns. These depend on possible future plans and the nature of the software being developed.

### An Example Checklist for Java projects

I’d like to share a checklist below that I used for a project recently. I didn’t add my comments on the checklist items. The comments should be added to each item and if there are important details in the code, they should be added in the detailed report indicating the code blocks with the comments.

#### Clean Code & General

- Use solution-problem domain names
- Classes should be small
- Functions should be small
- Do one thing
- Don’t repeat yourself (avoid duplication)—reusability
- Explain yourself in your code
- Use exceptions rather than return codes, nulls
- Configurable

#### Security

- Minimize the accessibility of classes and members
- Avoid excessive logs for unusual behavior
- Release resources (streams, connections, etc) in all cases
- Validate inputs
- Validate outputs
- Make public static fields final
- Authorize and authenticate

#### Performance

- Avoid excessive synchronization
- Keep synchronized sections small
- String concatenation
- Avoid creating unnecessary objects

#### Extensibility

- Make it easy to add enhancements with minimum changes
- Components should easily be replaceable

#### Scalability

- Consider large user base and data
- Can be deployed in distributed systems

#### A few possible checklist item comments:

- For naming checklist items, the below code piece complies with the conventions as it uses the solution domains as packaging name.

```package com.google.search.common;```

- On the other hand, the following line would violate the Java package naming conventions since its letter capitalizations and domain usage are inconsistent.

```package COM.google_search.common;```

- Sometimes a very long line of code could be used which usually violates the readability standards.

- Or sometimes a variable used in a class scope in a concurrently run singleton Java object violates thread safety and could be a security issue.

### Static Code Analysis

Reviewing is viewing the software by reviewer and the reviewers’ own comments and best practice notes will be used as the final output. There are also static code analysis tools like PMD for Java which generally checks the code for bugs and clean code. This static code analysis, usually attached to the final code review report of the reviewer, usually is only helpful for a detailed overview for the clean code. Sometimes software development IDEs also provide best practices while writing the code. I like the PyCharm IDE’s smart clean code suggestions for Python, for example.

### Automated Code Review

Automated testing is subject to measurable reports and static code analysis. Static code analysis tools can be scheduled for code checking and reporting. Testing the code as a preparation for code review is another process that can be automated and already part of the SDLC processes. Some overlooked issues, like releasing resources and concurrency issues, can be also checked by automated tests and can be reported as automated code review results.

### Conclusion

I have tried to outline the general code review cycle of a project. Depending on the programming language and the architecture of the software to be developed there can be additional best practices like functional, non-functional, OOP design principles, etc. Reviewers may extend or lessen their checklist items according to future plans, architecture or review request coverage.
