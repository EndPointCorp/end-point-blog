---
author: Jeff Boes
gh_issue_number: 915
tags: javascript, jquery
title: Unbalanced HTML considered harmful for jQuery
---



This isn't earth-shattering news, but it's one of those things that someone new to jQuery might trip over so I thought I'd share.

I had a bad experience recently adding jQuery to an existing page that had less than stellar HTML construction, and I didn't have time nor budget to clean up the HTML before starting work. Thus, I was working with something much more complex than, but equally broken as what follows:

```xml
&lt;table&gt;&lt;tr&gt;&lt;td&gt;
&lt;form&gt;
&lt;/td&gt;&lt;/tr&gt;
&lt;tr&gt;&lt;td&gt;
&lt;input type="text"&gt;
&lt;/form&gt;
&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;
```

The jQuery I added did something like this:

```javascript
$('form input').css('background-color: red');
```

and of course, I was quite puzzled when it didn't work. The pitfall here is that jQuery may or may not be able to handle misconstructed or unbalanced HTML, at least not as well as your average browser, which will shift things around internally until something makes sense to it. The minimal solution is to move the opening and closing "form" tags outside the table.

