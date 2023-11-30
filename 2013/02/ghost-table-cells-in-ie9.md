---
author: Greg Davidson
title: Ghost Table Cells in IE9
github_issue_number: 758
tags:
- browsers
- css
- javascript
- jquery
date: 2013-02-08
---

### What’s this about ghosts?

I recently came across an arcane layout issue in my work on a redesigned client site. The problem was specific to Internet Explorer 9 (IE9). The related CSS styles had been well tested and rendered consistently across a variety of browsers including IE7 and 8. Everything was fine and dandy until some new content was introduced into the page for a "Quickview" feature. While all of the other browsers continued to behave and render the page correctly, the layout would break in random and confusing ways in IE9.

The following screenshots compare the correct layout with an example of the broken layout in IE9.

### Correct grid layout:

<img alt="Correct grid" border="0" height="323" src="/blog/2013/02/ghost-table-cells-in-ie9/image-0.png" title="correct-grid.png" />

### Broken layout in IE9:

<img alt="IE9 ghost cells" border="0" height="325" src="/blog/2013/02/ghost-table-cells-in-ie9/image-1.png" title="IE9-ghost-cells.png" />

### The Stage

The following is a list of the factors at work on the page in question:

- Internet Explorer 9
- Browser mode: IE9, Document mode: IE9 standards
- Some content manipulation performed via JavaScript (and jQuery in this case)
- Lots of table cells

### Debugging

The page included a list of products. The first “page” of twelve results was shown initially while JavaScript split the rest of the list into several additional pages. Once this JavaScript pagination function was complete, users could cycle through products in bite-sized pieces.

My first thought was that the issue may be related to CSS or JavaScript. I tested and debugged the styles thoroughly, tweaked styles and edited the underlying HTML structure to see if that might resolve the problem. I also tested the JavaScript and compared the original HTML with the parts which had been paginated via JavaScript. No dice.

When changes improved the paginated HTML, the bug appeared in the initial HTML. Other changes resolved the issue in the original HTML but it appeared in the paginated HTML.

I inspected the table with the Chrome Developer Tools console and also with the Developer Tools in IE9. There did not appear to be any differences between the rows which rendered properly and those which were skewed.

### Bugging Out

At this point I began to research the issue and discovered it was a bug in the IE9 browser. A Microsoft forum post described the issue and included responses from Microsoft stating that it will not be fixed. It also included a sample application which demonstrated the issue. I tested and verified that the problem has been addressed and fixed in Internet Explorer 10, thankfully.

This explained the many, seemingly random ways I had seen the grid break. At times the cells were squished and pushed to the left. This was because the ghost cell had been added at the end of a row. Other times the cells were shifted to the right (as seen in the screenshot above). In this case, the ghost cell had been added to the middle of a row.

### The Fix

Further digging revealed the the issue was related to whitespace between table cells. The solution was fairly simple: use a regular expression to remove all whitespace between the table elements:

```javascript
$('#problem-table').html(function(i, el) {
  return el.replace(/>\s+</g, '><');
});
```

With all of the whitespace removed from the affected `<table>`, IE9 rendered the page correctly.
