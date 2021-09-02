---
author: Steph Skardal
title: 'Cross Browser Development: A Few CSS and JS Issues'
github_issue_number: 373
tags:
- browsers
- css
- javascript
date: 2010-10-20
---

Coding cross browser friendly JavaScript and CSS got you down? In a recent project, [Ron](/team/ron-phipps), [David](/blog/authors/david-christensen), and I worked through some painful cross browser issues. Ron noted that he **even** banged his head against the wall over a couple of them :) Three of these issues come up frequently in my other projects full of CSS and JS development, so I wanted to share.

### Variable Declaration in JS

In several cases, I noticed that excluding variable declaration (“var”) resulted in broken JavaScript-based functionality in IE only. I typically include variable declaration when I’m writing JavaScript. In our project, we were working with legacy code and conflicting variable names may have be introduced, resulting in broken functionality. Examples of before and after:

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr>
<th>Bad</th>
<th>Better</th>
</tr>
<tr>
<td valign="top">
<pre class="brush:jscript">
var display_cart_popup = function() {
    popup_id = '#addNewCartbox';
    left = (parseInt($(window).width()) - 772) / 2;
    ...
};
</pre>
</td>
<td valign="top">
<pre class="brush:jscript">
var display_cart_popup = function() {
    var popup_id = '#addNewCartbox';
    var left = (parseInt($(window).width()) - 772) / 2;
    ...
};
</pre>
</td>
</tr>
<tr>
<td valign="top">
<pre class="brush:jscript">
...
address_display = '';

country = $(type+'_country').value;
address = $(type+'_address').value;
address2 = $(type+'_address2').value;
city = $(type+'_city').value;
state = $(type+'_state').value;
zip = $(type+'_zip').value;
...
</pre>
</td>
<td valign="top">
<pre class="brush:jscript">
...
var address_display = '';

var country = $(type+'_country').value;
var address = $(type+'_address').value;
var address2 = $(type+'_address2').value;
var city = $(type+'_city').value;
var state = $(type+'_state').value;
var zip = $(type+'_zip').value;
...
</pre>
</td>
</tr>
</tbody></table>

I researched this to gain more insight, but I didn’t find much except a reiteration that when you create variables without the “var” declaration, they become global variables which may have resulted in conflicts. However, all the “learning JavaScript” documentation I browsed through includes variable declaration and there’s no reason to leave it out for these lexically scoped variables.

### Trailing Commas in JSON objects

According to JSON specifications, trailing commas are not permitted (e.g obj = { "1" : 2, }). From my experience, JSON objects with trailing commas might work in Firefox and WebKit browsers, but it dies silently in IE. Some recent examples:

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr>
<th>Bad</th>
<th>Better</th>
</tr>
<tr>
<td valign="top">
<p>
//JSON response from an ajax call<br/>
// if $add_taxes is not true, the carttotal element will be the last element of the list and it will end with a comma
</p>
<pre class="brush:jscript">
{
  "response_message"    : '<?= $response_message ?>',
  "subtotal"            : <?= $subtotal ?>,
  "shipping_cost"       : <?= $shipping ?>,
  "carttotal"           : <?= $carttotal ?>,
<?php if($add_taxes) { ?>
  "taxes"               : <?= $taxes ?>
<?php } ?>
}
</pre>
</td>
<td valign="top">
<p>
//JSON response from an ajax call<br/>
//No matter the value of $add_taxes, the carttotal element is the last element and it does not end in a comma
</p>
<pre class="brush:jscript">
{
  "response_message"    : '<?= $response_message ?>',
  "subtotal"            : <?= $subtotal ?>,
  "shipping_cost"       : <?= $shipping ?>,
<?php if($add_taxes) { ?>
  "taxes"               : <?= $taxes ?>,
<?php } ?>
  "carttotal"           : <?= $carttotal ?>
}
</pre>
</td>
</tr>
<tr>
<td valign="top">
<p>
//Page load JSON object defined<br/>
//Last element in array will end in a comma</p>
<pre class="brush:plain">
var fonts = {
[loop list=`$Scratch->{fonts}`]
    '[loop-param name]' : {
      'bold' : "[loop-param bold]",
      'italic' : "[loop-param italic]"
    },[/loop]
};
</pre>
</td>
<td valign="top">
<p>
//Page load JSON object defined<br/>
//A dummy object is appended to the fonts JSON object<br/>
//Additional logic is added elsewhere to determine if the object is a "dummy" or not
</p>
<pre class="brush:plain">
var fonts = {
[loop list=`$Scratch->{fonts}`]
    '[loop-param name]' : {
      'bold' : "[loop-param bold]",
      'italic' : "[loop-param italic]"
     },[/loop]
    'dummy' : {}
};
</pre>
</td>
</tr>
</tbody></table>

