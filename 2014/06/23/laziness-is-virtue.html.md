---
author: Jeff Boes
gh_issue_number: 1000
tags: css, html
title: Laziness is a virtue
---



Laziness *is a [virtue](http://threevirtues.com/).* Blessed Saint Larry told me so. And yet I am of little faith ...

Here I was, banging my head on the keyboard, trying to solve a vertical alignment issue. (The following is a bit simplified for presentation here.)

```html
&lt;td&gt;
&lt;ul class="floaty"&gt;
&lt;li&gt; Item 1&lt;/li&gt;
&lt;li&gt; Item 2&lt;/li&gt;
&lt;/ul&gt;
&lt;div class="sticky"&gt;
blah blah blah
&lt;/div&gt;
&lt;/td&gt;
```

The <ul> element was supposed to float to the right of the cell, and its individual <li> elements also floated, so that the list would fill up from right to left as more items were added:

One item:

- 1

Two items:

- 1
- 2

Three items:

- 1
- 2
- 3

etc., while the "sticky" div was supposed to stay on the left. The challenge was when the div got too tall, or the number of list items caused it to wrap around to a new row; the vertical alignment to keep everything nice and centered is probably achievable in CSS, but I decided to be lazy:

```html
&lt;td style="vertical-align: middle"&gt;
&lt;div class="sticky"&gt;
blah blah blah
&lt;/div&gt;
&lt;/td&gt;
&lt;td style="vertical-align: middle"&gt;
&lt;ul class="floaty"&gt;
&lt;li&gt; Item 1&lt;/li&gt;
&lt;li&gt; Item 2&lt;/li&gt;
&lt;/ul&gt;
&lt;/td&gt;
```

Duh. Seriously. Table cells do a bang-up job of vertical alignment under the worst of conditions. And I'm already in the middle of a table, so the work here was just a matter of adding the appropriate "colspans" elsewhere to account for my column's bifurcation.

P.S.: I love the word "bifurcate" and work it in to conversation when I can.


