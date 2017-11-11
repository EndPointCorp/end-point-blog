---
author: Steph Skardal
gh_issue_number: 415
tags: ecommerce, social-networks
title: Ecommerce Facebook Integration Tips
---



Over the past couple of months, I've done quite a bit of Facebook integration work for several clients. All of the clients have ecommerce sites and they share the common goal to improve site traffic and conversion with successful Facebook campaigns. I've put together a brief summary of my recent experience.

First, here are several examples of Facebook integration methods I used:

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr style="background:#DDE4DF;">
<th>
Name & Notes
</th>
<th>
Screenshot Examples
</th>
</tr>
<tr>
<td valign="top">
<b>Link to Facebook Page</b>: This is the easiest integration option. It just requires a link to a Facebook fan page be added to the site.
</td>
<td align="center" style="padding-bottom:30px;" valign="top">
<a href="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5577719060009011122" src="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 199px; height: 71px;"/></a>A link to <a href="http://lotstolivefor.com/">Lots To Live For's</a> Facebook page was added to the header.
</td>
</tr>
<tr style="background:#DDE4DF;">
<td valign="top">
<b>Facebook Like Button</b>: Implementation of the like button is more advanced than a simple link. Technical details on implementation are discussed below. This was integrated on multiple product page templates. The "like" event and page shows up on the user's wall.
</td>
<td align="center" style="padding-bottom:30px;" valign="top">
<a href="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5577716422165234146" src="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 149px;"/></a>Like button's were added throughout <a href="http://www.paper-source.com/">Paper Source's</a> site. The screenshot shown above indicates I've liked this product page.<br/><br/>
<a href="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5577716422635502162" src="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 146px;"/></a>"Liking" a product page shows up on my facebook wall.
</td>
</tr>
<tr>
<td valign="top">
<b>Facebook Like Box</b>: Another example of Facebook integration is adding a "Like Box". Acting on the Like Box results in liking the actual Facebook fan page. For example, I added a Like Box to Paper Source's footer. When a user clicks on it, they are Liking Paper Source's Facebook page and will begin to receive updates from Paper Source's Facebook page on their wall.
</td>
<td align="center" style="padding-bottom:30px;" valign="top">
<a href="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5577716667071246818" src="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 255px; height: 77px;"/></a>The Facebook Like Box was added to <a href="http://www.paper-source.com/">Paper Source's</a> footer.<br/><br/>
<a href="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-4-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5577716660317385122" src="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-4.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 198px;"/></a>Clicking on the Like Box is equivalent to liking the Paper Source fan page, shown here.
</td>
</tr>

<tr style="background:#DDE4DF;">
<td valign="top">
<b>Sharer</b>: The final example of Facebook integration I implemented for a client was adding "sharer" functionality. This is accomplished by adding a link to "http://www.facebook.com/sharer.php?u=" followed by the URI encoded URL. The user is directed to Facebook and allowed to enter an additional comment and select a thumbnail. This is sent to the user's facebook wall and will be seen in the user's friends news feeds.
</td>
<td align="center" style="padding-bottom:30px;" valign="top">
<a href="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-5-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5577716896731565778" src="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-5.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 263px; height: 48px;"/></a>A Facebook share link is displayed for one of our Spree clients.<br/><br/>
<a href="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-6-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5577716895673012946" src="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-6.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 142px;"/></a>When you share an item, you are brought to a page much like the page shown in this screenshot to add a comment or select the thumbnail.<br/><br/>
<a href="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-7-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5577716895852330578" src="/blog/2011/02/23/ecommerce-facebook-integration-tips/image-7.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 148px;"/></a>Two of my Facebook friends shared the same article. I saw this on my News Feed.
</td>
</tr>
</tbody></table>

In addition to the like button and like box, there are several other types of Facebook plugins including an Activity Feed, Recommendations, Login Button, Facepile, Live Stream, and Comments. Facebook's documentation on Plugins can be found [here](http://developers.facebook.com/docs/plugins/).

### Plugin Integration: iframe versus xfbml

I've used iframe integration for the majority of clients and most recently used xfbml for Paper Source. Implementation with an iframe might be easier and require less templates to be modified. Implementation with xfbml provides more flexibility, claims to have more advanced reporting, and allows you to add event listeners to various actions. Here's a code comparison of equivalent functionality for the two options:

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr>
<th width="50%">
iframe
</th>
<th>
xfbml
</th>
</tr>
<tr>
<td valign="top">
<pre class="brush:plain">
<iframe
src="http://www.facebook.com/plugins/like.php
?href=<%= URI.encode(request.url) %>
&layout=button_count"
scrolling="no" frameborder="0"
style="border:none;overflow:hidden;
width:90px;height:21px;"
allowTransparency="true">
</iframe>
</pre>
</td>
<td valign="top">
<pre class="brush:plain">
<p><fb:like layout="button_count"></fb:like></p>
<div id="fb-root"></div>
<script>
var fb_rendered = false;
window.fbAsyncInit = function() {
    FB.init({appId: '*appid*',
      status: true,
      cookie: true,
      xfbml: true});
};
(function() {
    var e = document.createElement('script');
    e.type = 'text/javascript';
    e.src = document.location.protocol +
      '//connect.facebook.net/en_US/all.js';
    e.async = true;
    document.getElementById('fb-root').appendChild(e);
}());
</script>
</pre>
</td>
</tr>
</tbody></table>

### Gotchas

Throughout development, I've learned a few gotchas:

- Styling on the Facebook elements is not always easily adjustable. In some cases, the iframe or xfbml element had undesirable styling and the styling of the wrapper div may need to be adjusted to achieve desired results.
- Facebook crawls or scrapes the "Liked" pages to retrieve page information such as a title, description and thumbnail. Facebook follows rel=canonical URLs to retrieve this information - so it's important that these canonical URLs are correct. A couple of Paper Source's product page templates added an extra forward slash to the URL, and these were followed by Facebook's crawler, resulting in an infinite redirect loop of URLs with additional forward slashes. The result is that Facebook can not scrape the URL and the like button has a flickering effect when clicked.
- Facebook's crawler caches pages. If there is an error such as the canonical error listed above, it's recommended to wait 24 hours to test until the page has been re-crawled.

 xmlns, firewall issues 
