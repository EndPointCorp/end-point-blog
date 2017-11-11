---
author: Steph Skardal
gh_issue_number: 410
tags: css, performance
title: A Performance Case Study
---

<table cellpadding="5" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<p>I'm a sucker for a good performance case study. So, when I came across a general request for performance improvement suggestions at <a href="http://inspiredology.com/">Inspiredology</a>, I couldn't help but experiment a bit.</p>

<p>The site runs on WordPress and is heavy on the graphics as it's a site geared towards web designers. I inquired to the site administrators about grabbing a static copy of their home page and using it for a case study on our blog. My tools of choice for optimization were <a href="http://www.webpagetest.org/">webpagetest.org</a> and <a href="http://developer.yahoo.com/yslow/">YSlow</a>.</p>
<p>Here are the results of a 4-step optimization in visual form:</p>

<table cellpadding="0" celspacing="0" width="100%">
<tbody><tr><td>
<img src="http://chart.apis.google.com/chart?chxl=0:|Step+%234|Step+%233|Step+%232|Step+%231|Original&chxr=0,0,15|1,0,15&chxt=y,t&chbh=a&chs=300x225&cht=bhg&chco=A2C180&chds=0,15&chd=t:13.412,11.957,10.561,10.243,9.212&chtt=First+Request+Load+Time+(seconds)"/>
</td><td>
<img src="http://chart.apis.google.com/chart?chxl=0:|Step+%234|Step+%233|Step+%232|Step+%231|Original&chxr=0,0,15|1,0,15&chxt=y,t&chbh=a&chs=300x225&cht=bhg&chco=A2C180&chds=0,15&chd=t:7.329,3.717,3.278,2.434,2.563&chtt=Repeat+Request+Load+Time+(seconds)"/>
</td></tr></tbody></table>

</td>
<td align="center" valign="top">
<a href="/blog/2011/02/09/performance-case-study/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5571698267043922738" src="/blog/2011/02/09/performance-case-study/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 135px; height: 400px;"/></a>
Inspiredology's complete homepage.
</td>
</tr>
</tbody></table>

The graph on the left shows the page load time in seconds for a first time view. Throughout optimization, page load time goes from 13.412 seconds to 9.212 seconds. Each step had a measurable impact. The graph on the right shows the page load time in seconds for a repeated view, and this goes from 7.329 seconds to 2.563 seconds throughout optimization. The first optimization step (CSS spriting and file combination) yielded a large performance improvement. I'm not sure why there's a slight performance decrease between step 3 and step 4.

And here's a summary of the changes involved in each step:

- Step 1


        - Addition of CSS Sprites: I [wrote about CSS Sprites](http://blog.endpoint.com/2010/09/css-sprites.html) a while back and A List Apart has an older but still relevant article on CSS Sprites [here](http://www.alistapart.com/articles/sprites). Repeating elements like navigation components, icons, and buttons are suitable for CSS sprites. Article or page-specific images are not typically suitable for CSS sprites. For Inspiredology's site, I created two sprited images - one with a large amount of navigation components, and one with some of their large background images. You can find a great tool for building CSS rules from a sprited image [here](http://www.spritebox.net/).
        - Combination of JS and CSS files, where applicable. Any JavaScript or CSS files that are included throughout the site are suitable for combination. Files that can't be combined include suckerfish JavaScript like Google Analytics or marketing service scripts.
        - Moved JavaScript requests to the bottom of the HTML. This is recommended because JavaScript requests block parallel downloading. Moving them to the bottom allows page elements to be downloaded and rendered first, followed by JavaScript loading.



- Step 2


        - Image compression with jpegtran, pngcrush, convert. I use pngcrush often. I read about jpegtran in [Yahoo's Best Practices for Speeding Up Your Web Site](http://developer.yahoo.com/performance/rules.html). I [wrote a bit about image compression](http://blog.endpoint.com/2009/12/jpeg-compression-quality-or-quantity.html) a while ago and briefly experimented with image compression using imagemagick on Inspiredology's images.



- Step 3


        - Addition of expires headers and disabling ETags: These are standard optimization suggestions. [Jon Jensen](/team/jon_jensen) wrote about using these a bit [here](http://blog.endpoint.com/2010/11/speeding-up-spree-demo-site.html) and [here](http://blog.endpoint.com/2009/10/performance-optimization-of.html).



- Step 4


        - Serving gzipped content with mod_deflate: Also a fairly standard optimization suggestion. Although, I should note I had some issues gzipping a couple of the files and since the site was in a temporary location, I didn't spend much time troubleshooting.
        - A bit more cleanup of rogue html and CSS files. In particular, there was one HTML file requested that didn't have any content in it and another that had JavaScript that I appended to the combined JavaScript file (combined.js).




A side-by-side comparison of webpagetest.org's original versus step 4 results highlights the reduction of requests in the waterfall and the large reduction in requests on the repeat view:

<table width="100%">
<tbody><tr>
<td valign="top">
<a href="/blog/2011/02/09/performance-case-study/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5571698261206853250" src="/blog/2011/02/09/performance-case-study/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 318px; height: 400px;"/></a>
</td>
<td valign="top">
<a href="/blog/2011/02/09/performance-case-study/image-4-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5571698261191315554" src="/blog/2011/02/09/performance-case-study/image-4.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 365px;"/></a>
</td>
</tr>
</tbody></table>

### What Next?

At this point, [webpagetest.org](http://www.webpagetest.org/) suggests the following changes:

- Gzipping the remaining components has a potential of reducing total bytes of the first request by ~10%.
- Additional image compression has the potential of reducing total bytes of the first request by about ~6%. This metric is based on their image compression check: "JPEG - Within 10% of a photoshop quality 50 will pass, up to 50% larger will warn and anything larger than that will fail." Quite a few of Inspiredology's jpgs did not pass this test and could be optimized further.
- Use a CDN. This is a common optimization suggestion, but the cost of a CDN isn't always justified for smaller sites.

I would suggest:

- Revisiting CSS spriting to further optimize. I only spent a short time spriting and didn't work out all the kinks. There were a few requests that I didn't sprite because they were repeating elements, but repeating elements can be sprited together. Another 5 requests might be eliminated with additional CSS spriting.
- Server-optimization: Inspiredology runs on WordPress. We've used the [wp-cache](http://wordpress.org/extend/plugins/wp-cache/) plugin for a couple of our clients running WordPress, which I believe helps. But note that the case study presented here is a static page with static assets, so there is obviously a huge gain to be had by optimizing serving images, CSS, and JavaScript.
- Database optimization: Again, there's no database in play in this static page experiment. But there's always room for improvement on database optimization. [Josh Tolley](/team/josh_tolley) recently made performance improvements for one of our clients running on Rails with postgreSQL using [pgsi](http://bucardo.org/wiki/Pgsi), our open source postgreSQL performance reporting tool, and had outrageously impressive benchmarked improvements.
- I just read an article about CSS selectors. The combined.css file I created for this case study has 2000 lines. Although there might be only a small win with optimization here, surely optimization and cleanup of that file can be beneficial.
- I recently wrote about several [jQuery tips](http://blog.endpoint.com/2011/01/jquery-tips-ecommerce.html), including performance optimization techniques. This isn't going to improve the serving of static assets, but it would be another customer-facing enhancement that can improve the usability of the site.

I highly recommend reading [Yahoo's Best Practices on Speeding Up Your Web Site](http://developer.yahoo.com/performance/rules.html). They have a great summary of performance recommendations, covering the topics described in this article and lots more.


