---
author: Jeff Boes
gh_issue_number: 962
tags: javascript, jquery, html
title: jQuery Content Replacement with AJAX
---

This is not a huge breakthrough, but it colored in some gaps in my knowledge so I thought I would share.

Let’s say you have a product flypage for a widget that comes in several colors. Other than some of the descriptive text, and maybe a hidden field for use in ordering one color instead of another, all the pages look the same. So your page looks like this (extremely simplified):

```html
... a lot of boilerplate ...
<form id="order_item">
<input name="sku" type="hidden" value="WDGT-001-RED"/>
<input type="hidden"/>
</form>
... a lot more boilerplate ...
```

Probably the page is generated into a template based on a parameter or path segment:

```nohighlight
http://.../app/product/WDGT-001-RED
```

What we’re going to add is a quick-and-dirty way of having your page *rewrite itself* on the fly with just the bits that change when you select a different version (or variant) of the same product. E.g.,

```html
<select name="sku">
<option value="WDGT-001-RED">Cinnamon Surprise</option>
<option value="WDGT-002-BLK">Midnight Delight</option>
<option value="WDGT-003-YLW">Banana Rama</option>
</select>
```

The old-school approach was something like:

```javascript
 $('select[name=sku]').change(function(){
   document.location.href = my_url + $(this).val();
 });
```

I.e., we’ll just send the browser to re-display the page, but with the selected SKU in the URL instead of where we are now. Slow, clunky, and boring!

Instead, let’s take advantage of the ability to grab the page from the server and only freshen the parts that change for the desired SKU (warning: this is a bit hand-wavy, as your specifics will change up the code below quite a bit):

```javascript
// This is subtly wrong:
$('select[name=sku]').change(function(){
  $.ajax({
    async: false,
    url: my_url + $(this).val(),
    complete: function(data){
      $('form#order_item').html( $(data.responseText).find('form#order_item').html() );
    }
});
```

Why wrong? Well, any event handlers you may have installed (such as the .change() on our selector!) will fail to fire after the content is replaced, because the contents of the form don’t have those handlers. You could set them up all over again, but there’s a better way:

```javascript
// This is better:
$('form#order_item').on('change', 'select[name=sku]',
  function(){
  $.ajax({
    async: false,
    url: my_url + $(this).val(),
    complete: function(data){
      var doc = $(data.responseText);
      var $form = $('form#order_item');
      var $clone = $form.clone( true );
      $clone.html(doc.find('form#order_item').html());
      $form.replaceWith($clone);
    }
  });
```

Using an “on” handler for the whole form, with a filter of just the select element we care about, works better—​because when we clone the form, we copy its handler(s), too.

There’s room for improvement in this solution, because we’re still fetching the entire product display page, even the bits that we’re going to ignore, so we should look at changing the .ajax() call to reference something else—​maybe a custom version of the page that only generates the form and leaves out all the boilerplate. This solution also leaves the browser’s address showing the original product, not the one we selected, so a page refresh will be confusing. There are fixes for both of these, but that’s for another day.
