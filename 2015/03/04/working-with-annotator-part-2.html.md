---
author: Steph Skardal
gh_issue_number: 1097
tags: javascript, rails
title: 'Working with Annotator: Part 2'
---



A while back, [I wrote about](/blog/2014/07/15/interactive-highlighting-and) my work on Ruby on Rails based [H2O](http://cyber.law.harvard.edu/research/h2o) with [Annotator](http://annotatorjs.org/), an open source JavaScript library that provides annotation functionality. In that article, I discussed the history of my work with annotations, specifically touching on several iterations with native JavaScript functionality developed over several years to handle colored highlight overlapping on selected text.

Finally, last July we completed the transition to [Annotator](http://annotatorjs.org/) from custom JavaScript development, with the caveat that the application had quite a bit of customization hooked into Annotator’s easily extensible library. But, just a few months after that, I revisited the customization, described in this post.

### Separation of UI Concerns

In our initial work with Annotator, we had extended it to offer a few additional features:

- Add multiple tags with colored highlights, where content can be tagged on the fly with a color chosen from a set of predefined colors assigned to the tag. Text would then be highlighted with opacity, and colors combined (using [xColor](https://github.com/infusion/jQuery-xcolor)) on overlapping highlights.
- Interactive functionality to hide and show un-annotated text, as well as hide and show annotated text with specific tags.
- Ability to link annotated text to other pieces of content.

But you know [the paradox of choice](https://www.ted.com/talks/barry_schwartz_on_the_paradox_of_choice?language=en)? The extended Annotator, with so many additional features, was offering too many choices in a cluttered user interface, where the choices were likely not used in combination. See:

<img border="0" src="/blog/2015/03/04/working-with-annotator-part-2/image-0.png" style="margin-bottom:2px;"/>Too many annotation options: Should it be hidden? Should it be tagged?

Should it be tagged with more than one tag? Can text be tagged and hidden?

So, I separated concerns here (a common term in software) to intentionally separate annotation features. Once a user selects text, a popup is shown to move forward with adding a comment, adding highlights (with or without a tag name), adding a link, or hiding that text:

<img border="0" src="/blog/2015/03/04/working-with-annotator-part-2/image-1.png" style="margin-bottom:2px;"/>

The new interface, where a user chooses the type of annotation they are saving, and only relevant fields are then visible.

<img border="0" src="/blog/2015/03/04/working-with-annotator-part-2/image-2.png" style="margin-bottom:2px;"/>

After the user clicks on the highlight option, only highlight related fields are shown.

### Annotator API

The functionality required to intercept and override Annotator’s default behavior and required core overrides, but the API has a few nice hooks that were leveraged to accommodate this functionality in the  H2O plugin:

- annotationsLoaded: called after annotation data loaded
- annotationsEditorSubmit: called after user saves annotation, before data sent to server
- annotationCreated: after annotation created
- annotationUpdated: after annotation updated
- annotationDeleted: after annotation deleted

While these hooks don’t mean much to someone who hasn’t worked with Annotator, the point is that there are several ways to extend Annotator throughout the CRUD (create, read, update, destroy) actions on an annotation.

### Custom Data

On the backend, the four types of annotation are contained in a single table, as was the data model prior to this work. There are several additional data fields to indicate the type of annotation:

- hidden (boolean): If true, text is not visible.
- link (text): Annotation can link to any other URL.
- highlight (color only, no tag): Annotation can be assigned a single colored highlight.
- highlight + tag (separate table, using various Rails plugins ([acts_as_taggable_on](https://github.com/mbleigh/acts-as-taggable-on))): Annotation can be assigned a single tag with a corresponding colored highlight.

### Conclusion

The changes here resulted in a less cluttered, more clear interface. To a user, each annotation has a single concern, while utilizing Annotator and saving to a single table.


