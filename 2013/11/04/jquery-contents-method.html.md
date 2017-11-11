---
author: Steph Skardal
gh_issue_number: 872
tags: javascript, jquery
title: jQuery contents() method
---



I had an interesting JavaScript challenge recently and came across a jQuery method that I hadn't heard of before, so I wanted to share my experience. Given the following markup, I needed a way to hide all the text not inside span.highlighted elements:

```html
<p>Here is some text. 
<span class="highlighted">Here is more text! </span>
Here is even more text! Here is some more un-wrapped text. 
<span class="highlighted">Here is another wrapped span.</span>
</p>
```

With standard CSS rules like visibility, display, and opacity, there's not an easy way to hide only the unhighlighted text without additional HTML modifications. So, I set out to wrap the unhighlighted text in additional HTML elements dynamically, to produce the following markup from our example:

```html
<p><span class="unhighlighted">Here is some text. </span>
<span class="highlighted">Here is more text! </span>
<span class="unhighlighted">Here is even more text! Here is some more un-wrapped text. </span>
<span class="highlighted">Here is another wrapped span.</span>
</p>
```

With the markup above, the CSS rules to hide the desired spans would look something like:

```css
p span.unhighlighted { display: none; }
p span.highlighted { display: inline-block; }
```

The challenge was how to wrap the unwrapped text inside the paragraph without having any DOM elements to select? My first clumsy attempt was using regular expressions, which looked something like this:

```javascript
var matches = $('p').html().match(/<span class="highlighted.*?"<.*?<\/span>/g);
var non_matches = $('p').html().split(/<span class="highlighted.*?">.*?<\/span>/);

var b = '';
for(var _i=0; _i<non_matches.length; _i++) {
  if(non_matches[i] != '') {
    b += '<span class="unhighlighted">' + non_matches[i] + '</span>';
  }
  if(matches[i] !== undefined) {
    b += matches[i];
  }
}
$('p').html(b);
```

In the code above, I create two arrays – one that includes the unhighlighted text and one that includes the highlighted spans and their content with a non-greedy regular expression. I incremented through these arrays and built HTML with alternating newly wrapped unhighlighted content and existing highlighted spans. At the end of the loop, the paragraph HTML is updated with the new HTML. Now, there are quite a few edge cases with this method which needed to be addressed **and** the bigger issue I came across was that the highlighted spans were being rewritten, so any important data tied to the overwritten highlighted spans was lost with the HTML update. I felt that this implementation was overcomplicated and went in search of something more simple.

### jQuery contents()

Enter the [jQuery.contents()](http://api.jquery.com/contents/) method. This method returns the children nodes of an element (or elements) in an array form, including(!) text and comment nodes. The console output of the contents() method for our example paragraph might look like:

<img src="/blog/2013/11/04/jquery-contents-method/image-0.png" style="border:1px solid #000;"/>

Example output from the contents() method.

This was just the tool I was looking for: I wanted a simple way to iterate through text and span elements from my existing paragraph, without replacing exising span elements. The following JavaScript shows incremental through the contents() array and wrapping text elements with the new markup:

```javascript
var contents = $('p').contents();
for(var _i = 0; _i < contents.length; _i++) {
  if(contents[_i].nodeType == 3) { //conditional indicates match on TextNode
    var updated = '<span class="unhighlighted">' + $(contents[_i]).text() + '</span>';
    $(contents[_i]).replaceWith(updated); 
  }
}
```

I then have the ability to toggle the visibility of both the highlighted and unhighlighted spans for the desired functionality. I've been working with jQuery for a long time and was happy to browse through the documentation to find this little gem!


