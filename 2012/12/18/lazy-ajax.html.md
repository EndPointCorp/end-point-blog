---
author: Jeff Boes
gh_issue_number: 736
tags: ajax, interchange, javascript, jquery
title: Lazy AJAX
---



Don't do this, at least not without a good reason. It's not the way to design AJAX interfaces from scratch, but it serves well in a pinch, where you have an existing CGI-based page and you don't want to spend a lot of time rewriting it.

I was in a hurry, and the page involved was a seldom-used administration page. I was attempting to convert it into an AJAX-enabled setup, wherein the page would stand still, but various parts of it could be updated with form controls, each of which would fire off an AJAX request, and use the data returned to update the page.

However, one part of it just wasn't amenable to this approach, or at least not quick-and-dirty. This part had a relatively large amount of inline interpolated (Interchange) data (if you don't know what Interchange is, you can substitute "PHP" in that last sentence and you'll be close enough.) I wanted to run the page back through the server-side processing, but only cared about (and would discard all but) one element of the page.

My lazy-programmer's approach was to * submit the page itself as an AJAX request*:

```
$.ajax({
    url: '/@_MV_PAGE_@',
    data: {
        'order_date': order_date,
        'shipmode' : shipmode
    },
    method: 'GET',
    async: true,
    success: function(data, status){
        $('table#attraction_booklet_order').replaceWith(
            $(data).find('#attraction_booklet_order').get(0)
        );
        $('table#attraction_booklet_order').show();
    }
}); 
```

In this excerpt, "MV_PAGE" is a server-side macro that evaluates to the current page's path. The element I care about is a rather complex HTML table containing all sorts of interpolated data. So I'm basically reloading the page, or at least that restricted piece of it. The tricky bit, unfamiliar to jQuery newcomers, lets you parse out something from the returned document much as you would from your current document.

Again, don't do this without a reason. When I have more time, I'll revisit this and improve it, but for now it's good enough for the current needs.


