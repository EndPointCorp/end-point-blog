---
author: Steph Skardal
title: Content Syndication, SEO, and the rel canonical Tag
github_issue_number: 238
tags:
- seo
date: 2009-12-17
---

### End Point Blog Content Syndication

The past couple weeks, I’ve been discussing if content syndication of our blog negatively affects our search traffic with [Jon](/team/jon-jensen). Since the blog’s inception, full articles have been syndicated by [OSNews](http://www.osnews.com/). The last couple weeks, I’ve been keeping an eye on the effects of content syndication on search to determine what (if any) negative effects we experience.

By my observations, immediately after we publish an article, the article is indexed by Google and is near the top search results for a search with keywords similar to the article’s title. The next day, OSNews syndication of the article shows up in the same keyword search, and our article disappears from the search results. Then, several days later, our article is ahead of OSNews as if Google’s algorithm has determined the original source of the content. I’ve provided visual representation of this behavior:

<a href="http://3.bp.blogspot.com/_wWmWqyCEKEs/SyrLDr2gVsI/AAAAAAAAC1U/qCiICz4Dk6U/s1600-h/contentsyndication.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5416364766037825218" src="/blog/2009/12/content-syndication-seo-rel-canonical/image-0.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 149px;"/></a>

With content syndication of our blog articles, there is a several day lag where Google treats our blog article as the duplicate content and returns the OSNews article in search results for a search similar to our the blog article’s title. After this lag time, the OSNews article is treated as duplicate content and our article is shown in the search results.

<a href="http://4.bp.blogspot.com/_wWmWqyCEKEs/SyrLCz9MRnI/AAAAAAAAC1E/aKcg77ZqpPg/s1600-h/example1.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5416364751033484914" src="/blog/2009/12/content-syndication-seo-rel-canonical/image-0.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 244px;"/></a>

During the lag time, a search for “google pages indexed seo”, an article I published last Thursday, the OSNews article is shown at search position #5.

<a href="http://3.bp.blogspot.com/_wWmWqyCEKEs/SyrLDcTVJxI/AAAAAAAAC1M/cwtg7yjTgy8/s1600-h/example2.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5416364761863759634" src="/blog/2009/12/content-syndication-seo-rel-canonical/image-0.png" style="margin: 0px auto 10px; display: block; text-align: center; cursor: pointer; width: 400px; height: 238px;"/></a>

After the lag time, a search for “google pages indexed seo” returned the original End Point blog article to search position #2.

Several other factors have influenced the lag time, but typically I’ve seen very similar behavior.

End Point’s content syndication has only been an issue with blog articles, since the majority of our new content comes in the form of blog articles. Examples of content syndication in the ecommerce space may include:

- inner-company content syndication of products across sister sites. For example, our client [Backcountry.com](http://www.backcountry.com/) sells outdoor gear, while their site [RealCyclist](http://www.realcyclist.com/) targets the road biking niche of the outdoor gear industry. Cycling products sold on both sites and may compete directly for search engine traffic.
- syndication of product information through affiliate programs like [Commission Junction](http://www.cj.com/) and [AvantLink](http://www.avantlink.com/). Affiliates are paid a small portion of the sales and may target traffic by building supplementary content or communities around content provided by ecommerce sites through the affiliate program.

### Cross-Domain rel=canonical Tag

I’ve been planning to write this article and with impeccable timing, [Google announced support for the rel=canonical tag across different domains](https://webmasters.googleblog.com/2009/12/handling-legitimate-cross-domain.html) this week. I’ve referenced the use of the rel=canonical tag in two articles ([PubCon 2009 Takeaways](/blog/2009/11/pubcon-vegas-7-takeaway-nuggets), [Search Engine Thoughts](/blog/2009/02/search-engine-optimization-thoughts)), but I haven’t gone too much into depth about its use. Support of the rel=canonical tag was introduced early this year as a method to help decrease duplicate content across a single domain. A non-canonical URL that includes this tag suggests its canonical URL to search engines. Search engines then use this suggestion in their algorithms and results to reduce the effects of duplicate content.

```nohighlight
<link rel="canonical" href="http://www.example.com/product.php?item=swedish-fish" />
```

With the cross-domain rel=canonical support announcement, the rel=canonical tag presents another tool to battle duplicate content from content syndication across domains.

### Back to Content Syndication

The point of my investigation was to identify whether or not content syndication to OSNews negatively affects our search traffic. The data above suggests that after the brief lag time, Google’s algorithm sorts out the source of the original content. The value of exposure, referral traffic, and link juice from OSNews outweighs lost search traffic during this lag time.

In the example of similar product content across backcountry.com’s sites, using the rel=canonical tag across domains would allow backcountry.com to suggest prioritization of same product URLs for search results. This may be a valuable tool for directing search traffic to the desired domain.

In the example of content syndication across sites that are not owned by the same company, the use of the rel=canonical tag is more complicated. If the goals of the site that grabs content are to compete directly for search traffic, they would likely not want to use the canonical tag. However, if the goal of the site that grabs content is to focus on search traffic from aggregate content or by building a community around the valuable content, they may be more willing to implement the cross-domain rel=canonical tag to point to the original source of the content. In the case of affiliate programs, I believe it will be difficult to negotiate the cross-domain rel=canonical tag use into existing or future contracts.

The takeaways:

- Content syndication of our blog does not cause negative long term effects on search. This should be monitored for sites that may have much different behavior than the data I provided above.
- The announcement of support of the cross-domain rel=canonical tag may be helpful for battling duplicate content across sites, especially to sites owned by the same company.
- The use of the cross-domain rel=canonical tag in affiliate programs or through sites owned by different companies will be trickier to negotiate.
