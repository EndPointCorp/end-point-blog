---
author: "Marco Pessotto"
date: 2022-04-08
title: "Perl Web Frameworks"
tags:
 - perl
 - web
 - mojolicious
 - catalyst
 - dancer
 - interchange
---

### CGI

When I started programming, back in the days, CGI was still widely
used. Usually the Apache webserver would just execute a script or a
binary with some environment variables set and serve whatever the
executable sent to the standard output, while keeping the standard
error in the logs (this simple mechanism can still be used for small
programs, but large applications usually wants to save the start-up
time and live longer than just a request).

At that time, Perl was way more used and it had (and still has) the
[CGI.pm](https://metacpan.org/pod/CGI) module to help the programmer
to get the job done.

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

Of course here the script mixes logic and formatting, and the encoding
it produces by default tells us that this comes from another age...
But still, if you want something not persistent in the machine memory,
which the webserver executes on demand, this is still a viable option.

# Mojolicious

Fast-forward to 2022.

Nowadays Perl is just another language between dozens of them. But
still gets the job done and let you write nice, maintainable code like
any other modern language.

[Mojolicious](https://mojolicious.org/) is currently the top choice if
you want to do web development in Perl. It is an amazing framework,
with a large and active community, and appears to have collected the
best web frameworks have to offer.

Let's hack an app in a couple of minutes, in a single file:

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
(in the "Lite" version) and you declare that the root (`/`) of your
application is executing some code. It populates the "stash" with some
variables, and finally renders a template. If you execute the script,
you get:

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

The nice thing in this example is that we created prototype in a
single file and launched it as a CGI. But we can also launch it as
daemon and visit the given address with a browser.

```
./mojo.pl daemon
[2022-04-08 14:48:42.01827] [163409] [info] Listening at "http://*:3000"
Web application available at http://127.0.0.1:3000
[2022-04-08 14:48:48.53687] [163409] [debug] [CwM6zoUQ] GET "/"
[2022-04-08 14:48:48.53715] [163409] [debug] [CwM6zoUQ] Routing to a callback
[2022-04-08 14:48:48.53752] [163409] [debug] [CwM6zoUQ] Rendering template "index.html.ep" from DATA section
[2022-04-08 14:48:48.53808] [163409] [debug] [CwM6zoUQ] 200 OK (0.001209s, 827.130/s)
```

If you want you can launch it with HTTPS as well, giving it the SSL
certificates:

```
./mojo.pl daemon -l 'https://[::]:8080?cert=./ssl/fullchain.pem&key=./ssl/privkey.pem' -m production
```

For a small application this is already enough and the whole
deployment problem goes away.

Speaking about deployment, Mojolicious has basically no dependencies
beside the core modules, and comes with a lot of goodies, for example
a [non blocking user-agent](https://docs.mojolicious.org/Mojo/UserAgent).

Recently a legacy application needed to do some API call. To speed up
the process, we wanted to make the requests in parallel. And here's
the gist of the code:

```
use Mojo::User-Agent;
use Mojo::Promise;

my $ua = Mojo::UserAgent->new;

sub example {
    my $email = 'test@example.com'
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
}
```

So the bunch of requests are run in parallel and then synced before
returning. Does it remind you of the async JS? Of course. A lot of
common paradigms taken from other languages and frameworks were
implemented here, and you can find the best of them in this nice
package.

But the point here is that it doesn't need dozens of new modules. It's
just a single module in pure Perl that you can even install in your
application tree. This is a huge advantage if you're dealing with a
legacy application which has an old Perl tree and you want to play
safe.

So, if you're starting from scratch, go with Mojolicious. It lets you
prototype fast and doesn't let you down later.

However, starting from scratch is not always an option. Actually, it's
a rare opportunity. There's a whole world of "legacy" working
applications which generate real work and real money. It's simply not
possible or even desirable to throw away something that works for
something that would do the same thing but in a "cooler" way. In ten
years, the way we're coding will look old as well, probably.

### Interchange

Wait. Isn't [Interchange](https://www.interchangecommerce.org) an old
e-commerce platform? Yes, it's not exactly a generic web framework, on
the contrary, it's a specialized one, but it still a framework and you
can still do things in a maintainable fashion. The key is using the
so-called action maps:

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
}
EOR
```

Now, I can't show you a simple script which demonstrate this and
you'll have to take my word for it. Interchange is old, and it shows
its years, but it is actively maintained. It lacks many of the Mojo's
goodies, *but* you can still do modern things in a reasonable way. The
key is to use the action maps, so that code will execute when /jump/
is hit, and the whole path passed to the routine. So you can split at
`/`, apply your logic, and finally either set `$CGI->{mv_nextpage}` to
a file under `pages/` or output the response body with `deliver`.
That's basically the core of what a framework like
[Dancer](https://metacpan.org/pod/Dancer2) does.

### Dancer (1 & 2)

Dancer is basically [Sinatra](https://github.com/sinatra/sinatra)
ported to Perl. As already mentioned, ideas developed in other
languages and frameworks are often ported to Perl, and this is no
exception.

Let's see it in an action:










