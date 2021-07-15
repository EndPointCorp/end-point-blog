---
author: Sam Batschelet
title: Perl Dancer Conference 2016 Day 1
github_issue_number: 1271
tags:
- conference
- perl
- devops
date: 2016-11-30
---

<img border="0" height="306" src="/blog/2016/11/perl-dancer-conference-2016-day-1/image-0.jpeg" width="320"/>

## Perl Dancer Conference Day 1

The [Perl Dancer Conference](https://perl.dance/) is a great event, now in its third year. <img align="left" border="0" height="90" src="/blog/2016/11/perl-dancer-conference-2016-day-1/image-1.png" width="130"/> The event took place in the same location as last year in Vienna, Austria at the Hotel Schani Wien. For those of you who have never visited Vienna, it is a perfect place to bring the family. From visiting the beautiful parks to taking a scenic ride on the Danube River, the beautiful and historic city is known for its rich art and musical culture, and has much to offer.

I was very excited to not only attend but also give a talk this year. My talk titled [“Dancing in the Clouds”](https://www.perl.dance/talks/45-dancing-in-the-clouds) also coincided with the release of 2 new Perl modules [Etcd3](https://metacpan.org/pod/Etcd3) and [Dancer2::Plugin::Etcd](https://metacpan.org/pod/Dancer2::Plugin::Etcd). This article will be the first of a 3 part series, with the final article a focus on my talk and usage examples with the new modules.

### Sawyer X (Sawyer X) — A bus tour through Dancer core

The Captain of Dancer core, SawyerX, took us on a bus tour through the core functionality of Dancer2. Using practical examples of code blocks from core, he explained how different areas of the code base worked. I personally enjoyed his explanation of how hooks are implemented and created. Learning from the 1st iteration of Dancer, the second version shows maturity and stability.

### Stefan Hornburg (Racke) — No Act on ACT

If you have ever taken the time to review a Perl conference’s website or even purchase tickets to attend you have no doubt been in contact with ACT. “Act (A Conference Toolkit) is a multilingual, template-driven, multi-conference website that can manage the users, talks, schedule, and payment for your conference.” While this package has been around for many years, it is somewhat dreaded because of its lack of features.

Stefan outlines his work with Interchange6::Schema and the perl.dance website painting a picture of the replacement for ACT. Utilizing Dancer2, DBIx::Class, Moo and other modern Perl tools the infrastructure outlined is very compelling. The package has a user admin, e-commerce, and even a module to print out the passes. Although he notes that this is not a plug and play replacement for ACT yet, with a bit of work and support, it could be the future of Perl conference management.

### Andrew Beverly — Implementing i18n in a Dancer application using Plugin::LogReport

Andrew extended his talk last year about internationalization with the Dancer2::Plugin::LogReport module. Using great examples, he not only outlined the usage of the module, but also got into details of how the process works on a technical level. Explaining the different ways that internationalization can be done, he begins to outline how he achieved his task of deploying i18n in a Dancer app.

### Theo van Hoesel — Quickstep

Theo was a great addition to the conference this year. He was able to make the event on very short notice after Dancer core Jason Crome was not able to attend due to injury. Theo outlined the Act::Voyager project briefly and the general requirements of adding user friendly features to the ACT toolkit. He also spent a good amount of time explaining the concept of web caching and how many of the existing modules failed in the task of complying with RFC7234. He then explained how all of this brought him to create HTTP::Caching and how it has “The RFC 7234 compliant brains to do caching right”. Along with this contribution part of the HTTP::Bundle, his Dancer focused Dancer2::Plugin::HTTP::Bundle was explained.

### Job van Achterberg (jkva) — Dancing with Disabilities

Job’s talk was a very interesting look into how taking a considerate approach to development and small changes to your code can improve a disabled web user’s experience. Using the tools in macOS Job showed how simple things such as naming a list are reflected in a disabled users ability to get information. What I found very interesting in this presentation was how awkward the tools were to use even for an experienced pro like Job. It really made me think a lot about the challenges the disabled face in something many of us take for granted.

### Jason Lewis — The Lazy Programmer’s Guide to building HTML tables in Dancer2

Jason has become a regular on the #dancer freenode IRC channel. This year he decided to travel all the way from Australia to give his presentation on his experiences replacing Crystal Reports with Dancer2 Template::Toolkit and DataTables. Although a great deal of the presentation was focused on the features of the jQuery plugin DataTables, he gave nice examples of code he used to populate reports and the hurdles he faced replacing Crystal Reports functionality. The reports looked beautiful and were very easy to convert to other data types such as PDF and CSV.

### Stefan Seifert (nine) — Perl 5 and Perl 6 — a great team

Stefan is a great presence at the conference, and his fun and witty personality carried over to his presentation. After opening with a really funny skit as a reporter reading the the news, he continued to outline the current state of Perl6 and how important it is for all of us as a community to embrace the fact that we are all in this together. He reminded us of the perils of Python3’s launch and the lack of support even today. He then began to focus on the capabilities of using Perl5 with Perl6 together with Inline::Perl5 and Inline::Perl6 modules. To be honest before his talk I had given Perl6 very little time. Stefan’s talk opened my eyes to the possibilities of utilizing the two versions together and the advantages that ecosystem has.

Please stop back for links to day 2 of the conference and a breakdown of my talk outlining [etcd](https://coreos.com/etcd/) integration with Perl and [Dancer2](http://perldancer.org/).
