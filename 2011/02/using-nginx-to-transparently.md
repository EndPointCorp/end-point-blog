---
author: David Christensen
title: Using nginx to transparently modify/debug third-party content
github_issue_number: 407
tags:
- browsers
- camps
- interchange
- javascript
- linux
- testing
- tips
date: 2011-02-06
---



In tracking down a recent front-end bug for one of our client
sites, I found myself needing to use the browser’s JavaScript debugger
for stepping through some JavaScript code that lived in a mix of
domains; this included a third-party framework as well as
locally-hosted code which interfaced with—​and potentially
interfered with—​said third-party code. (We’ll call said code
foo.min.js for the purposes of this article.) The
third-party code was a feature that was integrated into the client
site using a custom domain name and was hosted and controlled by the
third-party service with no ability for us to change directly. The
custom domain name was part of a chain of CNAMEs which eventually
pointed to the underlying *actual* IP of the third-party service, so
their infrastructure obviously relied on getting the Host
header correctly in the request to select which among many clients was
being served.

It appeared as if there was a conflict between code on our site and
that imported by the third party service. As part of the debugging
process, I was stepping through the JavaScript in order to determine
what if any conflicts there were, as well as their nature (e.g.,
conflicting library definitions, etc.). Stepping through our code was
fine, however the third-party’s JS code was (a) unfamiliar, and (b)
minified, so this had the effect of putting all of the JavaScript code
more-or-less on one line, which made tracing through the code in the
debugger much less useful than I had hoped.

My first instinct was to use a JavaScript beautifier to reverse the
minification process, but since I had no control over the code being
included from the third-party service, this did not seem to be
directly feasible. The third-party code was deployed only on our
production site and relied on hard-coded domains which would make
integrating it into one of our development instances challenging since
we had no control over the contents of the returned resources. Since
the relevant feature (and subsequent bugs) was only on the production
site, making extensive modifications to how things were done and
potentially breaking that or other features for users while I was
debugging was obviously out as an option.

Enter nginx. I’ve been doing a lot with nginx lately as far as
using it as a reverse proxy cache, so it’s been on my mind lately. So
I came up with this technique:

1. Look up the IP address for the third-party’s domain name (used for later purposes).
1. Install nginx on localhost, listening to port 80.
1. Modify /etc/hosts to point the third-party’s domain name to the nginx server’s IP (also localhost in this case).
1. Configure a new virtual host with the following logical constraints:

        <ul>
          <li>We want to serve specific files (the beautified JavaScript) from our local server.
          <li>We want any other request going through that domain to be passed-through transparently, so neither the browser nor the third-party server treat it differently.
        </ul>

Given these constraints, this is the minimal configuration that I came up with (the interesting parts are located in the server block):

/etc/hosts:

```plain
example.domain.com 127.0.0.1
```

nginx.conf:

```plain
worker_processes 1;

events {
    worker_connections 10;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    
    server {
        server_name example.domain.com;
        root /path/to/local_root;

        try_files $uri @proxied;

        location @proxied {
            proxy_set_header Host $http_host;
            proxy_pass http://1.2.3.4;
        }
    }
}
```

Once I had the above configured/setup, I downloaded/saved the
foo.min.js file from the third-party service, ran it through
a JS beautifier, and saved it in the local nginx’s cache root so it
would be served up instead of the actual file from the third-party
service. Any other requests for static resources (images, other
scripts, etc) would pass-through to the third-party server, so I had
my nicely-formatted JavaScript code to step through, the production site
worked as normal for anyone else despite potential local changes to
the file on my end (i.e., adding JavaScript alert() calls to the
file, and no one was the wiser.

### A few notes

The try_files directive instructs nginx to first look for
a file named after the current URI (foo.min.js in our
example) in our local cache, and if this is not found, then fallback
to the proxied location block; i.e., relay the request to the original
upstream server. We explicitly set the Host header on the
proxy request because we want the request to behave normally with
respect to name-based hosting, and provide the saved IP address to
contact the server in question.

We only needed to preserve/lookup the upstream server’s IP address
because we’re running the nginx server on localhost, so if we used a
domain name the lookup would return the same IP defined in
/etc/hosts; if the nginx server was running on a different
machine, you would be able to just use the domain name as both the
server_name and the proxy_pass parameters and set
the entry for the host in your local /etc/hosts file to the
IP of the nginx server.

A possible extension would be to detect when an upstream request
matched a minified URL (via a location ~ \.min\..*\.js$
block) and automatically beautify/cache the content in our local
cache. This could be accomplished via the use of an external FastCGI
script to retrieve, post-process, and cache the content.

This technique can also be used when dealing with testing changes
to a production site on which you are unable or unwilling to make
potentially disruptive changes for the purposes of testing static
resources. (JavaScript seems the most obvious application here, but this
could apply to serving up images or other static content which would
be resolvable by the local cache.)

I always need to remind myself to undo changes to
/etc/hosts as soon as I’m done testing when using tricks like
these. Particularly in something like this which is more-or-less
transparent, the behavior would be functionaly identical as long as
code/scripts on the third-party site stayed the same, but could easily
introduce subtle bugs if the third-party services made changes to
their codebase. Since our local copies would mask any remote changes
for those non-proxied resources, this could be very confusing if you
forget that things are set up this way.


