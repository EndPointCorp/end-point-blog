---
author: Ron Phipps
gh_issue_number: 533
tags: javascript, jquery, tips, tools
title: Labeling input boxes including passwords
---



I'm currently working on a new site and one of the design aspects of the site is many of the form fields do not have labels near the input boxes, they utilize labels that are inside the input box and fade away when text is entered.  The label is also supposed to reappear if the box is cleared out.  Originally I thought this was a pretty easy problem and wrote out some jQuery to do this quickly.  The path I went down first was to set the textbox to the value we wanted displayed and then clear it on focus.  This worked fine, however I reached a stumbling block when it came to password input boxes.  My solution did not work properly because text in a password box is hidden and the label would be hidden as well.  Most people would probably understand what went in each box, but I didn't want to risk confusing anyone, so I needed to find a better solution

I did some searching for jQuery and labels for password inputs and turned up several solutions.  The first one actually put another text box on top of the password input, but that seemed prone to issue.  The solution I decided to ultimately use is called [In-Fields Labels](http://fuelyourcoding.com/in-field-labels/), a jQuery plugin by Doug Neiner. In this solution Doug has floating labels that appear over the top of the textbox, and they dim slightly when focus is gained and then disappear completely when typing begins.  The plugin does not mess with the value in the input box at all.

It was fairly easy to get up and running.  I added the plugin to the page, created some styling for the labels, added label tags with the class of 'overlay' for each input box and called $('label.overlay').inFieldLabels();.  This was all that was needed to get us going.

*Normal view*

<a href="/blog/2011/12/23/labeling-input-boxes-including/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5689389498450853362" src="/blog/2011/12/23/labeling-input-boxes-including/image-0.jpeg" style="cursor:pointer; cursor:hand;width: 370px; height: 230px;"/></a>

*Focus in the password box*

<a href="/blog/2011/12/23/labeling-input-boxes-including/image-1-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5689389502905817794" src="/blog/2011/12/23/labeling-input-boxes-including/image-1.jpeg" style="cursor:pointer; cursor:hand;width: 370px; height: 230px;"/></a>

*Typing in the password box*

<a href="/blog/2011/12/23/labeling-input-boxes-including/image-2-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5689389500673187938" src="/blog/2011/12/23/labeling-input-boxes-including/image-2.jpeg" style="cursor:pointer; cursor:hand;width: 372px; height: 230px;"/></a>

The effect is pretty cool and it provides a good interface for the user as they are reminded up until the time they type in the box what they are supposed to enter.


