---
author: Spencer Christensen
gh_issue_number: 920
tags: browsers, html
title: HTML Doctypes Make A Difference
---



If you are like me you may not have given much thought to an HTML doctype other than "yes, it needs to be there" and "there are a few different types, but I don't really understand the differences between them."  Well if you are like me then you also recently discovered why doctypes matter and how they actually affect your web page.

For those that are not familiar with an HTML doctype, they are the very first line of an HTML document and look like this:

```
&lt;!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" 
  "http://www.w3.org/TR/html4/strict.dtd"&gt;
```

As I mentioned before, there are a few different document types.  The reason for this is because each one corresponds to a different rule set of HTML syntax for the web browser to follow, like: HTML 4.0, HTML 4.01, XHTML 1.0, or XHTML 1.1.

*"The HTML syntax requires a doctype to be specified to ensure that the browser renders the page in standards mode. The doctype has no other purpose."* [[1](http://www.w3.org/TR/html5-diff/#doctype)]

When you specify an official doctype, your web browser should follow the standard behavior for rendering that specific rule set for the given HTML syntax.  Thus you should get expected results when it renders your web page.  There are official doctypes defined by the [W3C](http://www.w3c.org) for both "strict" and "transitional" rule sets.  A "strict" document type adheres strictly to the specification for that syntax, and any legacy or not supported tags found in your document will cause rendering problems.  A "transitional" document follows the specification for the given syntax, but also allows for legacy tags to exist in the document.  They also define "frameset" doctypes which are transitional documents that also allow for frame related tags.

The doctype for HTML 5 is a lot simpler and shorter than other doctypes, and may look like this:

```
&lt;!DOCTYPE html&gt;
```

When you declare an unofficial doctype, the browser will not know which tag syntax rule set to use and will not render the page in a standard way.  This is called quirks mode, and the browser basically regresses to an older rules engine to support all legacy tags it knows about and attempts to handle it.  This also means that your web page may not render or behave as expected, especially if you use newer tags or features in your document.

Besides the HTML tag syntax, JavaScript is also affected by the doctype- since it is tied to the DOM engine being used by the browser rendering the page.  For example, in an strict doctype you will have the native JSON parser object available, but in quirks mode it may not even exist and calls to JSON.parse() or JSON.stringify() could fail.

If you are not sure you are using an official doctype, or if you are using tags that are not supported by the doctype that you are using, then you can check with [http://validator.w3.org/](http://validator.w3.org/) and validate your page.  The whole point is to get your web page to render and behave as you expect it, providing a better experience for you and your users.


