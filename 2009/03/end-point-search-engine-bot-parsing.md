---
author: Steph Skardal
title: 'End Point: Search Engine Bot Parsing'
github_issue_number: 121
tags:
- seo
date: 2009-03-25
---

I’ve talked to several coworkers before about bot parsing, but I’ve never gone into too much detail of why I support search engine bot parsing. When I say bot parsing, I mean applying regular expressions to access log files to record distinct visits by the bot. Data such as the url visited, exact date-time, http response, bot, and ip address is collected. Here is a visual representation of bot visits (y-axis is hits).

<a href="https://4.bp.blogspot.com/_wWmWqyCEKEs/ScrWJYHi6gI/AAAAAAAABrk/T4C1oS7V1GM/s1600-h/n4.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5317297766645557762" src="/blog/2009/03/end-point-search-engine-bot-parsing/image-0.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 183px;"/></a>

And here are the top ten reasons why search engine bot parsing should be included in search engine optimization efforts:

\#10: **It gives you the ability to study search engine bot behavior.** What is bot behavior after 500 error responses to a url? What IP addresses are the bots coming from? Do bots visit certain pages on certain days? Do bots *really* visit js and css pages?

\#9: **It can be used as a teaching tool.** Already, I have discussed certain issues from data generated by this tool and am happy to teach others about some search engine behavior. After reading this post, you will be much more educated in bot crawling!!

\#8: **It gives you the ability to compare search engine bot behavior across different search engines.** From some of the sites I’ve examined, the Yahoo bot has been visiting much more frequently than Googlebot, msnbot, and Teoma (Ask.com). I will follow up this observation by investigating which urls are getting crawled by Yahoo so much more frequently.

\#7: **It can help identify where 302s (temporary redirects) are served when 301s (permanent redirects) should be served.** For example, spree has a couple of old domains that are 302-ing occassionally. We now have the visibility to identify these issues and remediate them.

<a href="https://3.bp.blogspot.com/_wWmWqyCEKEs/ScrWTgHw71I/AAAAAAAABrs/d0YqN59Epx0/s1600-h/n7.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5317297940592652114" src="/blog/2009/03/end-point-search-engine-bot-parsing/image-1.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 259px;"/></a>

\#6: **It gives you the ability to study bot crawling behavior across different domains.** Today, I was asked if there was a metric for a “good crawl rate”. I’m not aware of a metric, but comparing data across different domains can certainly give you some context to the data to determine where to make search engine optimization efforts if you are divided between several domains.

<a href="https://3.bp.blogspot.com/_wWmWqyCEKEs/ScrWd5WbQsI/AAAAAAAABr0/YmZ6eJE7UV0/s1600-h/n6p1.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5317298119163724482" src="/blog/2009/03/end-point-search-engine-bot-parsing/image-2.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 186px;"/></a>

Website #1

<a href="https://4.bp.blogspot.com/_wWmWqyCEKEs/ScrWeBv_R4I/AAAAAAAABr8/MFUUGVZXUq4/s1600-h/n6p2.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5317298121418426242" src="/blog/2009/03/end-point-search-engine-bot-parsing/image-3.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 183px;"/></a>

Website #2

\#5: **It gives you the ability to determine how often your entire site is crawled.** I previously developed a bot parsing tool that did a comparison to the urls included in the sitemap. It provided metrics of how often 100% of a site was crawled or even how often 50% of a site was crawled. Perhaps only 95% of your site has ever been crawled - this tool can help identify which pages are not getting crawled. This data is also relevant because as the bots deem your content more “fresh”, they will visit more. “Freshness” is an important factor in search engine performance.

<a href="https://4.bp.blogspot.com/_wWmWqyCEKEs/ScrWs1sAfXI/AAAAAAAABsE/wM5oyiZNwFc/s1600-h/n5.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5317298375878540658" src="/blog/2009/03/end-point-search-engine-bot-parsing/image-4.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 250px;"/></a>

\#4: **It gives you the ability to correlate search engine optimization efforts with changes in bot crawling.** Again, the goal is to increase your bot visits. If you begin working on a search engine marketing campaign, the bot crawl rate over time will be one KPI (key performance indicator) to measure the success of the campaign.

\#3: **It gives you the immediate ability to identify crawlability issues such as 500 or 404 responses, or identify the frequency of duplicate content being crawled.** Many other tools can provide this information as well, but it can be important to distinguish bot behavior from user behavior.

<a href="https://3.bp.blogspot.com/_wWmWqyCEKEs/ScrWs90XNjI/AAAAAAAABsM/vOpV5cK5q3s/s1600-h/n3.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5317298378061067826" src="/blog/2009/03/end-point-search-engine-bot-parsing/image-5.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 252px;"/></a>

\#2: **It provides a benchmark for bot crawling.** Whether you are implementing a search engine marketing campaign or are simply making other website changes, this data can server as a good benchmark. If a website change immediately causes bot crawling problems, you can identify the problem before finding out a month later as search engine results start to suffer. Or, if a website change causes an immediate increase in bot visibility, keep it up!

<a href="https://2.bp.blogspot.com/_wWmWqyCEKEs/ScrWtBS9VZI/AAAAAAAABsU/ySSi_o7yy80/s1600-h/n2.gif" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5317298378994701714" src="/blog/2009/03/end-point-search-engine-bot-parsing/image-6.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 188px;"/></a>

And the #1 reason to implement bot parsing is...

**“cuz robots are cool”,** *Aleks*. No explanation necessary.

<a href="http://www.mwctoys.com/REVIEW_061808a.htm" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5317298379611777938" src="/blog/2009/03/end-point-search-engine-bot-parsing/image-7.gif" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 200px; height: 361px;"/></a>
