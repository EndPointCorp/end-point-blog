---
author: Jeff Boes
gh_issue_number: 862
tags: dancer, perl
title: 'First Dance: a Gentle Introduction to Dancer.pm for Web Services'
---

I’ve been dabbling in Dancer ([Version One](http://search.cpan.org/~yanick/Dancer-1.3118/lib/Dancer.pm), not so much [Version Two](https://web.archive.org/web/20131119231012/http://search.cpan.org/~sukria/Dancer2-0.10/lib/Dancer2.pm)). Our first opportunity to create a production-worthy Dancer application just rolled out with encouraging results, so I thought I would outline some things we tried, and things we learned.  Don’t worry if you don’t know a thing about Dancer; I’ll educate you a little as we go along.

First, some background. This application was a re-host and rewrite of an existing application written in Javascript and plain old CGI Perl scripts, returning either HTML or fairly simple JSON objects. Even the database it connected to was ancient DBM files. Those files were created by extracting data from the main website’s database, so that part was easy to replace — we just had to use the extraction queries (mostly) to connect directly.

We chose Dancer as the platform for this effort because of its purely Perl footprint, and its relatively easy deployment.

Since I didn’t really want to rewrite the front-end Javascript code, I left that mostly as-is and concentrated on replacing the CGI scripts. The first step was to move all their code into a non-Dancer Perl module, which communicated with the outside world entirely in the form of hashrefs:

```perl
sub do_something_great {
    my $opt = shift;
    my $output = {};
    # do something great!
    return $output;
}
```

Next, as a stop-gap measure, I replaced the innards of all the CGI scripts to turn CGI arguments into a hashref and call my new processing stuff. Note that so far, no actual Dancer code has been involved. This was intentional; since my Dancer expertise was still a bit thin, I wanted to have as few app-caused problems as possible, when I started Dancing.

But now we should stop for a moment and learn just enough about Dancer to be less dangerous.

Dancer (details at the first link in this article) is a web application framework: in essence, it’s a way to convert URLs into data. You feed in a URL, you get back a web page, a structure, maybe a side effect or three. In order to connect your application to a browser, you need a series of *routes*:

```perl
package MyApp::Routes;
use Dancer;

get '/index.html' => sub {
    print 'hello, world';
}
```

Dancer sets up some easy-to-grasp syntax that lets you associate a clump of Perl code (an anonymous sub, in the example above) with a URL and a method. Here, a GET of “/index.html” runs the code, and sends the output back to the browser.

```perl
...
post '/myapp/do_this.html' => sub {
    do_this(param->{foo});
    return q{It's done.};
};
```

Likewise, we can specify more complex URLs (such as “/myapp/do_this.html?foo=bar”), with POST methods, and access the CGI parameters via the param() function. It just returns a hashref, which we can address as shown.

Dancer provides quite a bit of support infrastructure: config files, database connections, plug-ins for templating HTML or other output, etc. Since this article is a Gentle Introduction, I refer you to the link cited above if you want to delve deeper.

Now it was pretty simple to make gradual progress: I’d eliminate one CGI script at a time, replacing it with a Dancer route (stored separately from my main processing module, so that the processing could continue to be ignorant of Dancer). Most of the routes were very simple, since the paths they had to recognize were simple and straightforward, with simple CGI parameter lists. E.g.,

```perl
get '/notes.html' => sub {
    my $context = MyApp::get_notes({
        dbh    => database(),
        order  => params->{order},
        raw    => 1,
    });
    template 'notes', $context, { layout => 'plain' };
};
```

This example is one of the routes that produces HTML. The “template” built-in is just a layer wrapped around your preferred templating system (such as Template::Toolkit); it looks for a template file called “notes”, using a set of values specified by “$context”, and wraps the result in a “layout” file called “plain”.

(At the risk of grossly oversimplifying: your “template” can be thought of as all of your output HTML document within the <body> tag, while the “layout” is everything else, with a spot in the middle for your template’s output.)

By contrast, one simple route that is designed to return JSON to the Javascript side:

```perl
get '/orders.html' => sub {
    my $orders = MyApp::get_orders({
        dbh    => database(),
        date   => params->{date},
    });
    return to_json($orders || [], { pretty => params->{pretty} // 0 });
};
```

We had to make some adjustments to our Apache configuration to make this all work.

```
RewriteRule    ^/D/myapp/(.*) http://$SOME_ADDR:5001/$1 [P]
```

As you can see here, we decided to set up the Dancer app as a service on a particular port, and we settled on a particular prefix for our webservice requests to distinguish them from other traffic. All the requests in the Javascript were adjusted to this new style.

Our main Dancer application has the usual one-liner construction*:

```perl
dance;
```

*Okay, totally not true. For this application, there was a ton of file-parsing and environment-loading to do first, but it was all just a big work-around for some very specific things needed in the app, and not really anything to do with Dancer per se.

Now, we added one more layer to this: [Starman](http://search.cpan.org/~miyagawa/Starman-0.4008/script/starman). This provided us with a way to simply wrap our Dancer application with the necessary extra bits to turn it into a “service”. That way it starts and stops with a command line interface, logs to a particular path, doesn’t just quit if a user session is ended, etc.

I don’t have enough background to describe it more than that; hopefully, we’ll have a follow-on post here about Starman from one of my colleagues with more “chops”, soon.  One thing we learned at the cost of some sanity was: * Don’t put an “exit” statement in your Dancer script if you plan to use Starman*. We never learned why this messed it up, but I assume it’s got something to do with Starman absorbing your code into itself and turning it into a Perl subroutine.


