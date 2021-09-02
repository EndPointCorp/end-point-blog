---
author: Steph Skardal
title: 'Usability: Don’t Make Me Think and a Bookmarklet'
github_issue_number: 1151
tags:
- books
- javascript
- tips
date: 2015-08-13
---



*Hi! Steph here, former long-time End Point employee now blogging from afar as a software developer for [Pinhole Press](https://pinholepress.com/). While I’m no longer an employee of End Point, I’m happy to blog and share here.*

I’m only about a quarter of the way into [Don’t Make Me Think (Revised)](https://www.sensible.com/dmmt.html) by Steve Krug, but I can already tell it’s a winner. It’s a great (and quick) book about web usability, with both high level concepts and nitty gritty examples. I highly recommend it! Even if you aren’t interested in web usability but are a web developer, it’s still a quick read and would be invaluable to whomever you are coding for these days.

### A Bookmarklet

The book inspired me to write a quick bookmarklet to demonstrate some high level concepts related to usability. Here’s the bookmarklet:

```javascript
javascript:(function() {
  var possible = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  $('*:not(iframe)').contents().filter(function() {
     return this.nodeType == Node.TEXT_NODE && this.nodeValue.trim() != '';
  }).each(function() {
     var new_content = '';
     for(var i = 0; i<this.nodeValue.trim().length; i++) {
       new_content += possible.charAt(Math.floor(Math.random() * possible.length));
     }
     this.nodeValue = new_content;
  });
})();
```

To add the bookmarklet to your browser, simply copy the code in as the location for a new bookmark (and name it anything you want). Note that this particular bookmarklet assumes jQuery is installed, so it may not work on all websites. [Gist available here](https://gist.github.com/stephskardal/23112aa8e63252ac5be9)

### What does it do?

In short, the bookmarklet converts readable text on the page to jibberish (random characters of the same length). Pictures are worth a thousand words here. Here are some example pages with the bookmarklet in action:

<img border="0" src="/blog/2015/08/usability-dont-make-me-think-and/image-0.png" style="margin-bottom:5px;" width="800"/>

End Point home page.

<img border="0" src="/blog/2015/08/usability-dont-make-me-think-and/image-1.png" style="margin-bottom:5px;" width="800"/>

End Point client list page.

<img border="0" src="/blog/2015/08/usability-dont-make-me-think-and/image-2.png" style="margin-bottom:5px;" width="800"/>

[Stance](https://www.stance.com/) popup, with item in cart.

<img border="0" src="/blog/2015/08/usability-dont-make-me-think-and/image-3.png" style="margin-bottom:5px;" width="800"/>

[Backcountry.com](http://www.backcountry.com/womens-clothing) product listing page.

<img border="0" src="/blog/2015/08/usability-dont-make-me-think-and/image-4.png" style="margin-bottom:5px;" width="800"/>

[CityPASS](http://www.citypass.com/) home page.

### Why does this matter?

The bookmarklet provokes thought related to high level usability concepts, such as:

- Is it clear which buttons are clickable?
- Is the visual hierarchy clear?
- What conventions does the user interface follow?
- Users browsing behavior is often to hyperfocus and click on what they are looking for while ignoring other content entirely. Does the user interface aid or hinder that behavior?
- How and what do images communicate on the page?

All of these ideas are great things to talk through when implementing user interface changes or rolling out an entirely new website. And if you are interested in learning more, [visit Steve Krug’s website](https://www.sensible.com/dmmt.html).


