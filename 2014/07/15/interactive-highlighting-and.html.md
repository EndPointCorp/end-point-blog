---
author: Steph Skardal
gh_issue_number: 1012
tags: javascript, ruby, rails
title: Interactive Highlighting and Annotations with Annotator
---



Over a year ago, [I wrote about JavaScript-driven interactive highlighting](http://blog.endpoint.com/2013/01/javascript-driven-interactive.html) that emulates the behavior of physical highlighting and annotating text. It's interesting how much technology can change in a short time. This spring, I've been busy at work for on a major upgrade of both Rails (2.3 to 4.1) and of the annotation capabilities for [H2O](http://cyber.law.harvard.edu/research/h2o). As I explained in the original post, this highlighting functionality is one of the most interesting and core features of the platform. Here I'll go through a brief history and the latest round of changes.

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2014/07/15/interactive-highlighting-and/image-0.png" style="margin-bottom:3px;"/><br/>
Example digital highlighting of sample content.</div>

### History

My [original post](http://blog.endpoint.com/2013/01/javascript-driven-interactive.html) explains the challenges associated with highlighting content on a per-word basis, as well as determining color combinations for those highlights. In the past implementations, each word was wrapped in a single DOM element and that element would have its own background color based on the highlighting (or a white background for no highlighting). In the first iteration of the project, we didn't do allow for color combinations at all – instead we tracked history of highlights per word and always highlighted with the most recent color if it applied. In the second iteration of the annotation work, opaque layers of color were added under the words to simulate color combinations using absolute positioning. Cross browser support for absolute positioning is not always consistent, so this iteration had challenges.

In the third iteration that lasted for over a year, I found a great plugin ([xColor](https://github.com/infusion/jQuery-xcolor)) to calculate color combinations, eliminating the need for complex layering of highlights. The most recent iteration was acceptable in terms of functionality, but the major limitation we found was in performance. When every word of a piece of content has a DOM element, there are significant performance issues when content has more than 20,000 words, especially noticeable in the slower browsers.

I've had my eye out for a better way to accomplish this desired functionality, but without having a DOM per word markup, I didn't know if there was a better way to accomplish annotations without the performance challenges.

### Annotator Tool

Along came [Annotator](http://annotatorjs.org/), an open source JavaScript plugin offering annotation functionality. A coworker first brought this plugin to my attention and I spent time evaluating it. At the time, I concluded that while the plugin looked promising, there was too much customization required to support the already existing features in H2O. And of course, the tool did not support IE8, which was a huge at the time, although it becomes less of a limitation as time passes and users move away from IE8.

Time passed, and the H2O project manager also came across the same tool and brought it to my attention. I spent a bit of time developing a proof of concept to see how I might accomplish some of the desired behavior in a custom encapsulated plugin. With the success of the proof of concept, I also spent time working through the IE8 issues. Although I was able to work through many of them, I was not able to find a solution to fully support the tool in IE8. At that time, a decision was made to use Annotator and disable annotation capabilities for IE8. I moved forward on development.

### How does it work?

Rather than highlighting content on a word level, Annotator determines the [XPath](http://www.w3schools.com/XPath/) of a section of highlighted characters. The XPath for the annotation starting point and ending point is retrieved, and one or more DOM elements wrap this content. If the annotated characters span multiple DOM elements (e.g. the annotation spans multiple paragraphs), multiple DOM elements are created for each parent element to wrap the annotated characters. Annotator handles all the management of the wrapped DOM elements for an annotation, and it provides triggers or hooks to be called tied to specific annotation events (e.g. after annotation created, before annotation deleted).

This solution has much better performance than the aforementioned techniques, and there's a growing community of open source developers involved in it, who have helped improve functionality and contribute additional features.

### Annotator Customizations

Annotator includes a nice plugin architecture designed to allow custom functionality to be built on top of it. Below are customized features I've added to the application:

#### Colored Highlighting

In my custom plugin, I've added tagged colored highlighting. An editor can select a specific color for a tag assigned to an annotation from preselected colors. All users can highlight and unhighlight annotations with that specific tag. The plugin uses [jQuery XColor](https://github.com/infusion/jQuery-xcolor), a JavaScript plugin that handles color calculation of overlapping highlights. Users can also turn on and off highlighting on a per tag basis.

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2014/07/15/interactive-highlighting-and/image-1.png" style="margin-bottom:3px;"/><br/>
Tagged colored highlighting (referred to as layers here) is selected from a predefined set of colors.</div>

#### Linked Resources

Another customization I created was the ability to link annotations to other resources in the application, which allows for users to build relationships between multiple pieces of content. This is merely an extra data point saved on the annotation itself.

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2014/07/15/interactive-highlighting-and/image-2.png" style="margin-bottom:3px;"/><br/>
A linked collage from this annotation.</div>

#### Toggle Display of layered and unlayered content

One of the most difficult customization points was building out the functionality that allows users to toggle display of unlayered and layered content, meaning that after a user annotates a certain amount of text, they can hide all the unannotated text (replaced with an ellipsis). The state of the content (e.g. with unlayered text hidden) is saved and presented to other users this way, which essentially allows the author to control what text is visible to users.

<div class="separator" style="clear: both; text-align: center;"><img border="0" src="/blog/2014/07/15/interactive-highlighting-and/image-3.png" style="margin-bottom:3px;"/></div>

### Learn More

Make sure to check out the [Annotator website](http://annotatorjs.org/) if you are interested in learning more about this plugin. The active community has interesting support for annotating images, video, and audio, and is always focused on improving plugin capabilities. One group is currently focused on cross browser support, including support of IE8.


