---
author: Jeff Boes
title: jQuery Auto-Complete in Interchange
github_issue_number: 348
tags:
- interchange
- javascript
- jquery
date: 2010-09-13
---



“When all you have is a hammer, everything looks like a nail.”

Recently, I’ve taken some intermediate steps in using jQuery for web work,
in conjunction with Interchange and non-Interchange pages. (I’d done some
beginner stuff, but now I’m starting to see nails, nails, and more nails.)

Here’s how easy it was to add an auto-complete field to an IC admin page.
In this particular application, a \<select\> box would have been rather unwieldy, as there were 400+ values that could be displayed.

```
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"
type="text/javascript"></script>

<script type="text/javascript" src="http://dev.jquery.com/view/trunk/plugins/autocomplete/lib/jquery.bgiframe.min.js"></script>

<script type="text/javascript" src="http://dev.jquery.com/view/trunk/plugins/autocomplete/lib/jquery.dimensions.js"></script>

<script type="text/javascript" src="http://dev.jquery.com/view/trunk/plugins/autocomplete/jquery.autocomplete.js"></script>
```

That’s the requisite header stuff. Then you set up the internal list of
autocomplete terms:

<script type="text/javascript">

    $('document').ready(function(){

        var auto_list = "[perl]...[/perl]".split(" ");

        $('input[name="auto_field"]').autocomplete(auto_list);

    });

</script>

The [perl] block just needs to emit a space-delimited list of the autocomplete terms. For instance,

[perl table="foo"]

  return join(' ', map { $_->[0] }

    @{ $Db{foo}->query('SELECT keycol FROM foo ORDER BY 1') });

[/perl]

