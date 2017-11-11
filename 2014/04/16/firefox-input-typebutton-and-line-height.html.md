---
author: Kent Krenrich
gh_issue_number: 964
tags: browsers
title: Firefox, Input (type=button), and Line-Height
---

I recently discovered a discrepancy in the way Firefox treats inputs with a line-height style defined and how other browsers handle the same styling rule. Specifically, Firefox completely ignores it.

This behavior seemed odd enough to me that I did some Googling to determine if this was recently introduced, a long standing issue, or something I was just doing wrong. I found some interesting discussions on the issue. Several of the search results used the word “bug” in the title though it appears to be more of a deliberate (though possibly outdated) “feature” instead. Along with the discussions, I also came across a couple of suggestions for a solution.

First of all, I was able to locate a simple enough explanation of what’s causing the behavior. As [Rob Glazebrook](http://www.cssnewbie.com/input-button-line-height-bug/#.UzBquPldXgI) explains:

>
> Basically, Firefox is setting the line-height to “normal” on buttons and is enforcing this decision with an !important declaration.” and, “browser-defined !important rules cannot be over-ruled by author-defined !important rules. This rule cannot be overruled by a CSS file, an inline style — anything.
>

Good news is I can stop experimenting hoping for different results.

I also located a [Bugzilla ticket](https://bugzilla.mozilla.org/show_bug.cgi?id=697451) opened in 2011 which contains some discussion on the pros and cons of allowing designers to control the line-height of input elements. The last few comments suggest that Firefox 30 may remove the !important declaration which would open up access to the styling property. At the time of this writing, Firefox version 30 appears to be in alpha.

Due to this long-standing stance by Mozilla, Twitter Bootstrap makes the recommendation to avoid using inputs with type set to button, submit, or reset. Instead, they recommend using button tags paired with the types already mentioned. Button tags are much more flexible in what styling rules are allowed to be applied and are therefore easier to get similar rendering results from the widest range of browsers.

If switching to button tags is not an option for whatever reason, another possible solution is to adjust the padding values for your input buttons. By shrinking the top padding, you can more easily fit text that needs to wrap due to a limited available width. Adjusting the top padding can better center the text on the button by preventing the first line of the text from rendering vertically dead center of the button.
