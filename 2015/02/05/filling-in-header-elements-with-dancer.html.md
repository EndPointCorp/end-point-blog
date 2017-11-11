---
author: Jeff Boes
gh_issue_number: 1086
tags: dancer, perl
title: Filling in header elements with Dancer and Template::Flute
---

Inserting content into [Dancer](http://perldancer.org/) output files involves using a templating system. One such is [Template::Flute](http://search.cpan.org/~hornburg/Template-Flute-0.0160/lib/Template/Flute.pm). In its simplest possible explanation, it takes a Perl hash, an XML file, and an HTML template, and produces a finished HTML page.

For a project involving Dancer and Template::Flute, I needed a way to prepare each web page with its own set of JavaScript and CSS files. One way is to construct separate [layout](https://www.blogger.com/blogger.g?blogID=7997313029981170997#) files for each different combination of .js and .css, but I figured there had to be a better way.

Here's what I came up with: I use one layout for all my typical pages, and within the header, I have:

```html
 <link class="additional_style" href="/css/additional.css" rel="stylesheet" type="text/css"/>
 <script class="additional_script" src="/javascripts/additional.js" type="text/javascript">
 </script>
```

The trick here is, there's no such files "additional.css" and "additional.js". Instead, those are placeholders for the actual CSS and JS files I want to link into each HTML file.

My Perl object has these fields (in addition to the other content):

```perl
    $context->{additional_styles}    = [
        { url => '/css/checkout.css' },
        { url => '/css/colorbox.css' },
    ];
    $context->{additional_scripts}   = [
        { url => '/javascripts/sprintf.js' },
        { url => '/javascripts/toCurrency.js' },
        { url => '/javascripts/jquery.colorbox-min.js' },
        { url => '/javascripts/checkout.js' },
    ];
```

while my XML file looks like this:

```xml
<specification>
<list iterator="additional_styles" name="additional_style">
  <param field="url" name="additional_style" target="href"/>
</list>
<list iterator="additional_scripts" name="additional_script">
  <param field="url" name="additional_script" target="src"/>
</list>
</specification>
```

So we have all the elements, but unless you have used all this before, you may not realize how we get the output. (Skip to the punchline if that's not true.)

The XML file is a connector that tells Template::Flute how to mix the Perl hash into the HTML template. Usually you connect things via class names, so in the case of:
```html
<link class="additional_style" href="/css/additional.css" rel="stylesheet" type="text/css"/>
```

the class name in the HTML and the name field in the XML connect, while the iterator field in the XML and the hash key in the Perl hashref do as well. The case of a ~~~
<list>
```
 means that the hash value must be an arrayref of hashrefs, i.e.,
```perl
 {
  "additional_style" => [
    { url => "...", },
    ...,
   ],
 }
```

Important note: if the hash value is undefined, you'll get a run-time error when you try to expand the HTML template, and if you have an empty arrayref, the result of the expansion is an empty string (which is just what you want).

And so, through the magic of Template::Flute, what the browser sees is:

```html
<link class="additional_style" href="/css/checkout.css" rel="stylesheet" type="text/css"/>
<link class="additional_style" href="/css/colorbox.css" rel="stylesheet" type="text/css"/>
<link class="additional_style" href="/css/admin/admin.css" rel="stylesheet" type="text/css"/>...
...
<script class="additional_script" src="/javascripts/sprintf.js" type="text/javascript">
</script>
<script class="additional_script" src="/javascripts/toCurrency.js" type="text/javascript">
</script>
<script class="additional_script" src="/javascripts/jquery.colorbox-min.js" type="text/javascript">
</script>
<script class="additional_script" src="/javascripts/checkout.js" type="text/javascript">
</script>
```


