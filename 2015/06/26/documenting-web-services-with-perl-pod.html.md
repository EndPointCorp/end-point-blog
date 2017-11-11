---
author: Jeff Boes
gh_issue_number: 1137
tags: ajax, dancer, javascript, perl
title: Documenting web services with Perl POD and AJAX
---



Perl POD is a handy, convenient, but low-tech approach to embedded documentation. Consider a web service in [Dancer](http://www.perldancer.org):

```perl
get time => sub {
  return scalar(localtime());
};
```

(Disclaimer: my actual use-case of this technique was even more legacy: I was documenting [Interchange Actionmaps](http://interchange.rtfm.info/icdocs/config/ActionMap.html) that returned images, JSON, etc.)

Your application might have several, or even dozens of these, with various parameters, returning data in JSON or TXT or CSV or who-knows-what.
I chose to document these in Perl [POD (Plain Old Documentation)](http://perldoc.perl.org/perlpod.html) format, e.g.,

```nohighlight

=pod

=head1 time

Retrieves the current time

=over 3

=item Parameters

None.

=item Example

=begin html

<script src="/js/example-time.js" type="text/javascript"></script>

=end html

=back

=cut

```

This block gets inserted right in-line with the web service code, so it's immediately obvious to anyone maintaining it (and thus has the best chance of being maintained if and when the code changes!). Now I can generate an HTML page directly from my Perl code:

```shell
$ pod2html MyPackage.pm
```

Your output looks something like this (excerpted for clarity):

> 
> 
> 
> ### [time]()
> 
> 
> 
> 
> Retrieves the current time
> 
> 
> 
> **[Parameters]()**
> 
> 
> 
> 
> None.
> 
> 
> 
> 
> **[Example]()**
> 
> 

Where the magic comes in is the Javascript code that allows an in-line example, live and accurate, within the documentation page. You'll actually get something more like this:

> 
> 
> 
> ### [time]()
> 
> 
> 
> 
> Retrieves the current time
> 
> 
> 
> **[Parameters]()**
> 
> 
> 
> 
> None.
> 
> 
> 
> 
> **[Example]()**
> 
> 
> <input type="submit" value="Get data">
> <input type="button" value="Hide result" name="hide">
> 
> (results appear here)
> 
> 
> 

Note that the code I have below is not factored by choice; I could move a lot of it out to a common routine, but for clarity I'm leaving it all in-line. I am breaking up the script into a few chunks for discussion, but you can and should construct it all into one file (in my example, "js/example-time.js").

```javascript
/* example-time.js */
$(document).ready(
  function(){
    $('script[src$="/example-time.js"]').after(
"<form action='\"/time\"'>" +
/* Note 1 */
"<input data\"="" type='\"submit\"' value='\"Get'/>" +
"<input name="hide" none\"="" result\"="" style='\"display:' type='\"button\"' value='\"Hide'/>" +
"</form>" +
"<div id='\"time-result\"'></div>"
    );
```

Note 1: This being a painfully simple example of a web service, there are no additional inputs. If you have some, you would add them to the HTML being assembled into the <form> tag, and then using jQuery, add them below to the url parameter, or into the data structure as required by your particular web service.

This step just inserts a simple <form> into the document. I chose to embed the form into the Javascript code, rather than the POD, because it reduces the clutter and separates the example from the web service.

```javascript
    var $form = $('form[action="/time"]');
    $form.submit(function(){
      $.ajax(
        {
          'url': $form.attr('action') /* Note 1 also */,
          'data': {},
          'dataType': 'text',
          'async': false,
          'success':
             function(data){
                 $('#time-result').html($('<pre;//>').html(data))
                     .addClass('json');
             },
```

Here we have a submit handler that performs a very simple AJAX submit using the form's information, and upon success, inserts the results into a result <div> as a pre-formatted block. I added a "json" class which just tweaks the font and other typographic presentation a bit; you can provide your own if you wish.

I'm aware that there are various jQuery [plug-ins](http://malsup.com/jquery/form/) that will handle AJAX-ifying a form, but I couldn't get the exact behavior I wanted on my first tries, so I bailed out and just constructed this approach.

```javascript
          'error':
             function(){
                 $('#time-result').html('Error retrieving data!')
                     .removeClass('json');
             },
/* */
```

(That stray-looking comment above is just a work-around for the syntax highlighter.)

Error handling goes here. If you have something more comprehensive, such as examining the result for error codes or messages, this is where you'd put it.

```javascript
          'complete':
             function(){
                 $form.find('input[name="hide"]').show();
             }
         }
      );
      return false;
    }).find('input[type="button"]').click(function(){
      $('#time-result').html('');
    });
  }
);
```

And just a bit of UI kindness: we have a "hide" button to make the example go away. Some of my actual examples ran to dozens of lines of JSON output, so I wanted a way to clean up after the example.


