---
author: Steph Skardal
title: 'Open Source: Challenges of Modularity and Extensibility'
github_issue_number: 958
tags:
- open-source
date: 2014-04-07
---

While I was at the [I Annotate 2014](http://iannotate.org/2014/) conference last week, I spoke with a couple developers about the challenges of working in open source. Specifically, the [Annotator JavaScript](http://annotatorjs.org/) library that we are using for [H2O](https://cyber.law.harvard.edu/research/h2o) is getting a bit of a push from the community to decouple (or make more modular) some components as well as improve the extensibility. Similarly, Spree, an open source Ruby on Rails platform that End Point has sponsored in the past and continued to work with, made a shift from a monolithic platform to a modular (via Ruby gems) approach, and [Piggybak](https://github.com/piggybak/piggybak) started out as a modular and extensible ecommerce solution. I like doodling, so here’s a diagram that represents the ecosystem of building out an open source tool with a supplemental explanation below:

<img border="0" src="/blog/2014/04/open-source-challenges-of-modularity/image-0.jpeg" width="100%"/>

Here are some questions I consider on these topics:

- What is the cost of extensibility?

    - code complexity
    - code maintenance (indirectly, as code complexity increases)
    - harder learning curve for new developers (indirectly, as code complexity increases)
    - performance implications (possibly, indirectly, as code complexity increases)
    - difficulty in testing code (possibly)

- What is the cost of modularity?

    - same as cost of extensibility
    - challenge of determining what features to include in core (or exclude from core)
    - can be both performance implications and performance mitigation

- What are the values of extensibility?

    - robustness of tool
    - increased community involvement (indirectly, as robustness increases)
    - further reach, increased use cases (indirectly, as robustness increases)

- What are the values of modularity

    - same as values of extensibility

From a cost-benefit perspective, the goal here should allow the values of extensibility and modularity to outweigh the disadvantages to allow for a flourishing, growing community of developers and users of the tool. Extensibility and modularity are not always easy to figure out, especially in some frameworks, but I think getting these two elements correct are very important factors in the success of an open source project. I also don’t think many tools "get it right" the first time around, so there’s always a chance to improve and refactor as the user base builds.
