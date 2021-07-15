---
author: Greg Sabino Mullane
title: State of the Postgres project
github_issue_number: 245
tags:
- community
- database
- mysql
- postgres
date: 2010-01-04
---



It’s been interesting watching [the](https://web.archive.org/web/20100304140554/http://blogs.the451group.com/opensource/2009/10/26/everything-you-always-wanted-to-know-about-mysql-but-were-afraid-to-ask/) [MySQL](https://web.archive.org/web/20100821005629/http://blogs.the451group.com/opensource/2009/11/12/everything-you-always-wanted-to-know-about-mysql-but-were-afraid-to-ask-part-two/) [drama](https://web.archive.org/web/20100109005715/http://blogs.the451group.com/opensource/2010/01/04/everything-you-always-wanted-to-know-about-mysql-but-were-afraid-to-ask-part-three/) unfold, but I have to take issue when people start trying to drag Postgres into it again by spreading FUD (Fear, Uncertainty, and Doubt). Rather than simply rebut the FUD, I thought this was a good opportunity to examine the strength of the Postgres project.

Monty recently espoused the following in a [blog comment](https://web.archive.org/web/20100329100324/http://ostatic.com/blog/oracle-mysql-and-the-gpl-dont-take-montys-word-for-it):

> “...This case is about ensuring that Oracle doesn’t gain money and market share by killing an Open Source competitor. Today MySQL, tomorrow PostgreSQL.
> 
> Yes, PostgreSQL can also be killed; To prove the case, think what would happen if someone managed to ensure that the top 20 core PostgreSQL developers could not develop PostgreSQL anymore or if each of these developers would fork their own PostgreSQL project.”
> 

Later on in his blog [he raises the same theme again](http://monty-says.blogspot.com/2009/12/help-keep-internet-free.html) with a slight bit more detail:

> “Note that not even PostgreSQL is safe from this threat! For example, Oracle could buy some companies developing PostgreSQL and target the core developers. Without the core developers working actively on PostgreSQL, the PostgreSQL project will be weakened tremendously and it could even die as a result.”
> 

Is this a valid concern? It’s easy enough to overlook it considering the Sturm und Drang in Monty’s recent posts, but I think this is something worth seriously looking into. Specifically, is the Postgres project capable of withstanding a direct threat from a large company with deep pockets (e.g. Oracle)?

To get to the answer, let’s run some numbers first. Monty mentions the “top 20” Postgres developers. If we look at the [community contributors](https://www.postgresql.org/community/contributors/) page, we see that there are in fact 25 major developers listed, as well as 7 core members, so 20 would indeed be a significant chunk of that page. To dig deeper, I looked at the cvs logs for the year of 2009 for the Postgres project, and ran some scripts against them. The 9185 commits were spread across 16 different people, and about 16 other people were mentioned in the commit notes as having contributed in some way (e.g. a patch from a non-committer). So again, it looks like Monty’s number of 20 is a pretty good approximation.

However (and you knew there was a however), the catch comes from being able to actually stop 20 of those people from working on Postgres. There are basically two ways to do this: Oracle could buy out a company, or they could hire (buy out) a person. The first problem is that the Postgres community is very widely distributed. If you look at the people on the community contributors page, you’ll see that the 32 people work for 24 different companies. Further, no one company holds sway: the median is one company, and the high water mark is a mere three developers. All of this is much better than it was years ago, in the total number and in the distribution.

The next fly in the ointment is that buying out a company is not always easy to do, despite the size of your pockets. Many companies on that list are privately held and will not sell. Even if you did buy out the company, there is no way to prevent the people working there from then moving to a different company. Finally, buying out some companies just isn’t possible, even if you are Oracle, because there are some big names on the list of people employing major Postgres developers: Google, Red Hat, Skype, and SRA. Then of course there is NTT, which is a **really, really** big company (larger than Oracle). NTT’s Postgres developers are not always as visible as some of the English-speaking ones, but NTT employs a lot of people to work on Postgres (which is extremely popular in Japan).

The second way is hiring people directly. However, people can not always be bought off. Sure, some of the developers might choose to leave if Oracle offered them $20 million dollars, but not all of them (Larry, I might go for $19 million, call me :). Even if they did leave, the depth of the Postgres community should not be underestimated. For every “major developer” on that page, there are many others who read the lists, know the code well, but just haven’t, for one reason or another, made it on to that list. At a rough guess, I’d say that there are a couple hundred people in the world who would be able to make commits to the Postgres source code. Would all of them be as fast or effective as some of the existing people? Perhaps not, but the point is that it would be nigh impossible to thin the pool fast enough to make a dent.

The project’s [email lists](https://postgresql.markmail.org/) are as strong as ever, to such a point that I find it hard to keep up with the traffic, a problem I did not have a few years ago. The number of conferences and people attending each is growing rapidly, and there is a great demand for people with Postgres skills. The number of projects using Postgres, or offering it as an alternative database backend, is constantly growing. It’s no longer difficult to find a hosting provider that offers Postgres in addition to MySQL. Most important of all, the project continues to regularly release stable new versions. Version 8.5 will probably be released in 2010.

In conclusion, the state of the Postgres project is in great shape, due to the depth and breadth of the community (and the depth and breadth of the developer subset). There is no danger of Postgres going the MySQL route; the PG developers are spread across a number of businesses, the code (and documentation!) is BSD, and no one firm holds sway in the project.


