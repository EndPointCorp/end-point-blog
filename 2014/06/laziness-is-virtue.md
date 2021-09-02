---
author: Jeff Boes
title: Laziness is a virtue
github_issue_number: 1000
tags:
- css
- html
date: 2014-06-23
---



Laziness *is a [virtue](http://threevirtues.com/).* Blessed Saint Larry told me so. And yet I am of little faith ...

Here I was, banging my head on the keyboard, trying to solve a vertical alignment issue. (The following is a bit simplified for presentation here.)

```html
<td>
<ul class="floaty">
<li> Item 1</li>
<li> Item 2</li>
</ul>
<div class="sticky">
blah blah blah
</div>
</td>
```

The \<ul\> element was supposed to float to the right of the cell, and its individual \<li\> elements also floated, so that the list would fill up from right to left as more items were added:

One item:

<div style="width: 50%; height: 40px">
<ul style="list-style-type: none">
<li style="border: 1px solid white; height: 20px; text-align: center; width: 40px; float: right">1</li>
</ul>
</div>

Two items:

<div style="width: 50%; height: 40px">
<ul style="list-style-type: none">
<li style="border: 1px solid white; height: 20px; text-align: center; width: 40px; float: right">1</li>
<li style="border: 1px solid white; height: 20px; text-align: center; width: 40px; float: right">2</li>
</ul>
</div>

Three items:

<div style="width: 50%; height: 40px">
<ul style="list-style-type: none">
<li style="border: 1px solid white; height: 20px; text-align: center; width: 40px; float: right">1</li>
<li style="border: 1px solid white; height: 20px; text-align: center; width: 40px; float: right">2</li>
<li style="border: 1px solid white; height: 20px; text-align: center; width: 40px; float: right">3</li>
</ul>
</div>

<br/>

etc., while the “sticky” div was supposed to stay on the left. The challenge was when the div got too tall, or the number of list items caused it to wrap around to a new row; the vertical alignment to keep everything nice and centered is probably achievable in CSS, but I decided to be lazy:

```html
<td style="vertical-align: middle">
<div class="sticky">
blah blah blah
</div>
</td>
<td style="vertical-align: middle">
<ul class="floaty">
<li> Item 1</li>
<li> Item 2</li>
</ul>
</td>
```

Duh. Seriously. Table cells do a bang-up job of vertical alignment under the worst of conditions. And I’m already in the middle of a table, so the work here was just a matter of adding the appropriate “colspans” elsewhere to account for my column’s bifurcation.

P.S.: I love the word “bifurcate” and work it in to conversation when I can.


