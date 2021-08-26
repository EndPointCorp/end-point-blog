---
author: Patrick Lewis
title: 'Zurb Foundation 5: Applying Styles Conditionally Based on Viewport Size'
github_issue_number: 1200
tags:
- css
- mobile
date: 2016-02-08
---

The [Zurb Foundation 5](http://foundation.zurb.com/sites/docs/v/5.5.3/) front-end framework provides many convenient features such as the ability to control the visibility of HTML elements for different browser window sizes using CSS classes. Foundation CSS classes like “show-for-small-only” and “hide-for-large-up” (full list at [http://foundation.zurb.com/sites/docs/v/5.5.3/components/visibility.html](http://foundation.zurb.com/sites/docs/v/5.5.3/components/visibility.html)) make it easy to add mobile-specific content to your page or prevent certain page elements from being displayed on mobile devices.

Having an easy way to show/hide elements based on viewport size is nice, but what if you want to style an element differently based on the size of the browser that’s viewing the page? Foundation has you covered there, too, though the method is less obvious. It’s possible to use Foundation’s media query SCSS variables when writing your own custom styles in order to apply different styling rules for different viewport sizes.

For example, if you have an element that you want to offset with a margin in a large window but be flush with the left edge of a small window, you can use the Foundation media query variables to apply a styling override that’s specific to small windows:

```scss
#element {
    margin-left: 100px;

    @media #{$small-only} {
        margin-left: 0;
    }
}
```

This will apply a specific set of styling to the element for small viewports and a different set for medium and larger viewports (with the definitions for “small”, “medium”, etc. corresponding to the same values used by Foundation’s visibility classes like “show-for-small-only” which were mentioned at the start of this post).

It wasn’t immediately obvious to me how to apply conditional styling using Foundation’s own definitions of small, medium, etc. viewport sizes but luckily the variable definitions provided by the SCSS framework make it easy to do so.
