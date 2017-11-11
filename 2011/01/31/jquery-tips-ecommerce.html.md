---
author: Steph Skardal
gh_issue_number: 401
tags: ecommerce, javascript, jquery, performance
title: jQuery Tips and an Ecommerce Demo
---

I've recently been jumping back and forth between YUI and jQuery on several different client projects. I prefer working with jQuery, but whenever I work with another framework, I realize what's out there and how I should continue to improve my skills in my preferred framework. I read up on jQuery tips and put together a summary of common tips I need to follow more explained here in an ecommerce demo.

### The Setup

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<p>Before we get started, some notes on the ecommerce demo and performance testing:</p>
<ul>
<li>The fake product images come from <a href="http://dryicons.com">DryIcons</a></li>
<li>A <a href="https://github.com/stephskardal/jquerytips/blob/master/public/products.js">JSON array contains product information</a> (price, image, and title).</li>
<li>The code runs on a quick and dirty sinatra app.</li>
<li>console.time(‘task’) and console.timeEnd(‘task’) are used to debug task runtime for performance measurement</li>
<li>The performance numbers provided in the article were measured in Chrome (Ubuntu) where the average of 10 tests is reported. In all the tests, an additional for loop was added as part of the test to see measurable performance differences. See the notes at the bottom of the article on performance differences between Chrome and Firefox.</li>
</ul>
</td>
<td align="center" valign="top">
<a href="/blog/2011/01/31/jquery-tips-ecommerce/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5567773008183125922" src="/blog/2011/01/31/jquery-tips-ecommerce/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 317px;"/></a>
A screenshot from the demo app.
</td>
</tr>
</tbody></table>

**1.** The first tip I came across was a recommendation to use a for loop instead of jQuery's each method. I start off with some un-optimized code to test that loops through our products JSON object and renders the images to the page. In this case, the use of the for loop instead of each doesn't give us a significant performance difference.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<pre class="brush:jscript">
for(var k=0;k&lt;10;k++) {
  $('div.products').html('');
  console.time('test ' + k);
  for(var j=0;j&lt;10;j++) {
    $.each(products, function(index, e) {
      var ihtml = $('div.products').html();
      ihtml += '&lt;a href="#"&gt;'
        + '&lt;img class="product" src="/images/'
        + e.image + '" /&gt;&lt;/a&gt;';
      $('div.products').html(ihtml);
    });
  }
  console.timeEnd('test ' + k);
}
</pre>
</td>
<td valign="top">
<pre class="brush:jscript">
for(var k=0;k&lt;10;k++) {
  $('div.products').html('');
  console.time('test ' + k);
  for(var j=0;j&lt;10;j++) {
    for(var i=0;i&lt;products.length; i++) {
      var ihtml = $('div.products').html();
      ihtml += '&lt;a href="#"&gt;'
        + '&lt;img class="product" src="/images/'
        + products[i].image + '" /&gt;&lt;/a&gt;';
      $('div.products').html(ihtml);
    }
  }
  console.timeEnd('test ' + k);
}
</pre>
</td>
</tr>
<tr>
<td valign="top">
10 tests average: 505ms
</td>
<td valign="top">
10 tests average: 515ms
</td>
</tr>
</tbody></table>

<a href="/blog/2011/01/31/jquery-tips-ecommerce/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5567850235750329490" src="/blog/2011/01/31/jquery-tips-ecommerce/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 282px;"/></a>

Products displayed with a for loop instead of jQuery's each method.

