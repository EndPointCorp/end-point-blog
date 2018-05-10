---
author: Greg Davidson
gh_issue_number: 876
tags: browsers, javascript, jquery, tips
title: "IE7 “Enhances” href Attributes of Links Added via innerHTML"
---

I ran into this issue the other day while testing a new feature for a client site. The code worked well in Chrome, Firefox, Safari and IE (8-11) but it blew up in IE7. The page was fairly straightforward—​I was using jQuery and the excellent [doT.js templating library](http://olado.github.io/doT/index.html) to build up some HTML and add it to the page after the DOM had loaded. This content included several links like so: 

```html
    <a href="#panel1">More Info</a>
    <a href="#panel2">More Info</a>
    <a href="#panel3">More Info</a>
```

Each of the links pointed to their corresponding counterparts which had also been added to the page. The JavaScript code in question responded to clicks on the “More Info” links and used their href attribute as a jQuery selector:

```js
$('.my-links').on('click', function(e) {
      e.preventDefault();
      var sel = $(this).attr('href');
      ...
    });
  
```

### Links “Enhanced” By IE7

As I debugged in IE7, I determined that it was adding the fully qualified domain name to the links. Instead of “#panel2” the href attributes were set to “http://example.com/#panel2” which broke things—​especially my jQuery selectors. Fixing the issue was straightforward at this point:

```js
// fix hrefs in IE7 and 6
  if ( /^http/.test(href) ) {
    sel = sel.substr(href.indexOf('#'));
  } 
  
```

When the href attribute begins with http, discard everything before the hash (#).

### Digging Deeper

Although the problem had been solved, I was still curious as to why this was happening. While the .href property (e.g. myAnchor.href) of a link will return the entire domain in all browsers, getAttribute('href') will return only the text of the attribute. I believe the $.attr() method from jQuery is using getAttribute() behind the scenes. For modern browsers, calling $.attr() or getAttribute() worked as I was expecting.

However IE 6 and 7 had different ideas about this:

<img alt="Ie7 demo" border="0" height="355" src="/blog/2013/11/07/ie7-href-attributes-of-links-added-via/image-0.png" title="ie7-demo.png" width="550"/> 

Notice that the fully qualified domain name is prepended to the href attribute in the first example.

When links are added to the page *via innerHTML*, IE includes/prepends the full URL. However, when links are added to the page via the createElement function they remain unscathed.

The following screenshot demonstrates how Chrome and other modern browsers handle the same code:

<img alt="Chrome demo" border="0" height="385" src="/blog/2013/11/07/ie7-href-attributes-of-links-added-via/image-1.png" title="chrome-demo.png" width="550"/>

These browsers happily leave the href attributes alone :)

You learn something new every day!
