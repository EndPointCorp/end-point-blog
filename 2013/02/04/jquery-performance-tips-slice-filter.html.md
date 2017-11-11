---
author: Steph Skardal
gh_issue_number: 755
tags: javascript, jquery, rails
title: 'jQuery Performance Tips: Slice, Filter, parentsUntil'
---



I recently wrote about working with an [intensive jQuery UI interface to emulate highlighting text](http://blog.endpoint.com/2013/01/javascript-driven-interactive.html). During this work, I experimented with and worked with jQuery optimization quite a bit. In the previous blog article, I mentioned that in some cases, the number of DOM elements that I was traversing at times exceeded 44,000, which caused significant performance issues in all browsers. Here are a few things I was reminded of, or learned throughout the project. 

- console.profile, console.time, and the Chrome timeline are all tools that I used during the project to some extent. I typically used console.time the most to identify which methods were taking the most time.
- Caching elements is a valuable performance tool, as it's typically faster to run jQuery calls on a cached jQuery selector rather than reselecting the elements. Here's an example:

<table cellpadding="0" cellspacing="0" width="100%"><tbody><tr> <th align="center" width="50%">Slower</th> <th align="center" width="50%">Faster</th> </tr>
<tr> <td valign="top" width="50%"><pre class="brush:javascript">//Later in the code
$('.items').do_something();
</pre></td> <td valign="top" width="50%"><pre class="brush:javascript">//On page load
var cached_items = $('.items');
//Later in the code
cached_items.do_something();
</pre></td> </tr></tbody></table>

- The [jQuery .filter operator](http://api.jquery.com/filter/) came in handy, and gave a bit of a performance bump in some cases.

<table cellpadding="0" cellspacing="0" width="100%"><tbody><tr> <th align="center" width="50%">Slower</th> <th align="center" width="50%">Faster</th> </tr>
<tr> <td valign="top" width="50%"><pre class="brush:javascript">$('.highlighted');
</pre></td> <td valign="top" width="50%"><pre class="brush:javascript">cached_items.filter('.highlighted');
</pre></td> </tr></tbody></table>

- [jQuery slicing](http://api.jquery.com/slice/) from a cached selection was typically much faster than reselecting or selecting those elements by class. If retrieving slice boundaries is inexpensive and there are a lot of elements, slice was extremely valuable.

<table cellpadding="0" cellspacing="0" width="100%"><tbody><tr> <th align="center" width="50%">Slower</th> <th align="center" width="50%">Faster</th> </tr>
<tr> <td valign="top" width="50%"><pre class="brush:javascript">cached_items.filter('.highlighted');
</pre></td> <td valign="top" width="50%"><pre class="brush:javascript">cached_items.slice(10, 100);
</pre></td> </tr></tbody></table>

- [Storing data](http://api.jquery.com/jQuery.data/) on elements was typically a faster alternative than parsing the id from the HTML markup (class or id). If it's inexpensive to add data values to the HTML markup, this was a valuable performance tool. Note that it's important to test if the jQuery version in use automatically parses the data value to an integer.

<table cellpadding="0" cellspacing="0" width="100%"><tbody><tr> <th align="center" width="50%">Slower</th> <th align="center" width="50%">Faster</th> </tr>
<tr> <td valign="top" width="50%"><pre class="brush:javascript">//given <tt data-id="123" id="r123"></tt>
var slice_start = parseInt($('tt#r123')
                    .attr('id')
                    .replace(/^r/, ''));
</pre></td> <td valign="top" width="50%"><pre class="brush:javascript">//given <tt data-id="123" id="r123"></tt>
var slice_start = $('tt#r123')
                    .data('id');
</pre></td> </tr></tbody></table>

- [Advanced jQuery selectors](http://www.w3schools.com/jquery/jquery_ref_selectors.asp) offered performance gain as opposed to jQuery iterators. In the example below, it's faster to use selectors :has and :not combined rather than iterating through each parent.

<table cellpadding="0" cellspacing="0" width="100%"><tbody><tr> <th align="center" width="50%">Slower</th> <th align="center" width="50%">Faster</th> </tr>
<tr> <td valign="top" width="50%"><pre class="brush:javascript">$.each($('p.parent'), function(i, el) {
  //if el does not have any visible spans
  //  do_something()
});
</pre></td> <td valign="top" width="50%"><pre class="brush:javascript">$('p.parent:not(:has(span:visible))')
  .do_something();
</pre></td> </tr></tbody></table>

- The [jQuery method parentsUntil](http://api.jquery.com/parentsUntil/) was a valuable tool instead of looking at the entire document or a large set of elements. In the cases where the children were already defined in a subset selection, I  used the parentsUntil method to select all parents until a specific DOM element.

<table cellpadding="0" cellspacing="0" width="100%"><tbody><tr> <th align="center" width="50%">Slower</th> <th align="center" width="50%">Faster</th> </tr>
<tr> <td valign="top" width="50%"><pre class="brush:javascript">$('#some_div p.parent:not(:has(span:visible))')
  .do_something();
</pre></td> <td valign="top" width="50%"><pre class="brush:javascript">subset_of_items
  .parentsUntil('#some_div')
  .filter(':not(:has(span:visible))')
  .do_something();
</pre></td> </tr></tbody></table>

The best takeaway I can offer here is that it was almost always more efficient to work with as precise set of selected elements as possible, rather than reselecting from the whole document. The various methods such as filter, slice, and parentsUntil helped define the precise set of elements.