**2.** The next "I Can't Believe I'm Not Using this jQuery Technique" I found was a recommendation to use data tag. Although I've read about the data tag, I haven't worked with it enough to use it consistently. With this code, we assign product data (name, price) to each product link as it’s added to the DOM. Upon clicking a product, instead of traversing through the products array, we render the "featured_product" contents based on it's data. The data tag is recommended over assigning values to arbitrary HTML tag attributes such as assigning our product <a> and <img> the name and price values to title or alt attributes.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr><td valign="top">
<pre class="brush:jscript">
for(var i=0;i&lt;products.length; i++) {
  var link = $(document.createElement('a'))
    .attr(‘href’, ‘#’)
    .html('&lt;img class="product" src="/images/' + products[i].image + '" /&gt;')
    .data('name', products[i].name)
    .data('price', products[i].price);
  if(products[i].featured) {
    link.addClass('featured');
  }
  if(products[i].sale) {
    link.addClass('sale');
  }
  $('div.products').append(link);
};
$('div.products a').click(function() {
   $('div.featured_product')
    .html('&lt;h1&gt;' + $(this).data('name') + '&lt;/h1&gt;');
  $(this).find('img').clone().appendTo('.featured_product');
});
</pre>
</td></tr>
</tbody></table>

<a href="/blog/2011/01/31/jquery-tips-ecommerce/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5567850235768483282" src="/blog/2011/01/31/jquery-tips-ecommerce/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 302px;"/></a>

jQuery's data tag is used to populate the right side of the page as a product is clicked.

**3.** The next tip I came across frequently was a recommendation to cache your selectors, shown in the example below. A selector $('div.products a.featured') is created and used when users like to view "Featured" Items. This gave me a 33% performance gain.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<pre class="brush:jscript">
$('a.featured').click(function() {
  for(var k=0;k&lt;10; k++) {
    console.time('test ' + k);
    for(var j=0;j&lt;100;j++) {
      $('div.products a').css('background', '#FFF');
      $('div.products a.featured').css('background', '#999');
    }
    console.timeEnd('test ' + k);
  }
});
</pre>
</td>
<td valign="top">
<pre class="brush:jscript">
var all_products = $('div.products a');
var featured_products = $('div.products a.featured');
$('a.featured').click(function() {
  for(var k=0;k&lt;10; k++) {
    console.time('test ' + k);
    for(var j=0;j&lt;100;j++) {
      all_products.css('background', '#FFF');
      featured_products.css('background', '#999');
    }
    console.timeEnd('test ' + k);
  }
});
</pre>
</td>
</tr>
<tr>
<td valign="top">
10 tests average: 31ms
</td>
<td valign="top">
10 tests average: 21ms
</td>
</tr>
</tbody></table>

<a href="/blog/2011/01/31/jquery-tips-ecommerce/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5567850240733601346" src="/blog/2011/01/31/jquery-tips-ecommerce/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 145px; height: 400px;"/></a>

Multiple products added to test onclick for identifying "featured" products.

**4.** Another tip I came across was the recommendation on using context in jQuery selectors, described [here](”http://api.jquery.com/jQuery/#jQuery1”) in the jQuery documentation. In one example, I try updating the $('div.products') selector to set the context as $(‘div.wrapper’), but saw performance worsen here. In another example, I added "this" as a context for populating the featured product, but again saw performance worsen slightly here. In this case, performance gain will depend on your original selector, but it's worth testing.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<pre class="brush:jscript">
for(var k=0;k&lt;10;k++) {
  $('div.products').html('');
  console.time('test ' + k);
  for(var j=0;j&lt;10;j++) {
    for(var i=0;i&lt;products.length; i++) {
      ...
      $('div.products').append(link);
    }
  }
  console.timeEnd('test ' + k);
}
</pre>
</td>
<td valign="top">
<pre class="brush:jscript">
for(var k=0;k&lt;10;k++) {
  $('div.products').html('');
  console.time('test ' + k);
  for(var j=0;j&lt;10;j++) {
    for(var i=0;i&lt;products.length; i++) {
      ...
      $('div.products', $('div.wrapper')).append(link);
    }
  }
  console.timeEnd('test ' + k);
}
</pre>
</td>
</tr>
<tr>
<td valign="top">
10 tests average: 64ms
</td>
<td valign="top">
10 tests average: 76ms
</td>
</tr>
</tbody></table>

**5.** Another common tip I came across that "I can't believe I don't follow" is to use an id selector instead of a class. I’ve admittedly read this several times, but again it's a practice that I sometimes forget about. In my ecommerce setup, I add a loop to add the products 10x to our DOM, and with a change of selector from 'div.products' to 'div#products', I saw a small performance improvement.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<pre class="brush:jscript">
for(var k=0;k&lt;10;k++) {
  $('div.products').html('');
  console.time('test ' + k);
  for(var j=0;j&lt;10;j++) {
    for(var i=0;i&lt;products.length; i++) {
       ...
       $('div.products').append(link);
    }
  }
  console.timeEnd('test ' + k);
}
</pre>
</td>
<td valign="top">
<pre class="brush:jscript">
for(var k=0;k&lt;10;k++) {
  $('div.products').html('');
  console.time('test ' + k);
  for(var j=0;j&lt;10;j++) {
    for(var i=0;i&lt;products.length; i++) {
      ...
       $('div#products').append(link);
    }
  }
  console.timeEnd('test ' + k);
}
</pre>
</td>
</tr>
<tr>
<td valign="top">
10 tests average: 64ms
</td>
<td valign="top">
10 tests average: 60ms
</td>
</tr>
</tbody></table>

**6.** I found a recommendation to minimize the DOM minimally. This is a tip that I typically follow, but another one that's easily forgotten. In our ecommerce setup, I create a single point of appending to the div#products selector after generating my product links and data. This gave a ~25% performance gain.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<pre class="brush:jscript">
for(var k=0;k&lt;10;k++) {
  $('div.products').html('');
  console.time('test ' + k);
  for(var j=0;j&lt;10;j++) {
    for(var i=0;i&lt;products.length; i++) {
      ...
      $('div#products').append(link);
    }
  }
  console.timeEnd('test ' + k);
}
</pre>
</td>
<td valign="top">
<pre class="brush:jscript">
for(var k=0;k&lt;10;k++) {
  $('div#products').html();
  console.time('test ' + k);
  var collection = $(document.createElement('div'));
  for(var j=0;j&lt;10;j++) {
    for(var i=0;i&lt;products.length; i++) {
      ...
      collection.append(link);
    }
  }
  $('div#products').append(collection);
  console.timeEnd('test ' + k);
}
</pre>
</td>
</tr>
<tr>
<td>
10 tests average: 60ms
</td>
<td>
10 tests average: 45ms
</td>
</tr>
</tbody></table>

**7.** Another tip I came across was to use event delegation in jQuery. The idea is that your event has more context to work with than general selectors. You can access the event and manipulate it’s parent. I found that $(e.target).parent() is the same as manipulating $(this) performance-wise. It’s likely that using one or the other is much faster than using a general DOM selector such as $(div.product' + id).

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr><td valign="top">
<pre class="brush:jscript">
var featured_product = $('div#featured_product');
$('div#products a').click(function(e) {
  var product = $(e.target).parent();  // same as $(this)
  featured_product
    .html('&lt;h1&gt;' + product.data('name') + '&lt;/h1&gt;')
    .append(product.find('img').clone());
});
</pre>
</td></tr>
</tbody></table>

**8.** One tip that I've never seen before is to use ".end()" in chaining. Instead of reselecting the $('div.products') region, I use "find()" to apply a css style, then traverse up the chain to find another set of products to apply a css style, and repeat. This change gave a small performance bump, but you might tend to use the cached selectors described in Tip #3 instead of the following.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<pre class="brush:jscript">
$('a#special').click(function() {
  for(var k=0;k&lt;10;k++) {
    console.time('test ' + k);
    for(var j=0;j&lt;100; j++) {
      $('div#products').find('a').css('background', '#FFF');
      $('div#products').find('.featured').css('background', '#999');
      $('div#products').find('.sale').css('background', '#999');
    }
    console.timeEnd('test ' + k);
  }
});
</pre>
</td>
<td valign="top">
<pre class="brush:jscript">
$('a#special').click(function() {
  for(var k=0;k&lt;10;k++) {
    console.time('test ' + k);
    for(var j=0;j&lt;100; j++) {
      $('div#products')
      .find('a')
        .css('background', '#FFF')
      .end()
      .find('.featured')
        .css('background', '#999')
      .end()
      .find('sale')
        .css('background', '#999');
    }
    console.timeEnd('test ' + k);
  }
});
</pre>
</td>
</tr>
<tr>
<td>
10 tests average: 47ms
</td>
<td>
10 tests average: 37ms
</td>
</tr>
</tbody></table>

<a href="/blog/2011/01/31/jquery-tips-ecommerce/image-4-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5567850251111423698" src="/blog/2011/01/31/jquery-tips-ecommerce/image-4.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 316px;"/></a>

Featured and Sale products are highlighted here.

**9.** I found several examples of writing your own selectors and how easy it is! I wrote two selectors with the following to identify products under $20.00 and products over $1000.00.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr><td>
<pre class="brush:jscript">
$(function() {
   $('a#under20').click(function() {
    all_products.css('background', '#FFF');
    $('div#products a:under20').css('background', '#999');
  });
  $('a#over1000').click(function() {
    all_products.css('background', '#FFF');
    $('div#products a:over1000').css('background', '#999');
  });
});

$.extend($.expr[':'], {
  under20: function(a) {
    if($(a).data('price') &amp;&amp; $(a).data('price') &lt; 20) {
      return true;
    }
    return false;
  },
  over1000: function(a) {
    if($(a).data('price') &amp;&amp; $(a).data('price') &gt; 1000) {
      return true;
    }
    return false;
  }
});
</pre>
</td></tr>
</tbody></table>

<a href="/blog/2011/01/31/jquery-tips-ecommerce/image-5-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5567850720843374002" src="/blog/2011/01/31/jquery-tips-ecommerce/image-5.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 289px;"/></a>

Products priced over $1000 are highlighted with a custom selector.

**10.** I also found several examples of how to write your own chain methods. In this example, I create two chain methods to set the product background to white or grey and update my under20 &amp; over1000 methods to use this new chain method. The nice thing about creating your own chain methods is that these methods can be easily modified in the future with minimal code changes because it follows the DRY principle. I'm not sure if it's intended, but the use of my custom chain method did not work with the end() chain method described in Tip #8.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr><td>
<pre class="brush:jscript">
$.fn.unhighlight_product = function() {
  return $(this).css('background', '#FFF');
}
$.fn.highlght_product = function() {
  return $(this).css('background', '#999');
}

$(function() {
  $('a#under20').click(function() {
    all_products.unhighlight_product();
    $('div#products a:under20').highlight_product();
  });
  $('a#over1000').click(function() {
    all_products.unhighlight_product();
    $('div#products a:over1000').highlight_product();
  });
});
</pre>
</td></tr>
</tbody></table>

<a href="/blog/2011/01/31/jquery-tips-ecommerce/image-6-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5567850723346023426" src="/blog/2011/01/31/jquery-tips-ecommerce/image-6.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 356px; height: 285px;"/></a>

Products priced under $20 are highlighted with a custom selector and custom chain method.

Again, the product images for this demo app are from [DryIcons.com](http://dryicons.com) and the final application code can be found [here](https://github.com/stephskardal/jquerytips). The application was also deployed on [Heroku](http://heroku.com/) to verify that the code works in IE [8], Chrome, and Firefox.

### In Case You are Interested

During development of the demo, I found a significant performance differences between Chrome and Firefox. See the following tests:

- Tip #1: 6200ms (FF) vs 515ms (Chrome)
- Tip #3: 106ms (FF) vs 21ms (Chrome)
- Tip #4: 258ms (FF) vs 60ms (Chrome)
- Tip #6: 169ms (FF) vs 45ms (Chrome)
- Tip #8: 154ms (FF) vs 37ms (Chrome)

Or in visual form:

<img alt="" src="http://chart.apis.google.com/chart?chxl=0:|Tip+%231|Tip+%233|Tip+%234|Tip+%236|Tip+%238&amp;chxr=1,0,6250&amp;chxt=x,y&amp;chbh=a&amp;chs=745x300&amp;cht=bvg&amp;chco=A2C180,3D7930&amp;chds=0,6250,0,6250&amp;chd=t:6200,106,258,169,154|515,21,60,45,37&amp;chdl=Firefox+3.6|Chrome+8.0&amp;chtt=jQuery+Performance"/>
