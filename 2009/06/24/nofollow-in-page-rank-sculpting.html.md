---
author: Steph Skardal
gh_issue_number: 161
tags: seo
title: nofollow in PageRank Sculpting
---

Last week the SEO world reacted to [Matt Cutts' article](http://www.mattcutts.com/blog/pagerank-sculpting/) about the use of nofollow in PageRank sculpting.

Google uses the [PageRank](http://en.wikipedia.org/wiki/PageRank) algorithm to calculate popularity of pages in the web. Popularity is only one factor in determining which pages are returned in search results (relevance to search terms is the other major factor). Other major search engines use similar popularity algorithms. Without describing the algorithm in detail, the important takeaways are:

- PageRank of a single page is influenced by all inbound (external links) links
- PageRank of a single page is passed on to all outgoing links after being normalized and divided by the total number of outgoing links

So, given page C with an inbound links from page A and B, where page A and B have equal page rank X, page A has 3 total external links and B has 5 total external links, page C receives more PageRank from page A than page B.

<a href="http://1.bp.blogspot.com/_wWmWqyCEKEs/SkJx484BdLI/AAAAAAAABuY/HPa0OXDZC3c/s1600-h/pr1.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5350964530497287346" src="/blog/2009/06/24/nofollow-in-page-rank-sculpting/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 390px;"/></a>

From an external link perspective, it's great to get as many links as possible from a variety of sources that rank high and have a low number of external links. From an internal site perspective, it's important to examine how PageRank is passed throughout a site to apply the best site architecture. In addition to designing a site architecture that pleases users and passes link juice throughout a site effectively, the rel="nofollow" tag was adopted by several major search engines and was used as an additional tool to stop the flow of link juice from one page to another. The nofollow tag can also be used to identify paid links (early implementation) or to avoid passing links to external sites completely.

In the example above, rel="nofollow" could be added to 2 links on page B which would result in the same PageRank passed from page B to page C as from page A to page C.

<a href="http://1.bp.blogspot.com/_wWmWqyCEKEs/SkJx5C0oxcI/AAAAAAAABug/-WPznLcuCdI/s1600-h/pr2.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5350964532093699522" src="/blog/2009/06/24/nofollow-in-page-rank-sculpting/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 335px;"/></a>

Then, at a recent SEO conference, Matt Cutts (head of the Google spam team) made a comment about how the PageRank algorithm changed its use of nofollow and just last week, it was announced that the PageRank algorithm would no longer use the nofollow attribute in PageRank sculpting. Any link with the nofollow attribute will no longer reduce the count of outgoing page links to improve link juice passed on to other pages, but link juice will still not be passed from one link to another with the nofollow attribute.

In the ongoing example, the link juice passed from page B to page C will be less than from page A to C because it has more outgoing links, even if they are nofollow links.

<a href="http://4.bp.blogspot.com/_wWmWqyCEKEs/SkJx5Z86AuI/AAAAAAAABuo/e-bVOvB3Eik/s1600-h/pr3.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5350964538302399202" src="/blog/2009/06/24/nofollow-in-page-rank-sculpting/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 335px;"/></a>

One [SEOmoz article](http://www.seomoz.org/blog/google-says-yes-you-can-still-sculpt-pagerank-no-you-cant-do-it-with-nofollow) I read suggests that SEO best practices will now be to recommend blog owners to disallow comments that may contain external links to prevent the dilution of link juice. Other potential solutions would be to filter out links from user generated content (comments or qna specifically), use iframes to display any user generated content, or embed flash or java with external links. The nofollow attribute may be used to stop the flow of link juice to external pages, however, it may no longer be used for internal PageRank sculpting.
