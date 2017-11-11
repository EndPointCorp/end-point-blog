---
author: Josh Williams
gh_issue_number: 885
tags: ajax, django, javascript, python
title: Asynchronous Page Switches with Django
---

Now that the newly rebuilt [endpoint.com](/) website is up and running, you may have noticed it does something fancy: internal links within the site are fetched in the background, and the page is replaced dynamically with a script.  That eliminates the 'flicker' of normal website navigation, and removes the need for the browser to re-parse CSS and JavaScript, making it feel more responsive.

Recently I did some work on a Django project that uses jQuery for some AJAX calls to send information back to the database. It was a fairly simple $.post() call, but it got me thinking about Django's template inheritance and how it could be used to render parts of templates and update those client-side without having to render the whole thing.  The idea being, if your base template is complex and has a number of built-in queries or calculations, for example if you have a dynamic navigation menu, why put extra load on Postgres, on the web server, or have the browser reload the CSS, JS, images, or other resources, to load in what could be otherwise static data into a content column?

The idea's a little half-baked, just the result of a little after-hours tinkering over a couple evenings.  Certainly hasn't been fleshed out in a production environment, but seems to work okay in a test.  I probably won't develop it much more, but maybe the concepts will help someone looking for something similar.

There's a few options out there, apparently, between [django-ajax-blocks](https://pypi.python.org/pypi/django-ajax-blocks/0.1a2) (which seems to do something similar to what I'm about to describe) and [Tastypie](http://tastypieapi.org/), which lets you easily build with REST-based frameworks.  Django's usually pretty good about that, having projects available that build functionality on top of it.  But not having researched those at the time, I put together this basic technique for doing the same:

1. Create a replacement template render function that detects AJAX-y requests.
1. Update your page templates to use a variable in {% extends %}.*
1. Create a simple XML base template with the blocks you use in your normal base template.
1. Add a little JavaScript to perform the content switch.

* Yes, this works, which was a bit of a surprise to me.  It's also the part I'm least happy with.  More on that in a bit.

The details...

### Template Render Function

This takes after the handy django.shortcuts.render function.  In fact, it leans on it fairly heavily.

```python
def my_render(request, template, context={}, html_base='main.html', xml_base='main.xml'):
    if request.is_ajax():
        context['base_template'] = xml_base
        return render(request, template, context, content_type='application/xml')
    else:
        context['base_template'] = html_base
        return render(request, template, context)
```

Giving html_base and xml_base as parameters lets views override those.  This then injects a new variable, base_template, into the context passed to it with the appropriate base template.

### Update Page Templates

Your page templates, assuming they now at the top say {% extends 'main.html' %}, replace with {% extends base_template %}.  You shouldn't have to make any other changes to it.

But again, this is the bit I'm least happy about.  It takes the selection out of the page template, and puts it in code.  That takes away some of the decoupling an MVC environment like this is supposed to provide.  Haven't come up with a way around it, though.

### Create XML Base Template

In templates/main.xml (or whatever you want to call it above) create XML nodes for the blocks in your main.html file.  Or at least the blocks your pages will replace:

```xml
&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;content&gt;
 &lt;title&gt;&lt;![CDATA[{% block title %}Django Site!{% endblock %}]]&gt;&lt;/title&gt;
 &lt;main_content&gt;&lt;![CDATA[{% block main_content %}{% endblock %}]]&gt;&lt;/main_content&gt;
&lt;/content&gt;
```

Like your main.html, you can have defaults for the blocks here, such as a default title.

Why XML?  I'd originally envisioned using JSON, but it has escaping rules, of course.  Django, so far as I'm aware, will always drop the contents of a block into place verbatim, without an opportunity to escape it into a JSON string.  That's where XML's CDATA construct came in handy, allowing a segment of HTML to be put right in place.  Assuming, of course, "]]>" doesn't appear in your HTML.

### JavaScript Page Switches

That takes care of the back-end Django bit.  The last bit involves the front end JavaScript that takes care of the page switch/content replacement.  This example leans on jQuery fairly heavily.  In essence we'll: A) take over the link's click event, B) send off an AJAX-type request for the same href, C) set up a callback to do the actual content switch.  Or, to put it another way:

```javascript
$('a.ajax').click(function (e) {
  // Suppress the default navigate event
  e.preventDefault();
  // Instead, do the GET in the background
  $.get(this.href).done(function (response) {
    // The XML is automatically parsed and can be traversed in script
    var contentNodes = response.firstChild.childNodes;
    for (var i = 0; i &lt; contentNodes.length; i++) {
      // Ignore any textNodes or other non-elements
      if (contentNodes[i].nodeType != 1) continue;

      // Handle each XML element appropriately:
      if (contentNodes[i].nodeName == 'title')
        document.title = contentNodes[i].firstChild.nodeValue;
      if (contentNodes[i].nodeName == 'main_content')
        $('#main_content').html(contentNodes[i].firstChild.nodeValue);
    }
  });
});
```

JavaScript, I'll admit, isn't a language I work in all that often.  There's probably a better way of parsing and handling that, but that seemed to work okay in testing.  And, of course, it's fairly bare bones as far as functionality.  But it shouldn't be difficult to add in a spinner, error handling, etc.

Anyway, it was fun.  Even the slightly frustrating update-JS/refresh/try-again cycle.  Again it's still fairly rough, and quite untested at any scale.  But maybe the idea will help someone out there.
