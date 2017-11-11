---
author: Carl Bailey
gh_issue_number: 563
tags: ajax, jquery
title: 'jQuery Async AJAX: Interrupts IE, not Firefox, Chrome, Safari'
---



I recently worked on a job for a client who uses ThickBox ([http://jquery.com/demo/thickbox/](http://jquery.com/demo/thickbox/)).   Now, ThickBox is no longer maintained, but the client has used it for a while, and, "if it ain't broke don't fix it," seems to apply.  Anyway, the client needed to perform address verification checks through Ajax calls to a web-service when a form is submitted. Since the service sometimes takes a little while to respond,  the client wanted to display a ThickBox, warning the user of the ongoing checks, then, depending on the result, either continue to the next page, or allow the user to change their address.

Since the user has submitted the form and is now waiting for the next page, I chose to have jQuery call the web service with the async=false option of the ajax() function.  (Not the best  choice, looking back).   Everything worked well: Firefox, Safari and Chrome all worked as expected, and then we tested in IE. Internet Explorer would not pop up the initial ThickBox ('pleaseWait' below), until the Ajax queries had completed,  unless I put an alert in place between them, then the ThickBox would appear as intended.

```javascript
function myFunc(theForm) {
    ...
    tb_show("Please wait.','#TB_inline?
    height=50&amp;width=200#inlineID=pleaseWait&amp;modal=true");
    ...
    $.ajax({
        type : "POST",
        url:  "call to webservice",
        data:   "address to post to the webservice",
        async:  false,
        success:  function (msg) {
            ...
        }
    });
};
```

To make a long story a bit shorter, we finally determined that the culprit was the async setting in the JQuery ajax call. Making the Ajax call in synchronous mode, locked the browser and delayed the display of the ThickBox, even though the tb_show call preceded the ajax call!   Setting the async value to true solved the locking problem, and worked fine in all browsers.

The jQuery Documentation states: "Note that synchronous requests may temporarily lock the browser, disabling any actions while the request is active," which turns out to be true (at least for IE).  What surprised me was , in this case, the ThickBox call was requested well before the jQuery AJAX call.   This makes me think that maybe tb_show is triggered asynchronously in IE.  In any case it is different here than in the other mainstream browsers, and it gets locked up by the synchronous Ajax.

I worked around the problem by setting the Ajax calls to be asynchronous, then keeping track to make sure both the shipping address and the billing address checks have returned before continuing.

The lessons here are:

(1) Be careful using synchronous mode with jQuery AJAX calls.  Easier to leave them as default and ensure all your calls have returned before you take the next step.

(2) As always, don't assume your solution will work as intended until you see it work in IE.


