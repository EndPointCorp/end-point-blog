---
author: Steph Skardal
title: Updated End Point Blog Stats and Our Services
github_issue_number: 1091
tags:
- company
date: 2015-02-10
---

Today, I sat down to read through a few recent End Point blog articles and was impressed at the depth of topics in recent posts ([PostgreSQL](/blog/2015/02/postgres-custom-casts-and-pgdump), [Interchange](/blog/2015/02/interchange-loop-optimization), [SysAdmin](/blog/2015/02/cron-wrapper-keep-your-cron-jobs), [Text Editors (Vim)](/blog/2015/02/vim-plugin-spotlight-ctrlp), [Dancer](/blog/2015/02/filling-in-header-elements-with-dancer), [AngularJS](/blog/2015/02/polemics-on-opinions-about-angularjs)) from my coworkers. The list continues if I look further back covering technologies in both front and back end web development. And, this list doesn’t even cover the topics I typically write about such as Ruby on Rails & JavaScript.

While 5 years ago, we may have said we predominately worked with ecommerce clients, our portfolio has evolved to include [Liquid Galaxy](https://liquidgalaxy.endpoint.com/) clients and many non-ecommerce sites as well. With the inspiration from reading through these recent posts, I decided to share some updated stats.

Do you remember [my post on Wordle](/blog/2011/02/in-our-own-words) from early 2011? [Wordle](http://www.wordle.net/) is a free online word cloud generator. I grabbed updated text from 2013 and on from our blog, using the code [included in my original post](/blog/2011/02/in-our-own-words), and generated a new word cloud from End Point blog content:

<img border="0" src="/blog/2015/02/updated-end-point-blog-stats-and-our/image-0.png" width="800px"/>

End Point blog Word cloud from 2013 to present

I removed common words from the word cloud not removed from the original post, including “one”, “like”, etc. Compared to the original post, it looks like database related topics (e.g. [PostgreSQL](/technology/postgresql)) still have strong representation on the blog in terms of word count, and many other common developer words. [Liquid Galaxy](https://liquidgalaxy.endpoint.com/) now shows up in the word cloud (not surprising), but many of the other technology specific terms are still present (Spree, [Rails](/technology/ruby-on-rails), [Bucardo](/technology/replication)).

I also took a look at the top 10 blog posts by page views, as compared to [this post](/blog/2010/01/2009-end-point-blogging):

- [Streaming Live with Red5 Media Server](/blog/2012/04/streaming-live-with-red5-media-server)
- [API gaps: an Android MediaPlayer example](/blog/2011/03/api-gaps-android-mediaplayer-example)
- [Streaming Live with Red5 Media Server: Two-Way](/blog/2013/03/streaming-live-with-red5-media)
- [Using cec-client to Control HDMI Devices](/blog/2012/11/using-cec-client-to-control-hdmi-devices)
- [MySQL and Postgres command equivalents (mysql vs psql)](/blog/2009/12/mysql-and-postgres-command-equivalents)
- [RailsAdmin: A Custom Action Case Study](/blog/2012/03/railsadmin-custom-action-case-study)
- [Git Workflows That Work ](/blog/2014/05/git-workflows-that-work)
- [Increasing MySQL 5.5 max_connections on RHEL 5](/blog/2013/12/increasing-mysql-55-maxconnections-on)
- [Restoring individual table data from a Postgres dump](/blog/2010/04/restoring-individual-table-data-from)
- [Using ln -sf to replace a symlink to a directory](/blog/2009/09/using-ln-sf-to-replace-symlink-to)

The page views are not normalized over time, which means older blog posts would not only have more page views, but also have more time to build up traffic from search. Again, this list demonstrates qualitatively the broad range of topics for which our blog is popular, including both very technology specific posts as well as general development topics. I also suspect our traffic continues to attract long-tail keywords, described more [in this post](/blog/2010/02/code-seo-google-analytics-api).

Finally, back in October, I visited End Point’s Tennessee office and got into a discussion with [Jon](/team/jon-jensen) about how we define our services and/or how our business breaks down into topics. Here’s a rough chart of what we came up with at the time:

<img border="0" src="/blog/2015/02/updated-end-point-blog-stats-and-our/image-1.png"/>

How do End Point services break down?

Trying to explain the broad range and depth of our services can be challenging. Here are a few additional notes related to the pie chart:

- Our [Liquid Galaxy](https://liquidgalaxy.endpoint.com/) work spans across the topics of Hardware & Hosting, Cloud Systems, and Databases.
- Our [Ecommerce](/ecommerce) services typically includes work in the topics of Backend & Client Side Development, as well as Databases.
- Our development in mobile applications spans Backend & Client Side Development.

All in all, I’m impressed that we’ve continued to maintain expertise in long-standing topics such as PostgreSQL and Interchange, but also haven’t shied away from learning new technologies such as GIS as related to Liquid Galaxy and JavaScript frameworks.

### PS

P.S. If you are interested in generating word statistics via command line, the following will get you the top 20 words given a text file:

```nohighlight
tr -c '[:alnum:]' '[\n*]' < some_text_file.txt | sort | uniq -c | sort -nr | head -20
```
