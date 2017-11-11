---
author: Ron Phipps
gh_issue_number: 356
tags: environment, javascript, jquery, testing
title: Debugging jQuery
---



A recent reskin project for a client requires that we convert some of their old Prototype code to jQuery as well as create new jQuery code. I have not done much with converting Prototype to jQuery and I felt like my debugging tools for JavaScript were under par. So this morning I set out to find what was available for jQuery and I found this [article](http://msdn.microsoft.com/en-us/scriptjunkie/ee819093.aspx) on the subject.

I've used Firebug for some time now, but was unaware of some of the supporting plugins that would certainly help with debugging JavaScript. Some of the plugins and methods found in the article that I found immediately helpful were:

- **FireFinder**: Makes it quite easy to verify that the selector values in your code are correct and that the proper elements are returned. I was able to immediately pinpoint problems with my selectors and this brought to light why certain events were not firing.

- **Firebug Console**: Using the console.log function allowed me to check values without littering my code with alert statements.

- **FireQuery**: At a glance this plugin for Firebug shows which elements have event handlers bound to them.

- **Firebug Breakpoints**: Setting breakpoints and watch statements in your code makes it easier to see what is happening in the JavaScript code as it is executed instead of trying to figure out what happened after the code has run its course.

Thanks to the author of the [article](http://msdn.microsoft.com/en-us/scriptjunkie/ee819093.aspx), Elijah Manor, for the in-depth information on debugging jQuery code.


