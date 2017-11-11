---
author: Greg Sabino Mullane
gh_issue_number: 263
tags: community, database, open-source, postgres
title: PostgreSQL version 9.0 release date prediction
---



So when will PostgreSQL version 9.0 come out? I decided to "run the numbers" and take a look at how the Postgres project has done historically. Here's a quick graph showing the approximate number of days each major release since version 6.0 took:

<a href="http://4.bp.blogspot.com/_BSsdd9WIV2k/S2x1d_lS9KI/AAAAAAAAAAU/ur4JnsuCxno/s1600-h/postgres_version_days.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5434848008473867426" src="/blog/2010/02/05/postgresql-version-90-release-date/image-0.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 278px;"/></a>

Some interesting things can be seen here: there is a rough correlation between the complexity of a new release and the time it takes, major releases take longer, and the trend is gradually towards more days per release. Overall the project is doing great, releasing on average every 288 days since version 6. If we only look at version 7 and onwards, the releases are on average 367 days apart. If we look at *just* version 7, the average is 324 days. If we look at *just* version 8, the average is 410. Since the last major version that came out was on July 1, 2009, the numbers predict 9.0 will be released on July 3, 2010, based on the version 7 and 8 averages, and on August 15, 2010, based on just the version 8 averages. However, this upcoming version has two very major features, streaming replication (SR) and hot standby (HS). How those will affect the release schedule remains to be seen, but I suspect the 9.0 to 9.1 window will be short indeed.

As a recap, the Postgres project only bumps the first part of the version number for major changes (Although many, myself included, would argue that 7.4 was such a major jump it should have been called 8.0). The second number occurs anytime a "new release" happens, and means new features and enhancements. The final number, the revision, is only incremented for security and bug fixes, and is almost always a 100% binary compatible drop in for the previous revision in the branch. (What's the average (mean) days between revisions? 84 days since version 6, and 88 days since version 7. The medians are 84 and 87 respectively.)

How busy were those periods? Here's the number of commits per release period. Note that I said release period, not release, as commits are still being made to old branches, although this is a very small minority of the commits, so I did not bother to break it down at that level.

<a href="http://3.bp.blogspot.com/_BSsdd9WIV2k/S2yEw2Dtc7I/AAAAAAAAAAc/RY1PclESiQY/s1600-h/postgres_version_commits.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5434864825009009586" src="/blog/2010/02/05/postgresql-version-90-release-date/image-0.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 280px;"/></a>

There is a strong correlation with the previous chart. Of note is version 8.1, which had few commits and was released relatively quickly. Also note that version 8.0 is still winning as far as the sheer number of commits, most likely due to the fact that native Windows support was added in that version.

Some other items of interest from the data:

- There have been roughly 140,000 commits from version 6.0 to 8.4.2.- There have been 32 CVS committers since the start of the project (and of course, many hundreds of others whose work was funnelled through those committers)- The mean number of commits per person is 4383, but the distribution is very skewed: Bruce, Peter, and Tom account for 80% of all commits, with the mean between them of 37,000 commits.- Commits changed about 40 lines on average.

Alright, two final charts: commits per time periods. I'll let the data speak for itself this time. Stay tuned for future blog posts exploring this data further!

<a href="http://4.bp.blogspot.com/_BSsdd9WIV2k/S2yNYHG1wPI/AAAAAAAAAAk/FzFGLixpN8w/s1600-h/postgres_commits_dow.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5434874295693459698" src="/blog/2010/02/05/postgresql-version-90-release-date/image-0.png" style="cursor: pointer; width: 400px; height: 275px;"/></a>

<a href="http://2.bp.blogspot.com/_BSsdd9WIV2k/S2yS7-TQuoI/AAAAAAAAAAs/LDxOqcqDKNw/s1600-h/postgres_commits_hour.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5434880409363069570" src="/blog/2010/02/05/postgresql-version-90-release-date/image-0.png" style="margin:0 0 10px 10px;cursor:pointer; cursor:hand;width: 261px; height: 320px;"/></a>


