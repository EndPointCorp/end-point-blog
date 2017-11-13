---
author: Jeff Boes
gh_issue_number: 620
tags: javascript, json
title: Simple Pagination with AJAX
---

Here's a common problem: you have a set of results you want to display (search results, or products in a category) and you want to paginate them in a way that doesn't submit and re-display your results page every time. AJAX is a clear winner in this; I'll outline a very simple, introductory approach for carrying this off.

(I'm assuming that the reader has some modest familiarity with JavaScript and jQuery, but no great expertise. My solutions below will tend toward the “Cargo Cult” programming model, so that you can cut and paste, tweak, and go, but with enough “how and why” sprinkled in so you will come away knowing enough to extend the solution as needed.)

Firstly, you have to have the server-side processing in place to serve up paginated results in a way you can use. We'll assume that you can write or adapt your current results source to produce this for a given URL and parameters:

```
/search?param1=123&param2=ABC&sort=colA,colB&offset=0&size=24
```

That URL offers a state-less way to retrieve a slice of results: in this case, it corresponds to a query something like:

```sql
SELECT … FROM … WHERE param1='123' AND param2='ABC'
ORDER BY colA,colB OFFSET 0 LIMIT 24
```

You can see that this will generate a slice of 0-24 results; changing “offset” will get other slices, which is the foundation of our ability to “page” the results.

The code behind “/search” should return a JSON structure suitable for your needs. My usual approach is to assemble what I want in Perl, then pass it through JSON::to_json:

```perl
my $results = perform_search(...);
my $json = JSON::to_json($results);
```

Don't forget to include an appropriate document header:

```
Content-type: application/json
```

Now we need a JavaScript function to retrieve a slice; I'll use jQuery here as it's my preferred solution (and because I'm not at all fluent in non-jQuery approaches!).

```javascript
function(){
  $.ajax({ url: '/search', data: { …, offset: $offset, limit: 24 },
…}
```

You'll need to keep track of (or calculate) the offset within your page. My approach is to drop each result into a div or similar HTML construction, then I can count them on the fly:

```javascript
var $offset = $('div.search_result').length;
```

For the “data” passed in the AJAX call above, you need to assemble your query parameters, most likely from form elements on the page. (Newbie note: you can put <input> and <select> elements in the page without a surrounding <form>, as jQuery doesn't care -- you aren't going to submit a form, but construct a URL that looks like it came from a form.) Here's one useful model to follow:

```javascript
var $data = { offset: $offset, limit: 24 };
$.each(['param1', 'param2'], function(ix, val) {
  $data[val] = $('input[name=' + val + '], select[name=' + val + ']').val();
};
```
and then:

```javascript
$.ajax({ url: '/search', data: $data, … });
```

Now we need something to handle the returned data. Within the ajax() call, we reference (or construct) a function that takes at least one argument:

```javascript
function(results) { … }
```

“results” is of course the JSON structure you built up in the “/search” response. Here, we'll assume that you are just sending back an array of objects:

```javascript
[ { col1: 'val1', col2: 'val2', col3: 'val3' }, { col1: 'val4', col2: 'val5', col3: 'val6' } ]
```
would represent two rows of three columns each. We can now process these:

```javascript
$.each(results, function(ix, val){
  var new_result = $('div.search_result').first().clone();
  $(new_result).find('span.col1').html(val.col1);
  $(new_result).find('span.col2').html(val.col2);
  $(new_result).find('span.col3').html(val.col3);
  $('div.search_result').last().append(new_result);
};
```

In place of an actual database query or search engine, I have a simple PHP program that sends back a chunk of simulated rows. A few other notes and finesses:

- In the HTML document, I have a template for the "search_result" DIV that is hidden. I can style this any way I like, then I clone it for each returned result row. Note that it's initially hidden, so after appending a new clone to the page, I have to "show()" it.

- I do some very simple arrangement of the results by inserting a hard break after every four results. You could do much fancier arrangements: assigning CSS classes based on whether the new result is at an edge of the grid, for instance.

- Error handling in this example is very rudimentary.

Here's a screenshot of what you might expect, with Firebug showing the returned JSON object.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2012/05/24/simple-pagination-with-ajax-heres/image-0.png" imageanchor="1" style="clear:left; float:left;margin-right:1em; margin-bottom:1em"><img border="0" height="233" src="/blog/2012/05/24/simple-pagination-with-ajax-heres/image-0.png" width="320"/></a></div>
