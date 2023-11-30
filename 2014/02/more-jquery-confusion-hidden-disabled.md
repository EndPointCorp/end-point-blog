---
author: Jeff Boes
title: 'More jQuery confusion: hidden, disabled fields'
github_issue_number: 931
tags:
- javascript
- jquery
date: 2014-02-24
---

As you may have read in my [earlier post](/blog/2014/01/unbalanced-html-considered-harmful-for/), I have a proclivity for stumbling into oddball bits of jQuery behavior. (Maybe it’s not just me.)

Here’s another I discovered recently. I was debugging an odd AJAX bug in a form, one of those dynamically updating form widgets in a page:

```html
 <select name="make">...</select>
 <select name="model">...</select>
```

where the first selector sends off an AJAX query to retrieve data to fill the second selector, and it in turn fires off a query to get data for the next, and so on down the line.

Squirreled away in the form was:

```html
 <input type="hidden" name="limitation" disabled="disabled" value="">
```

Supposedly, this input was filled in to restrict the query on some pages, but not all. I think the original author’s intent was to put data in here as it became available, and to toggle the field’s disabled setting when it was pertinent to limit the query. (Mostly, it was pertinent when the second or third selector was firing off its AJAX query.)

However, a recent change to the code behind this AJAX query created a bug, because the “limitation” parameter was showing up where it wasn’t wanted. The AJAX call was assembling parameters “by hand” (as opposed to the .serialize() method, and that’s where the problem lies!).

```html
<form>
<input type="hidden" name="secret" disabled="disabled" value="Sue Richards">
<input type="submit">
</form>
```

If you submit this form, the data received by the server won’t include the “secret” field. If you .serialize() it, likewise the data won’t include “secret”’s value. *But* if you build up the parameters “by hand”, e.g.,

```javascript
var data = {};
data.secret = $('input[name=secret]').val();
...
```

And that’s the bug. The short answer is:

```javascript
data.secret = $('input[name=secret]').not(':disabled').val();
```

because that will at least suppress the unwanted data from being transmitted.
