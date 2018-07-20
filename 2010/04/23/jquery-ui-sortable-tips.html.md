---
author: Chris Kershaw
gh_issue_number: 293
tags: browsers, javascript, jquery
title: jQuery UI Sortable Tips
---

I was recently tasked with developing a sorting tool to allow [Paper Source](https://www.papersource.com/) to manage the sort order in which their categories are displayed. They had been updating a sort column in a database column but wanted a more visual aspect to do so. Due to the well-received feature developed by Steph, it was decided that they wanted to adapt their upsell interface to manage the categories. See here for the post using [jQuery UI Drag Drop](/blog/2009/12/23/jquery-ui-drag-drop-tips-ecommerce).

The only backend requirements were that the same sort column was used to drive the order. The front end required the ability to drag and drop positions within the same container. The [upsell feature](/blog/2009/12/23/jquery-ui-drag-drop-tips-ecommerce) provided a great starting point to begin the development. After a quick review I determined that the [jQuery UI](https://jqueryui.com/) [Sortable](https://jqueryui.com/sortable/) function would be more favorable to use for the application.

<a href="/blog/2010/04/23/jquery-ui-sortable-tips/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5463443403683695490" src="/blog/2010/04/23/jquery-ui-sortable-tips/image-0.jpeg" style="cursor: pointer; width: 320px; height: 262px;"/></a>

Visual feedback was used to display the sorting in action with:

```javascript
// on page load
$('tr.the_items td').sortable({
opacity: 0.7,
helper: 'clone',
});
// end on page load
```

<a href="/blog/2010/04/23/jquery-ui-sortable-tips/image-1-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5463440966525461602" src="/blog/2010/04/23/jquery-ui-sortable-tips/image-1.jpeg" style="cursor: pointer; width: 320px; height: 170px;"/></a>

### Secondly I reiterate “jQuery UI Event Funtionality = Cool”

I only needed to use one function for this application to do the arrange the sorting values once the thumbnail had been dropped. This code calls a function which loops through all hidden input variables on the page and updates the sorting order.

```javascript
// on page load
$('tr.the_items td').sortable({
stop: function(event, ui) { do_drop(this); },
});
// end on page load
```

Validating the sorting fields was a little different from the previously developed feature in that the number of available items could change depending on the category. The number of items could easily be 3 or 30. Therefore I needed a quick way to check the ever changing number. I decided to use a nested loop using the each function.

```javascript
$('input.new_sku').each(
    function( intIndex, obj ) {
        $('input.new_sku').each(
            function( secIndex, secObj ) {
                if( (intIndex != secIndex) && ($(obj).val() == $(secObj).val()) ) {
                    error = true;
                }
            });
    }
);
```

<a href="/blog/2010/04/23/jquery-ui-sortable-tips/image-2-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5463443609961866050" src="/blog/2010/04/23/jquery-ui-sortable-tips/image-2.jpeg" style="cursor: pointer; width: 320px; height: 214px;"/></a>

The rest of the feature uses some of the same logic previously documented [here](/blog/2009/12/23/jquery-ui-drag-drop-tips-ecommerce).

All in all I learned that the jQuery UI is very versatile and a pleasure to work with. I hope to be using more of its features in the near future.
