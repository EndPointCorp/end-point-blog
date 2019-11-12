---
title: "Winning with CSS Grid and Autoprefixer"
author: Greg Davidson
tags: browsers, css, tools, development
gh_issue_number: 1571
---

![Aerial view of St. Vitus Cathedral, Prague](/blog/2019/11/04/winning-with-css-grid-and-autoprefixer/grid.jpg)

Photo by [Stijn te Strake](https://unsplash.com/photos/BWtyq5fn6Ng) on [Unsplash](https://unsplash.com/)

### Using CSS Grid Today

[Support for CSS Grid](https://caniuse.com/#search=css%20grid) is excellent (over 90% globally! 💯). I have been using it in a variety of client projects for the past few years with great success. The combination of CSS Grid and Flexbox has made layout on the web much simpler, more fun and less frustrating compared to the ~~hacks~~ techniques which were used for CSS layout in the past. Definitely give it a try if you haven’t already done so.

IE10 and IE11 support an earlier version of the CSS Grid spec and with help from Autoprefixer we can reap the benefits of CSS Grid in those old browsers with a little bit of extra work. I’ve long been a huge fan and happy user of [Autoprefixer](https://github.com/postcss/autoprefixer). It’s a [PostCSS](https://postcss.org/) plugin that examines your CSS and augments it with [vendor prefixes](https://developer.mozilla.org/en-US/docs/Glossary/Vendor_Prefix) and alternative syntaxes. Although vendor prefixes (e.g. `-webkit`, `-moz`, `-o`, etc.) are much less common these days, there are a few still in use.

### CSS Grid Basics

With CSS Grid the basic idea is to define the grid, i.e. the rows and columns that make it up, and then go about placing elements on the grid. Think of a website layout with a masthead, navigation, hero image, main content sidebar, and footer as an example. Your grid styles can specify where each of these elements should be displayed on the grid: how many rows or columns they span, etc. In addition to this method of explicitly placing elements on the grid, [auto-placement](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Auto-placement_in_CSS_Grid_Layout) places elements on the grid for you  automatically.

### Autoprefixer + CSS Grid

I recently learned how to use [control comments in Autoprefixer](https://github.com/postcss/autoprefixer#control-comments) to get fine-grained control over the way it operates on and enhances my CSS Grid styles. Rather than specifying a single (global) behavior via config options, control comments let you tell Autoprefixer how you would like it to process individual blocks of CSS code. For the scenario where I was explicitly placing elements on my grid I used the following control comment in my CSS file:

```css
/* autoprefixer grid: no-autoplace */
```

This allowed me to lay out the elements and Autoprefixer generated the `-ms-grid` styles required to make my modern CSS Grid styles work in IE 10 and IE 11.

In another scenario I ***did*** want the auto-placement support and enabled it with the following control comment in a different block of the same CSS file:

```css
/* autoprefixer grid: autoplace */
```

This was for a group of uniformly sized tile elements that I wanted to lay out in a grid that adapted as the viewport size varied. E.g.: from 4 tiles per row, to 3 tiles, to 2 and finally to 1 tile per row for the smallest viewports.

In both cases I was pleasantly surprised that my CSS Grid styles worked in modern browsers **and** also in IE 11 and 10! I added some fallback styles using flexbox for those browsers which do not yet support CSS Grid to ensure the content was accessible there as well.

### Test Your Autoprefix’d Grid Styles

Please note the Autoprefixer docs warn its grid support may not work in *all* cases and must be tested. For my purposes this worked you great but make sure to test because your mileage may vary.

### Learning More

If you’d like to learn more about CSS Grid I would recommend checking out [Jen Simmons’](https://jensimmons.com/) [CSS Grid Basics](https://www.youtube.com/playlist?list=PLbSquHt1VCf0b43dfLKTrCriXdlZcmgoi) series on YouTube and the [Grid by Example](https://gridbyexample.com/) site by [Rachel Andrew](https://rachelandrew.co.uk/). To learn more about Autoprefixer, check out [the docs](https://github.com/postcss/autoprefixer) at GitHub or you can [try it out interactively](https://autoprefixer.github.io/).
