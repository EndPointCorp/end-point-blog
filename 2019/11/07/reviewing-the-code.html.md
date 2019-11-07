---
title: "Reviewing the Code"
author: Kursat Aydemir
tags: software, code, review, SDLC, SQA
---
![Magnifying glass](/2019/11/07/reviewing-the-code/review_magnifier.png)

Code review is analysis of source code of a software project by reading the code itself or sometimes using automated tools to analyze it, and it is part of the Software Quality Assurance (SQA) activities which defines the quality assurance of whole software development lifecycle.
As we’re going to list the flow of a code-review we’ll understand what to assure by doing code review. Code review lifecycle covers the guideline and the code review process itself.

### 1 – Code review guideline

#### Preparing for code review
- Pick the right reviewers
The right reviewer should be an experienced software architect and sometimes less experienced group can join the reviewer team. Communication is also important. Making frequent round table code review meetings with the developers is not productive.
- Let authors annotate the code before review to indicating which files have precedence for review
Annotation by the developers to the code files to orientate the reviewer to see where the changes has been going around and where to review is important, is a good practice.
- Request code review
Also, a request for code review from developers just before the testing is another good practice.

#### Tips for reviewer during the code review
- Review small pieces of code at a time, like around 400 lines of code.
- Review around 60 minutes at a time
- Set goals and metrics
  - Use SMART criteria
  - Measure inspection rate and defect rate
- Use checklists



### 2 – Code review flow

Regardless of what programming language is used to develop, code-review should cover reviewing the following common sections:
- Maintainability
- Reusability
- Performance
- Security
- Bug analysis
- Knowledge sharing
Optionally other best practices can be reviewed like extensibility or OOP software design patterns which depend on the possible future plans or the nature of the software being developed.

#### An Example Checklist for Java projects
I’d like to share a checklist below that I used for a project last time. I didn’t add my comments on this check list. The comments should be added to each item and if important details in the code they should be added in the detailed report indicating the code blocks with the comments.

##### Clean Code  & General
- Use  Solution-Problem Domain Names
- Classes should  be small
- Functions  should be small
- Do one Thing
- Don't Repeat  Yourself (Avoid Duplication) - Reusability
- Explain  yourself in code
- Use Exceptions  rather than Return codes, nulls
- Configurable

##### Security
- Minimize the  accessibility of classes and members
- Avoid  excessive logs for unusual behavior
- Release  resources (Streams, Connections, etc) in all cases
- Validate inputs
- Validate outputs
- Make public  static fields final
- Authorize and  authenticate

##### Performance
- Avoid  excessive synchronization
- Keep  Synchronized Sections Small
- String  concatenation
- Avoid creating  unnecessary objects

##### Extensibility
- Make it easy  to add enhancement with minimum changes
- Components  should easily be replacable

##### Scalability
- Consider large  user base and data
- Can be  deployed in distributed systems


###### A few possible checklist item comments:

- For naming checklist item, the below code piece complying to the conventions as it uses the solution domains as packaging name.

```package com.google.search.common;```

- On the other hand, the following line would violate the Java package naming conventions since its letter capitalizations and domain usage is inconsistent.

```package COM.google_search.common;```

- Sometimes a very long line of code could be used which usually violates the readability standards.

- Or sometimes a variable used in a class scope in a concurrently ran singleton Java object violates thread safety as could be a security issue.


#### Static Code Analysis
Reviewing is viewing the software by reviewer and the reviewers’ own comments and best practice notes will be used as the final output. There are also static code analysis tools like PMD for Java which generally checks the code against bugs and clean code. These static code analyses usually attached to the final code review report of the reviewer and usually is only helpful for a detailed overview for the clean code. Sometimes software development IDEs also providing best practices while writing the code. I like the PyCharm IDE’s smart clean code suggestions for Python as example.


#### Automated Code Review
Automated testing is subject to measurable reports and static code analysis. Static code analysis tools can be scheduled for code checking and reporting. Also testing the code as a preparation for code review is another process can be automated and already part of the SDLC processes. Some overlooked issues like releasing resources and concurrency issues can be also checked by automated tests and can be reported as automated code review results.


#### Conclusion
I tried to outline the general code review cycle of a project. Depending on the programming language and the decided architecture of the software to be developed there can be additional best practices like functional, non-functional, OOP design principles etc. The reviewers may extend or lessen their checklist items according future plans, architecture or review request coverage.