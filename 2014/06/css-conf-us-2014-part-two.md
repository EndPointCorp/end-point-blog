---
author: Greg Davidson
title: CSS Conf US 2014 — Part Two
github_issue_number: 990
tags:
- accessibility
- android
- chrome
- conference
- css
- html
date: 2014-06-04
---

### More Thoughts on Getting Vertical, Testing and Icon Fonts

Without further ado I’ve written up another batch of my notes about three more great talks at CSS Conf US in Amelia Island, Florida last week.

### Antoine Butler — Embrace the Vertical

Antoine shared his observation that vertical media queries are available to CSS developers but not
often used. With the [vast array](https://opensignal.com/reports/fragmentation-2013/)
of devices accessing the web today vertical media queries can be a useful tool to adapt your content effectively. Antoine walked us through a couple examples of how he applied this technique in a couple of his projects. The first was a prototype of WikiPedia. While they have gone with a separated mobile site (e.g. en.m.wikipedia.org/), he started with the HTML from the desktop site and applied some vertical media queries to make the content much more digestible. Take a look at [his code](https://codepen.io/aebsr/full/155081893d1efd09a4893953be36cd8f/) to see how it works.

The second example Antoine demonstrated was for the navigation at [Volkswagen](http://www.vw.com/). The client wanted to display an unlimited number of items in the secondary navigation. Once again Antoine applied vertical media queries to handle the varying number of navigation elements based on the device height. Check out his [adaptive sticky vertical navigation code](https://codepen.io/aebsr/pen/wBuci/) for a closer look.

Slides from this talk are available here: [Embrace the Vertical](https://speakerdeck.com/aebsr/embrace-the-vertical).

### Christophe Burgmer — If your CSS is happy and you know it...

This was a really interesting talk about testing your CSS visually with a tool Christophe has been developing called [CSS Critic](http://cburgmer.github.io/csscritic/). Christophe covered some of the existing CSS/HTML testing tools like [Selenium](http://docs.seleniumhq.org/) and found that while they worked well they didn’t meet his needs entirely. He wanted a way to visually diff the changes that were made and to be able to write tests for his UI code. For example, when the “accepted” version of the page changed visually, he wanted to be notified and decide whether or not to accept the proposed change.

Christophe demoed the tool for us and it was really cool to see a visual diff in the browser. For a change that was introduced, screenshots of the old, new and difference were displayed. The user then has the ability to accept / OK the change or reject it. You can view the tool in action on the [CSS Critic](http://cburgmer.github.io/csscritic/) site. Under the hood, CSS Critic uses some other nifty projects including [Wraith](https://github.com/BBC-News/wraith), [PhantomCSS](https://github.com/Huddle/PhantomCSS), [CasperJS](http://casperjs.org/) and [Hardy](http://hardy.io/). Christophe also mentioned [csste.st](http://csste.st/) as a site which curates information on all of these topics and projects.

Slides from this talk are available here: [If you CSS is happy and you know it...](http://cburgmer.github.io/csscritic/cssconf2014/#/step-1)

### Zach Leatherman — Bulletproof Icon Fonts

Zach wrote a [great article](https://filamentgroup.com/lab/bulletproof_icon_fonts.html) on Bulletproof Accessible Icon Fonts earlier this year and his talk was along similar lines. He chronicled some of the challenges and pitfalls worth knowing about in order to support icon fonts in your sites and applications. Browser support varies a great deal and Zach cited John Holt Ripley’s [Unify](https://web-beta.archive.org/web/20161125011236/http://unicode.johnholtripley.co.uk:80/all/) unicode support charts as a helpful reference. He works on the [a-font-garde](https://github.com/filamentgroup/a-font-garde) project which documents best (er. bulletproof) practices for working with icon fonts today.

### Stay Tuned

Watch for one more post later this week with the last batch of talks from the conf!
