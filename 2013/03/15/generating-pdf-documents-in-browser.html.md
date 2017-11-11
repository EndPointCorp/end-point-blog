---
author: Kamil Ciemniewski
gh_issue_number: 769
tags: javascript
title: Generating PDF documents in the browser
---



### What you will learn.

- How to generate PDF documents in the browser with JavaScript
- How to generate them out of *normal* HTML
- How to *open* those PDFs in new windows
- How to render them inline inside the DOM

### Introduction

Every once in a while as web developers we face the challenge of providing PDF documents for the data we have persisted in the database.

The usual approach is to:

- generate the document with a library / DSL in the language of the backend
- or - generate *normal html* view and use a utility like [wkhtmltopdf](https://code.google.com/p/wkhtmltopdf/)

That works nice, but what if you’re developing an [SPA](http://en.wikipedia.org/wiki/Single-page_application) app which only consumes JSON data from its backend? Imagine a scenario when the backend isn’t capable of producing responses other than JSON data. What could you do there?

### The solution

Thanks to some very bright folks behind the [jsPDF](http://jspdf.com/) library we have both above mentioned options right inside the browser.

I strongly encourage you to visit their website. There is a nice live coding editor set up which reflects in real time the PDF your code is producing.

### Using the DSL

The whole process looks like this:

```python
# 1. create jsPDF object:
doc = new jsPDF()

# 2. put something interesting in there:
doc.setFontSize(22)
doc.text(20, 20, 'This is a title')
doc.setFontSize(16)
doc.text(20, 30, 'This is some normal sized text underneath.')

# 3. choose some useful outlet:
doc.output('dataurlnewwindow', {})
```

### Where is the documentation?

One thing I didn’t like about the experience which was really great otherwise, was the fact that you could browse the Internet for hours without luck, looking for some useful docs for the library.

For all of you who don’t know the shortcut yet, here it is:

```bash
git clone https://github.com/MrRio/jsPDF.git
```

And in the *doc* directory you will find nicely generated docs out of the project sources - very neat!

### Can I generate it just from HTML?

Yes you can. On the project’s website the authors are warning us that this feature is still **experimental**. But I have to say that last time I used it, all went well and the code produces nice PDF to this day (yay!).

```python
doc.fromHTML $('.report_web').get(0), 10, 10,
  'width': 170,
  'elementHandlers': 
    'LI': (el, renderer) =&gt;
      if renderer.y &gt; 250
        doc.addPage()
        renderer.y = 10
      else
        renderer.y += 10
      false
    'H1': (el, renderer) =&gt;
      doc.setFontSize(14)
      doc.setFontStyle('bold')
      doc.text($(el).text(), 10, renderer.y)
      doc.setFontSize(12)
      doc.setFontStyle('normal')
      true
doc.output 'dataurlnewwindow', {}
```

Take a look at the code above. *#fromHtml* method takes the DOM element, margins, and a hash of options. From my experience the *elementHandlers* attribute seems to be mandatory (I got errors without it).

Every element handler is just a pair of capitalized tag name and the function which takes DOM element and the renderer context.

The *renderer* variable contains data of the current paragraph, the pdf internal object, settings object and x and y. You have to remember to **change x and y variables yourself** after creating some content.

One last thing to remember is that the handler can return either *true* or *false*. If it returns *true*, then the engine will not create content out of the given DOM element on its own. Otherwise, after your handler finishes its execution, the engine will generate the content for you. So you can use those handlers to munge a few things in the output document or you can take over the whole control and do it *your way*.

### Open PDF output in a new window

You may have notice in one of above examples, that we were simply creating new windows with PDF documents there.

To recap, opening PDF documents in new window:

```python
doc.output 'dataurlnewwindow', {}
```

### Render PDFs in the DOM

Nesting the PDF document inside the DOM seems way cooler. To do so:

```python
data = doc.output 'dataurlstring', {}
$('#report').html "&lt;iframe src='#{data}'&gt;&lt;/iframe&gt;"
```

You will notice that the *#output* method takes a string which tells it how you’d like to generate the PDF. If you specify the **‘dataurlstring’** it will return a string containing the url data you use in your iframe. That is how the last example works.

There is much more to jsPDF than shown in this short post. If you’re interested, you can browse the docs included in the projects repository. There are a lot of useful methods for creating almost any type of document you would want.


