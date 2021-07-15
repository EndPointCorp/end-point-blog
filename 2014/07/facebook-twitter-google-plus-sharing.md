---
author: Marina Lohova
title: Facebook, Twitter, Google+ sharing with the URL
github_issue_number: 1010
tags:
- social-networks
date: 2014-07-10
---

This blog post is intended for the folks who spent way more time displaying social sharing buttons on their websites than originally planned. My buttons were supposed to bring up the Share Dialog for Facebook, Twitter and Google+ platforms. I had the requirement to display a custom logo and a custom description. It seemed easy... until it turned out to be rather difficult.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/07/facebook-twitter-google-plus-sharing/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/07/facebook-twitter-google-plus-sharing/image-0.png"/></a></div>

The appropriate format for Twitter is:

```ruby
<a href="http://twitter.com/share?text=<%= desc %>&url=<%= url %>">Twitter</a>
```

Note that Twitter dialog does not include the picture, only the description.

Trouble started with Facebook when I learned that custom parameters in Facebook’s sharer.php url are officially not supported anymore: [https://developers.facebook.com/bugs/357750474364812](https://developers.facebook.com/bugs/357750474364812). I tried the format widely suggested on forums, and while custom image was successfully displayed, neither title, not description showed.

```ruby
<a href="http://www.facebook.com/sharer.php?u=<%= url %>&p[images][0]=<%= img  %>&description=<%= desc %>">Facebook</a>
```

Facebook documentation hinted that addition of the OpenGraph Protocol standard tags to the of the page may help:

```html
<meta content="http://samples.ogp.me/136756249803614" property="og:url"/> 
<meta content="Chocolate Pecan Pie" property="og:title"/>
<meta content="This pie is delicious!" property="og:description"/> 
<meta content="https://fbcdn-dragon-a.akamaihd.net/hphotos-ak-prn1/851565_496755187057665_544240989_n.jpg" property="og:image"/> 
```

I wasn’t able to get it up and working with sharer.php. After spending considerable amount of time on this I had to give up and acknowledge that the only way to fully customize the dialog would require registering an app and utilizing APP_ID [https://developers.facebook.com/docs/sharing/reference/share-dialog](https://developers.facebook.com/docs/sharing/reference/share-dialog).

I anticipated the same kind of trouble with the last button for Google+. And I wasn’t mistaken. The only allowed format for G+ is:

```ruby
<a href="https://plus.google.com/share?url=<%= url %>">Google+</a>
```

Despite a few mentions on the web this does not work anymore:

```ruby
<meta content="<%= desc %>" itemprop="description"/>
```

Same here. Doesn’t work:

```ruby
<meta content="<%= title %>" property="og:title"/>
<meta content="article" property="og:type"/>
<meta content="<%= url %>" property="og:url"/>
<meta content="<%= img  %>" property="og:image"/>
<meta content="<%= desc %>" property="og:description"/>
```

Eventually it turned out that it wasn’t possible to use parameters for G+ link unless you sign up for the API key and use one of the API methods. I wasn’t planning to obtain a key at that time, so I had to simply drop the custom logo and text for G+.

Looks like both Facebook and Google+ took steps to restrict the free usage of their share urls so more people would register their apps with them.