Additional solutions to avoid the trailing comma include using join (Perl, Ruby) or implode (PHP), conditionally excluding the comma on the last element of the array, or using library methods to serialize data to JSON.

### Floating Elements in IE

Often times, you’ll get a design like the one shown below. There will be a static width and repeating components to span the entire width. You may programmatically determine how many repeating elements will be displayed, but using CSS floating elements yields the cleanest code.

<a href="/blog/2010/10/cross-browser-css-js-issues/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5530221714317774530" src="/blog/2010/10/cross-browser-css-js-issues/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 122px;"/></a>

Example of a given design with repeating elements to span a static width.

You start working in Chrome or Firefox and apply the following CSS rules:

<a href="/blog/2010/10/cross-browser-css-js-issues/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5530221724836477618" src="/blog/2010/10/cross-browser-css-js-issues/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 122px;"/></a>

CSS rules for repeating floating elements.

When you think you’re finished, you load the page in IE and see the following. Bummer!

<a href="/blog/2010/10/cross-browser-css-js-issues/image-2-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5530221714104026050" src="/blog/2010/10/cross-browser-css-js-issues/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 157px;"/></a>

Floating elements wrap incorrectly in IE.

This is a pretty common scenario. In IE, if the combined widths of consecutive floating elements is greater than or equal to 100% of the available width, the latter floating element will jump down based on the IE float model. Instead of using floating elements, you might consider using tables or CSS position rules, but my preference is to use tables only for elements that need vertical align settings and to stay away from absolute positioning completely. And I try to stay away from absolute positioning in general.

The simplest and minimalist change I’ve found to work can be described in a few steps. Let’s say your floating elements are <div>’s inside a <div> with an id of “products”:

```nohighlight
<div id="products">
  <div class="product">product 1</div>
  <div class="product">product 2</div>
  <div class="product" class="last">product 3</div>
  <div class="product">product 4</div>
  <div class="product">product 5</div>
  <div class="product" class="last">product 6</div>
</div>
```

And let’s assume we have the following CSS:

```css
<style>
div#products { width: 960px; }
div.product { float: left; width: 310px; margin-right: 15px; height: 100px; }
div.last { margin-right: 0px; }
</style>
```

Complete these steps:

- First, add another div to wrap around the #products div, with an id of “outer_products”
- Next, update the 'div#products' width to be greater than 960 pixels by several pixels.
- Next, add a style rule for 'div#outer_products' to have a width of “960px” and overflow equal to “hidden”.

Yielding:

```nohighlight
<div id="outer_products">
  <div id="products">
    <div class="product">product 1</div>
    <div class="product">product 2</div>
    <div class="product" class="last">product 3</div>
    <div class="product">product 4</div>
    <div class="product">product 5</div>
    <div class="product" class="last">product 6</div>
  </div>
</div>
```

And:

```css
<style>
div#outer_products { width: 960px; overflow: hidden; }
div#products { width: 980px; }
div.product { float: left; width: 310px; margin-right: 15px; height: 100px; }
div.last { margin-right: 0px; }
</style>
```

The solution is essentially creating a “display window” (outer_products), where overflow is hidden, but the contents are allowed to span a greater width in the inside <div> (products).

<a href="/blog/2010/10/cross-browser-css-js-issues/image-3-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5530221720067114994" src="/blog/2010/10/cross-browser-css-js-issues/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 113px;"/></a>

The white border outlines the outer_products “display window”.

Some other issues that I see less frequently include [the double-margin IE6 bug](http://www.positioniseverything.net/explorer/floatIndent.html), [chaining CSS in IE](http://www.ryanbrill.com/archives/multiple-classes-in-ie/), and [using '#' vs. 'javascript:void(0);'](https://stackoverflow.com/questions/134845/which-href-value-should-i-use-for-javascript-links-or-javascriptvoid0).
