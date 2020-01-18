---
author: Steph Skardal
gh_issue_number: 432
tags: analytics, ecommerce
title: Referral Tracking with Google Analytics
---

<a href="/blog/2011/03/25/referral-tracking-google-analytics/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5588025431694738370" src="/blog/2011/03/25/referral-tracking-google-analytics/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 98px;"/></a>

It’s pretty easy to use Google Analytics to examine referral traffic, including using custom referral tracking codes. Here’s how:

Once you have referrers or affiliates that plan to link to your site, you can ask that those affiliates append a unique tracking ID to the end of the URL. For example, I’ll use the following referral ID’s to track metrics from Milton and Roger’s websites to End Point’s site.

- http://www.endpoint.com/?ref=milton
- http://www.endpoint.com/?ref=roger

After you’ve seen some traffic build up from those affiliates, you must create two Custom Advanced Segments in Google Analytics:

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="bottom"><a href="/blog/2011/03/25/referral-tracking-google-analytics/image-1-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5588030206055790546" src="/blog/2011/03/25/referral-tracking-google-analytics/image-1.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 229px; height: 400px;"/></a>
</td>
<td valign="bottom"><a href="/blog/2011/03/25/referral-tracking-google-analytics/image-2-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5588025427517347346" src="/blog/2011/03/25/referral-tracking-google-analytics/image-2.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 192px;"/></a>
</td>
</tr>
<tr>
<td align="center" valign="top">Follow the link to create an Advanced Segment.</td>
<td align="center" valign="top">The New Advanced Segment page.</td>
</tr>
</tbody></table>

Once you’ve landed on the New Advanced Segment page, you create a custom segment by dragging “Landing Page” from the “Content” tab to define the criteria, and set it to contains your unique referral identifier.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td><a href="/blog/2011/03/25/referral-tracking-google-analytics/image-3-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5588027705314505746" src="/blog/2011/03/25/referral-tracking-google-analytics/image-3.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 289px;"/></a></td>
<td><a href="/blog/2011/03/25/referral-tracking-google-analytics/image-4-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5588027702483872770" src="/blog/2011/03/25/referral-tracking-google-analytics/image-4.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 289px;"/></a></td>
</tr>
<tr>
<td align="center">Roger’s Referral Traffic</td>
<td align="center">Milton’s Referral Traffic</td>
</tr>
</tbody></table>

That’s it! You now have custom Advanced Segments defined to track referral or affiliate data. You can select the Advanced Segments from any metrics page:

<a href="/blog/2011/03/25/referral-tracking-google-analytics/image-5-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5588034647905335026" src="/blog/2011/03/25/referral-tracking-google-analytics/image-5.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 111px;"/></a>

All traffic compared to referral traffic from Milton and Roger’s sites.

<a href="/blog/2011/03/25/referral-tracking-google-analytics/image-6-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5588028227247239538" src="/blog/2011/03/25/referral-tracking-google-analytics/image-6.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 93px;"/></a>

Traffic from Milton’s website only.

You can also examine conversion driven from the affiliate. For example, how does conversion driven by one affiliate compare to the entire site’s conversion? On our site, conversion is measured by contact form submission — but on ecommerce sites, you can measure conversion in the form of purchases relative to different affiliates.

<a href="/blog/2011/03/25/referral-tracking-google-analytics/image-7-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5588028222680855938" src="/blog/2011/03/25/referral-tracking-google-analytics/image-7.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 94px;"/></a>

Roger’s Referral conversion versus conversion of the entire site. Roger’s doing pretty good!

One potential disadvantage to this method for affiliate tracking is that you are creating duplicate content in Google by introducing additional URLs. You may want to use the [rel="canonical"](/blog/2009/12/17/content-syndication-seo-rel-canonical) tag on the homepage to minimize duplicate content in search engine indexes. A very similar alternative to this method to bypass adding a referral ID would be to create custom segments defined by Source and Referral Path, however, the method described in this article is valuable for sites that may have a redirect between the referral site and the landing URL (http://www.miltonsblog.com/ links to http://www.endpointcorp.com/?ref=milton redirects to http://www.endpoint.com/?ref=milton retains the referral information).

Google Analytics is a great tool that allows you to measure analytics such as the ones shown in this post. It’s fairly standard for our all of our clients to request Google Analytics installation. [Google announced last week](https://analytics.googleblog.com/2011/03/looking-towards-future-of-google.html) that a new Google Analytics platform will be rolled out soon, which includes a feature update to multiple segments that will allow us to examine traffic from multiple affiliates without showing “All Visits”.

Note that the data presented in this article is fictitious.
I don’t think Milton and Roger will be linking to End Point’s site any time soon!
