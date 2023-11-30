---
author: Jeff Boes
title: jQuery and hidden elements
github_issue_number: 487
tags:
- javascript
- jquery
date: 2011-08-16
---



Out of sight, not out of mind.

While extending some jQuery functionality on a page, I noted that a form element’s “change” handler wasn’t being invoked, which meant some of the page initialization code would be left out. So I helpfully added it:

```javascript
$('input[name=foobar]').change(...).change();
```

What I failed to contemplate was how this would impact another page, which just happened to have * some * (but not all) of the same form elements, and referenced the same JS code at page load. Specifically, my page’s sibling had:

```plain
<input name="foobar" type="hidden">
```

And of course this broke in production.

Well, that’s interesting. A change handler on a hidden form input field isn’t usually all that useful, so I figured out I really needed:

```javascript
$('input[name=foobar]').filter(':visible').change(...).change();
```

It happens that the “.filter()” step is actually *more efficient* than doing it all in one selector (“input[name=foobar]:visible”), because of some obscurities within jQuery. That little discovery was of value to an End Point co-worker, who realized she could shave a little time off a page load elsewhere, so my minor page malfunction will redeem itself.


