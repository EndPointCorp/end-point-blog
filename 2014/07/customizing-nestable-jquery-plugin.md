---
author: Steph Skardal
title: Customizing the Nestable jQuery Plugin
github_issue_number: 1018
tags:
- javascript
date: 2014-07-29
---



A while back, we started using the [Nestable jQuery Plugin](https://dbushell.com/2012/06/17/nestable-jquery-plugin/) for [H2O](https://cyber.law.harvard.edu/research/h2o). It provides interactive hierarchical list functionality – or the ability to sort and nest items.

<img border="0" src="/blog/2014/07/customizing-nestable-jquery-plugin/image-0.png"/>

Diagram from Nestable jQuery Plugin representing interactive hierarchical sort and list functionality.

I touched on H2O’s data model [in this post](/blog/2014/06/rails-performance-with-skylight/), but it essentially mimics the diagram above; A user can build sortable and nestable lists. Nesting is visible at up to 4 levels. Each list is accessible and editable as its own resource, owned by a single user. The plugin is ideal for working with the data model, however, I needed a bit of customization that I’ll describe in this post.

### Limiting Nestability to Specific List Items

The feature I was requested to develop was to limit nesting to items owned by the current authorized (logged in) user. Users can add items to their list that are owned by other users, but they can not modify the list elements for that list item. In visual form, it might look something like the diagram below, where green represents the items owned by the user which allow modified nesting, and red represents items that are not owned by the user which can not be modified. In the diagram below, I would not be able to add to or reorder the contents of Item 5 (including Items 6–8), and I would not be able to add any nested elements to Item 10. I can, however, reorder elements inside Item 2, which means e.g. I can move Item 5 above Item 3.

<img border="0" src="/blog/2014/07/customizing-nestable-jquery-plugin/image-1.png"/>

Example of nesting where nesting is prohibited among some items (red), but allowed under others (green).

There are a couple of tricky bits to note in developing this functionality:

- The plugin doesn’t support this type of functionality, nor is it currently maintained, so there are absolutely no expectations of this being an included feature.
- These pages are fully cached for performance optimization, so there is no per-user logic that can be run to generate modified HTML. The solution here was implemented using JavaScript and CSS.

### Background Notes on the Plugin

There are a couple of background notes on the plugin before I go into the implemented solution:

- The plugin uses \<ol\> tags to represent lists. Only items in \<ol\> elements are nestable and sortable.
- The plugin recognizes .dd-handle as the draggable handle on a list item. If an item doesn’t have a .dd-handle element, no part of it can be dragged.
- The plugin creates a \<div\> with a class of dd-placeholder to represent the placeholder where an item is about to be dropped. The default appearance for this is a white box with dashed outline.
- The plugin has an on change event which is triggered whenever any item is dropped in the list or any part of the list is reordered.

### Step 1: JavaScript Update for Limiting Nestability

After the content loads, as well as after additional list items are added, a method called set_nestability is run to modify the HTML of the content, represented by the pseudocode below:

```javascript
set_nestability: function() {
  // if user is not logged in
    // nestability is never enabled
  // if user is logged in user is not a superadmin (superadmins can edit all) 
    // loop through each list item 
      // if the list item data('user_id') != $.cookie('user_id')
        // remove dd-handle class from all list item children .dd-handle elements
        // replace all <ol> tags with <ul> tags inside that list item
```

The simple bit of pseudocode does two things: It removes the .dd-handle class for elements that can’t be reordered, and it replaces \<ol\> tags with \<ul\> tags to enable CSS. The only thing to take note of here is that in theory, a “hacker” can change their cookie to enable nestability of certain items, but there is additional server-side logic that would prohibit an update.

### Step 2: CSS Updates

```css
ul .dd-placeholder {
  display: none;
}
```

Next up, the simple CSS change above was made. This results in the placeholder div being hidden in any non-editable list. I made several small CSS modifications so that the ul and ol elements would look the same otherwise.

### Step 3: JavaScript On Change Updates

Finally, I modified the on change event:

```javascript
$('div#list').on('change', function(el) {
  // if item is dropped
    // if dropped item is not inside <ol> tag, return (do nothing)
    // else continue with dropped logic
  // else if position is changed
    // trigger position change logic  
}
```

The on change event does nothing when the dropped item is not inside an editable list. Otherwise, the dropped logic continues as the user has permissions to edit the list.

### Conclusion

The functionality described here has worked well. What may become a bit trickier is when advanced rights and roles will allow non-owners to edit specific content, which I haven’t gotten to yet. I haven’t found additional resources that offer sortable and nestable functionality in jQuery, but it’d be great to see a new well-supported plugin in the future.


