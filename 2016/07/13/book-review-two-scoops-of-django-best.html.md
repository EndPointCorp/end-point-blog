---
author: Phin Jensen
gh_issue_number: 1242
tags: books, django
title: "Book review: \u201CTwo Scoops of Django: Best Practices for Django 1.8\u201D"
---



*Two Scoops of Django: Best Practices for Django 1.8* is, shockingly, a book about best practices. It’s not a Django library reference, or a book about Django fundamentals, or tips and tricks. It’s a book designed to help web developers, novices and experts alike, avoid common pitfalls in every stage of the web development process, specifically the process of developing with Django.

The book can be used as a reference of best practices and a cover-to-cover guide to best practices. I’ve done both and found it to be enjoyable, accessible, and educational when read cover-to-cover and a valuable reference when setting up a new Django project or doing general Django development. It covers a huge range of material, answering questions like:

- Where should I store secret keys?
- Should I use virtualenv?
- How should I structure my Django project?
- When should I use ‘blank’ and ‘null’ in model fields?
- Should I use Class-Based Views or Function-Based Views?
- How should I structure my URLConfs?
- When should I use Forms?
- Where should templates be stored?
- Should I write custom template tags and filters?
- What package should I use to create a REST API?
- What core components should I replace?
- How can I modify or replace the User and authentication system?
- How should I test my app?
- How can I improve performance?
- How can I keep my app secure?
- How do I properly use the logging library?
- How do I deploy to a Platform as a Service or my own server(s)?
- What can I do to improve the debugging process?
- What are some good third-party packages?
- Where can I find good documentation and tutorials?
- Where should I go to ask more questions?

The question, then, is whether or not this book delivers this information well. For the most part, it does. It’s important to recognize that the book doesn’t cover any of these subjects in great detail, but it does do a great job explaining the “why” behind some of the simple rules that are established and referencing online resources that can be used to go much more in-depth with the subject. It does a great job showing clearly marked bad examples, making it very easy to see whether or not you are or were planning on doing something badly. The writing style is very accessible and straightforward; I read large portions of the book during breakfast or lunch.

Two sections stood out to me as being very helpful for my own projects. First is Chapter 4, Fundamentals of Django App Design, which explained better than any resource I’ve found yet exactly what a Django “app” (as in ./manage.py startapp polls) should be used for. It explains what an app should or shouldn’t have in it, how much an app should do, when you should break into separate apps, and more.

The next section that really helped me was Chapter 6, Model Best Practices, which explained things like what code should and shouldn’t be in a model, how to use migrations and managers, and ModelFields that should be avoided. Perhaps the most useful part of that chapter is a table in the section “When to use Null and Blank,” which makes for an easy and quick reference to which fields go well with the null and blank parameters and when you should use both or neither.

The only real problem I had with Two Scoops of Django was that the illustrations rarely felt necessary or helpful. The majority of them are ice cream-themed jokes that aren’t particularly funny. Overall, I really enjoyed this book and I definitely recommend it for anybody who is or is interested in doing serious Django development.


