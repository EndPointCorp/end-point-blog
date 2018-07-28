---
author: Brian J. Miller
gh_issue_number: 418
tags: javascript
title: YUI Extensions and Post Initialization
---

When using YUI3’s provided extension mechanism to enhance (composite, mix in, role, whatever you like to call it) a Y.Base inherited base class, it is often helpful to have “post initialization” code run after the attributes’ values have been set. The following code provides an easy way to hook onto a Y.Base provided attribute change event to run any post initialization code easily.

<script src="https://gist.github.com/849130.js?file=gistfile1.js"></script>
