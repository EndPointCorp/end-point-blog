---
author: Ron Phipps
gh_issue_number: 392
tags: javascript, jquery, tips
title: jQuery code for making a block level element clickable while maintaining left/middle/right
  clicking
---



While working on a recent redesign for a client we needed the ability to click on a div and have it function as a link to a product page.  The initial implementation used the jQuery plugin [BigTarget.js](http://newism.com.au/blog/post/58/bigtarget-js-increasing-the-size-of-clickable-targets/).  The plugin searches within the div for a link and when the div is clicked changes the location to the link that is found.  This plugin worked fine and was fairly easy to setup, however there was one drawback that we found once it was released in the wild.  Most people expect to be able to right click, middle click, shift click, and control click to get the context-sensitive menu, open in a new window, or open in a new tab.

Enter [Superlink.js](http://james.padolsey.com/javascript/table-rows-as-clickable-anchors/), a jQuery plugin that uses a cool trick of moving the location of a link to the location of the mouse within the block level element (such as a div, li, tr, td, etc.).  With this implementation the mouse is actually over a link so that the various ways of clicking function as expected.  Initially I started moving the clickable area within a table, as shown in the example, but then quickly realized there was no reason this shouldn't work within a div or li.  One other neat thing with this plugin is that the events attached to the block will continue to function, they are passed to the event handlers for the link being moved within the block.


