---
author: Steph Skardal
title: jQuery UI Drag Drop Tips and an Ecommerce Example
github_issue_number: 241
tags:
- browsers
- javascript
date: 2009-12-23
---



This week, I implemented functionality for [Paper Source](https://www.papersource.com/) to allow them to manage the upsell products, or product recommendations. They wanted a better way to visualize, organize, and select the three upsell products for every product. The backend requirements of this functionality were relatively simple. A new table was created to manage the product upsells.

The frontend requirements were more complex: They wanted to be able to drag and drop products into the desired upsell position (1, 2, or 3). I was allowed a bit of leeway on the interactivity level of the functionality, but the main requirement was to have drag and drop functionality working to provide a more efficient way to manage upsells. A mockup similar to the image shown below was provided at the onset of the project.

<a href="https://1.bp.blogspot.com/_wWmWqyCEKEs/SzKnodNzrzI/AAAAAAAAC2Q/Qz6A42KEaCc/s1600-h/image1.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5418577615159275314" src="/blog/2009/12/jquery-ui-drag-drop-tips-ecommerce/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 226px;"/></a>

The mockup provided did not demonstrate the “interactiveness” of the drag and drop functionality. Items below the current upsells were ordered by cross sell revenue, or the revenue of each related item purchased with the current item.

Since I was familiar with jQuery, I knew that the [jQuery UI](https://jqueryui.com/) included drag and drop functionality. I also had heard of several other jQuery drag and drop plugins, but since the jQuery UI is well supported, I was hopeful that the UI would have the functionality that I envisioned needing. Throughout the project, I learned a few valuable tips to consider with drag and drop implementation. To begin development, I downloaded the latest [jQuery](https://jquery.com/) and [UI Core](https://jqueryui.com/) in addition to the draggable and droppable UI components.

### Visual Feedback = Helpful

The first thing I learned from working on the drag and drop functionality, was that **visual feedback is very helpful in interactive design** and that the jQuery UI has functionality built in to provide visual feedback. The first bit of visual feedback I included was to use a “clone” helper with semi-opaque styling to provide visual feedback that the object was being dragged. This was accomplished using the following code:

```javascript
// on page load
$('div.common_item').draggable({
  opacity: 0.7,
  helper: 'clone'
});
// end on page load
```

And is shown here as the *Lake Peace 1.25” Circle Stickers* product is dragged:

<a href="https://4.bp.blogspot.com/_wWmWqyCEKEs/SzKno1CUs-I/AAAAAAAAC2Y/nW5Orkn5D6c/s1600-h/image2.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5418577621553558498" src="/blog/2009/12/jquery-ui-drag-drop-tips-ecommerce/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 227px;"/></a>

The second bit of visual feedback I included was adding a class to the droppable item when a draggable item hovered over it. I added the “hoveringover” class to the droppable item which was defined in by the stylesheet to have a different colored background. This was accomplished using the following code:

```javascript
// on page load
$('tr.upsells td').droppable({
  hoverClass: 'hoveringover'
});
// end on page load
```

And is shown here as the *Shimmer Silver A7 Envelope* product hovers above the *Quilt on Night with Curry A2 Stationers* in upsell position #2:

<a href="https://4.bp.blogspot.com/_wWmWqyCEKEs/SzKnpL8jKzI/AAAAAAAAC2g/KEzI_vYcfN8/s1600-h/image3.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5418577627703356210" src="/blog/2009/12/jquery-ui-drag-drop-tips-ecommerce/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 227px;"/></a>

### jQuery UI Event Functionality = Useful

The second tip I learned from working on the drag and drop functionality was that the **jQuery drag and drop UI includes valuable event functionality** to manage events during the drag and drop process.

By adding the code shown below, at the initiation of dragging, I set a hidden input variable to track which element was being dragged. This value was later used to populate the product upsell form.

```javascript
// on page load
$('div.common_item').draggable({
  start: function(event, ui) { $('input#is_dragging').val($(this).attr('id')); }
  });
// end on page load
```

By adding the code shown below, at the conclusion of dragging, I cleared the hidden input variable that indicated which item was being dragged.

```javascript
// on page load
$('div.common_item').draggable({      
  stop: function(event, ui) { $('input#is_dragging').val(''); }
});
// end on page load
```

A final event response was added to be called when an item is dropped on a droppable item. The function do_drop is called at this drop time. The do_drop function replaces the html of the current upsells if the dropped sku is different than the current upsell sku, updates the hidden form element, adds visual feedback by adding a class to show that the item had been replaced, and displays the “Save” and “Revert” options to save to database or revert the upsell items.

```javascript
// on page load
$('tr.upsells td').droppable({
  drop: function(event, ui) { do_drop(this); }
});
// end on page load

var do_drop = function(obj) {
  var current_sku = $('input#is_dragging').val();
  if(current_sku != $(obj).find('img').attr('class')) {
    //show "Save" and "Revert" options
    show_drag_form();

    //update hidden form element
    $('input#' + $(obj).attr('id').replace('td_', '')).val(current_sku);

    //replace html and add visual feedback by adding a class to show that the item was replaced
    $(obj).html($('div#' + current_sku).html()).addClass('replaced');     
  }
};
```

Shown below, the *Curry Dots A9 Printable Party Invitations* have been replaced with the *Olive Natsuki Gel Roller* and the background color change signifies the item has been modified.

<a href="https://1.bp.blogspot.com/_wWmWqyCEKEs/SzKnpTdne3I/AAAAAAAAC2o/QaAudyXFwpE/s1600-h/image4.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5418577629721099122" src="/blog/2009/12/jquery-ui-drag-drop-tips-ecommerce/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 247px;"/></a>

### jQuery UI Documentation and Examples = Awesome

I found the jQuery UI documentation and examples to be very helpful. Another jQuery UI draggable component that was used was to force draggable items to be contained to a region on the page. I contained the elements to the entire parent table using the following code.

```
$('div.common_item').draggable({
  containment: 'table#drag_table'
});
```

The *Envelope Liners* product is shown below to be confined to the table that contained potential and current upsell products. I could not drag the *Envelope Liners* any further to the right.

<a href="https://1.bp.blogspot.com/_wWmWqyCEKEs/SzKnpqTuX7I/AAAAAAAAC2w/Mye7b1Olirk/s1600-h/image5.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5418577635853623218" src="/blog/2009/12/jquery-ui-drag-drop-tips-ecommerce/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 231px;"/></a>

Because the functionality was a backend admin tool, the client requested that the functionality not be over-engineered to work across browsers. I did, however, verify that the drag and drop functionality worked in Firefox, Internet Explorer 7 and 8, Chrome, and Safari with a small amount of styling tweaking.

The final drag-drop JavaScript initiation is similar to the following code:

```
$(function() {
  $('div.common_item').draggable({
    opacity: 0.7,
    helper: 'clone',
    start: function(event, ui) { $('input#is_dragging').val($(this).attr('id')); },
    stop: function(event, ui) { $('input#is_dragging').val(''); },
    containment: 'table#drag_table'
  });
  $('tr.upsells td').droppable({
    hoverClass: 'hoveringover',
    drop: function(event, ui) { do_drop(this); }
  });
})
```

Shown below is an example of the product upsell in action for the Chrysanthemum Letterpress Thank You Notes.

<a href="http://3.bp.blogspot.com/_wWmWqyCEKEs/SzKnunOsOEI/AAAAAAAAC24/ed4uD6Y5fe4/s1600-h/image6.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5418577720926550082" src="/blog/2009/12/jquery-ui-drag-drop-tips-ecommerce/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 307px;"/></a>


