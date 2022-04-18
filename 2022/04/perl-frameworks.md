---
author: "Marco Pessotto"
date: 2022-04-08
title: "Perl Web Frameworks"
tags:
 - cgi
 - perl
 - web
 - mojolicious
 - catalyst
 - dancer
 - interchange
 - mvc
---

### CGI

When I started programming, back in the day, CGI was still widely
used. Usually the Apache webserver would just execute a script or a
binary with some environment variables set and serve whatever the
executable sent to the standard output, while keeping the standard
error in the logs (this simple and straightforward mechanism can still
be used for small programs, but larger applications usually want to
save the start-up time and live longer than just a request).

At that time Perl was used far more often than now, and it had (and still
has) the [CGI.pm](https://metacpan.org/pod/CGI) module to help the
programmer to get the job done.

```
#!/usr/bin/env perl

use utf8; 
use strict;
use warnings;
use CGI;

my $q = CGI->new;
print $q->header;
my $name = 'Marco';
print $q->p("Hello $name");
print "\n";
```

And it will output:

```
./cgi.pl
Content-Type: text/html; charset=ISO-8859-1

<p>Hello Marco</p>
```

Here the script mixes logic and formatting and the encoding it
produces by default tells us that this comes from another age... But
if you want something which is seldom used and gets executed on demand
without persisting in the machine's memory, this is still an option.

Please note that there are frameworks which can work in CGI mode, so
there is no reason to use CGI.pm, beside having to maintain legacy
programs.

### Mojolicious

Fast-forward to 2022.

Nowadays Perl is just another language among dozens of them. But it
still gets the job done and lets you write nice, maintainable code like
any other modern language.

[Mojolicious](https://mojolicious.org/) is currently the top choice if
you want to do web development in Perl. It is an amazing framework,
with a large and active community, and appears to have collected the
best concepts that other web frameworks from other languages have to
offer.

Let's hack an app in a couple of minutes in a single file, like during
the CGI days:

```
#!/usr/bin/env perl
use utf8;
use strict;
use warnings;

use Mojolicious::Lite;

get '/' => sub {
    my ($c) = @_;
    $c->stash(name => "Marco");
    $c->render(template => 'index');
};

app->start;

__DATA__
@@ index.html.ep
Hello <%= $name %>

```

Here the structure is a bit different. 

First, there's a Domain Specific Language (DSL) to give you some sugar
(this is the "Lite" version, while the well-structured Mojolicious one
prefers to write class methods) and declare that the root (`/`) of your
application is going to execute some code. It populates the "stash"
with some variables, and finally renders a template which can access
the stashed variables. If you execute the script, you get:

```
./mojo.pl cgi 2> /dev/null
Status: 200 OK
Content-Length: 12
Date: Fri, 08 Apr 2022 12:33:52 GMT
Content-Type: text/html;charset=UTF-8

Hello Marco
```

The logging in the standard error is:

```
[2022-04-08 14:33:52.92508] [163133] [debug] [82ae3iV2] GET "/"
[2022-04-08 14:33:52.92532] [163133] [debug] [82ae3iV2] Routing to a callback
[2022-04-08 14:33:52.92565] [163133] [debug] [82ae3iV2] Rendering template "index.html.ep" from DATA section
[2022-04-08 14:33:52.92610] [163133] [debug] [82ae3iV2] 200 OK (0.001021s, 979.432/s)
```

This is basically what a modern framework is supposed to do.

The nice thing in this example is that we created a single-file
prototype and launched it as a CGI. But we can also launch it as
daemon and visit the given address with a browser (which is how you
should normally deploy it, usually behind a reverse proxy like
[nginx](https://nginx.org/en/).

```
./mojo.pl daemon
[2022-04-08 14:48:42.01827] [163409] [info] Listening at "http://*:3000"
Web application available at http://127.0.0.1:3000
[2022-04-08 14:48:48.53687] [163409] [debug] [CwM6zoUQ] GET "/"
[2022-04-08 14:48:48.53715] [163409] [debug] [CwM6zoUQ] Routing to a callback
[2022-04-08 14:48:48.53752] [163409] [debug] [CwM6zoUQ] Rendering template "index.html.ep" from DATA section
[2022-04-08 14:48:48.53808] [163409] [debug] [CwM6zoUQ] 200 OK (0.001209s, 827.130/s)
```

If you want you can even launch it with HTTPS as well (please note the
syntax to pass the certificates).

```
./mojo.pl daemon -l 'https://[::]:8080?cert=./ssl/fullchain.pem&key=./ssl/privkey.pem' -m production
```

For a small application listening on a high port this is already
enough and the whole deployment problem goes away.

Speaking about deployment, Mojolicious has basically no dependencies
other than the core modules and comes with a lot of goodies, for example
a [non blocking user-agent](https://docs.mojolicious.org/Mojo/UserAgent).

Recently a legacy application needed to make some API calls. To speed up
the process, we wanted to make the requests in parallel. And here's
the gist of the code:

```
package MyApp::Async;

# ... more modules here

use Mojo::UserAgent;
use Mojo::Promise;

# .... other methods here

sub example {
    my $email = 'test@example.com'
    my $ua = Mojo::UserAgent->new;
    foreach my $list ($self->get_lists) {
        my $promise = $ua->post_p($self->_url("/api/v2/endpoint/$list->{code}"),
                                  json => { email => $email })
          ->then(sub {
                     my $tx = shift;
                     my $res = $tx->result;
                     if ($res->code =~ m/^2/) {
                         $self->_update_db($data);
                     }
                     else {
                         die $tx->req->url . ' ' . $res->code;
                     }
                 });
        push @promises, $promise;
    }
    my $return = 0;
    Mojo::Promise->all(@promises)->then(sub { $return = 1 }, sub { $return = 0})->wait;
    return $return;
}
```

So a bunch of requests are run in parallel and then synced before
returning. Does it remind you of Javascript? Of course. A lot of
common paradigms taken from other languages and frameworks were
implemented here, and you can find the best of them in this nice
package.

But the point here is that it doesn't need dozens of new modules
installed or upgraded. It's just a single module in pure Perl that you
can even install in your application tree. This is a huge advantage if
you're dealing with a legacy application which uses an old Perl tree
and you want to play safe.

So, if you're starting from scratch, go with Mojolicious. It lets you
prototype fast and doesn't let you down later.

However, starting from scratch is not always an option. Actually, it's
a rare opportunity. There's a whole world of legacy applications and
they generate real money every day. It's simply not possible or even
desirable to throw away something that works for something that would
do the same thing but in a "cooler" way. In ten years, the way we're
coding will look old anyway.

### Interchange

Wait. Isn't [Interchange](https://www.interchangecommerce.org) an old
e-commerce framework? Yes, it's not exactly a generic web framework,
on the contrary, it's a specialized one, but it's still a framework and
you can still do things in a maintainable fashion. The key is using
the so-called action maps:

```
ActionMap jump <<EOR
sub {
    # get the path parameters
    my ($action, @args) = split(/\//, shift); 

    # get the query/body parameters
    my $param = $CGI->{param};

    # redirect to another page
    $Tag->deliver({ location => $final });

    # or serve JSON
    $Tag->deliver({ type => 'application/json', body => $json_string });

    # or serve a file
    $Tag->deliver({ type => 'text/plain', body => $bigfile });

    # or populate the "stash" and serve a template page in pages/test.html

    $Tag->tmp(stash_variable => "Marco");
    # and in test.html "<p>Hello [scratch stash_variable]</p>
    $CGI->{mv_nextpage} = "test.html"
}
EOR
```

Now, I can't show you a simple script which demonstrates this and
you'll have to take my word for it (we can't go through the
installation process for a demo). Interchange is old, and it shows its
years, but it is actively maintained. It lacks many of the Mojo's
goodies, *but* you can still do things in a reasonable way. The key is
to use the so-called action maps. In the example the code will execute
when a path starting with `/jump/` is requested. The whole path is
passed to the routine, so you can split at `/`, apply your logic, and
finally either set `$CGI->{mv_nextpage}` to a file in the `pages`
directory or output the response body directly with `deliver`. This
way you can easily build, as a classical example, an API.

It's a bit of a poor man's
[MVC](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
but it works. That's basically the core of what a framework like
[Dancer](https://metacpan.org/pod/Dancer2) does.

### Dancer (1 & 2)

Dancer is basically Ruby's
[Sinatra](https://github.com/sinatra/sinatra) ported to Perl. As
already mentioned, ideas developed in other languages and frameworks
are often ported to Perl, and this is no exception.

Let's see it in an action:

```
#!/usr/bin/env perl
use strict;
use warnings;
use Dancer2;
 
get '/' => sub {
    my $name = "Marco";
    return "Hello $name\n";
};
 
start;
```

Start the script:

```
Dancer2 v0.400000 server 22969 listening on http://0.0.0.0:3000
```

Try it with `curl`:

```
$ curl -D - http://0.0.0.0:3000
HTTP/1.0 200 OK
Date: Mon, 11 Apr 2022 07:22:18 GMT
Server: Perl Dancer2 0.400000
Server: Perl Dancer2 0.400000
Content-Length: 12
Content-Type: text/html; charset=UTF-8

Hello Marco
```

If in the script you say `use Dancer;` instead of `use Dancer2`, you get:


```
$ curl -D - http://0.0.0.0:3000
HTTP/1.0 200 OK
Server: Perl Dancer 1.3513
Content-Length: 12
Content-Type: text/html
X-Powered-By: Perl Dancer 1.3513

Hello Marco
```

The Dancer's core doesn't do much more than routing. And you'll also
notice that the syntax is very similar to Mojolicious::Lites. So to
get something done you need to start installing plugins which will
provide the needed glue to interact with a database, work with your
template system of choice, and more.

Today you would wonder why you should use Dancer and not Mojolicious,
but when Dancer was at the peak of its popularity the games were still
open. There were plenty of plugins being written and published on CPAN.

Now, it was probably around 2013 when the Dancer's development team
decided to rewrite it to make it better. The problem was that plugins
and templates needed to be adapted as well.

I'm under the impression that the energy got divided and the momentum
was lost. Now there are two codebases and two plugin namespaces which
do basically the same thing, because for the end user there is not
much difference.

### Catalyst

So what was attracting people to Dancer? When Dancer came out, Perl
had a great MVC framework, which is still around,
[Catalyst](http://catalyst.perl.org/) (please note that the main
Mojolicious developer was in the Catalyst team).

Now, the problem is that to get started with Catalyst, even if it has
plenty of documentation, you need to be already acquainted with a lot
of concepts and technologies. For example, the
[tutorial](https://metacpan.org/dist/Catalyst-Manual/view/lib/Catalyst/Manual/Tutorial/03_MoreCatalystBasics.pod)
starts to talk about
[TemplateToolkit](http://www.template-toolkit.org/) and
[DBIC](https://metacpan.org/pod/DBIx::Class) very early.

These two modules are great and powerful and they deserve to be
studied, but for someone new to modern web development, or even to
Perl, it feels (and actually is) overwhelming.

So, why would you choose Catalyst today? Catalyst has the stability
which Mojo, at least at the beginning, lacked, while the
back-compatibility is a priority for Catalyst. The other way to look
at this is that Catalyst doesn't see much
[development](https://metacpan.org/dist/Catalyst-Runtime/changes), but
someone could see this as a feature.

Even if Catalyst predates all the hyper-modern features that Mojo has,
it's still a modern framework, and a good one. I can't show you a self
contained script (you need a tree of files), but I'd like to show you
what makes it very nice and powerful:


```
package MyApp::Controller::Root;

use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller'; }

# start the chain with /foo/XX
sub foo :Chained('/') CaptureArgs(1) {
    my ($self, $c, $arg) = @_;
    $c->stash(name => "$arg");
}
 
# /foo/XX/bar/YY
sub bar :Chained('foo') Args(1) {
    my ($self, $c, $arg ) = @_;
    $c->detach($c->view('JSON'));
}

# /foo/XX/another/YY 
sub another :Chained('foo') Args(1) {
    my ($self, $c, $arg ) = @_;
    $c->detach($c->view('HTML'));
}
```

So, if you hit `/foo/marco/bar/test` the second path fragment will be
processed by the first method (`CapturedArgs(1)`) and saved in the
stash. Then the second `bar` method will be chained to it and the
`name` will be available in the stash. The last method will be hit
with `/foo/marco/another/test2`. (Incidentally, please note that
Mojolicious has
[nested](https://docs.mojolicious.org/Mojolicious/Guides/Routing#Nested-routes)
routes as well).

Now, I think it's clear that in this way you can build deep hierarchies
of paths with reusable components. This works really great with the
[DBIx::Class](https://metacpan.org/pod/DBIx::Class) ORM, where you can
chain queries as well. As you can imagine, this is far from a simple
setup. On the contrary, this is an advanced setup for people who
already know their way around web frameworks.

### Conclusion

So, to sum up this excursion in the amazing land of the Perl web
frameworks: if you build something from scratch, go with Mojolicious,
it's your best bet. If nothing else, it's super-easy to install, with
basically no dependencies. However, there's no need to make a religion
out of it. Rewriting code without a clear gain is a waste of time and
money. A good developer should still be able to write maintainable
code with the existing tools.

