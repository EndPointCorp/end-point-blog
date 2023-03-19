---
author: "Jon Jensen"
title: "Interchange rust_link connector"
date: 2023-03-06
tags:
- interchange
- rust
github_issue_number: 1940
---

![Photograph of several layers of blacktop road with cracks and shadows](/blog/2023/03/interchange-rust_link/20220122_212608-sm.webp)

<!-- Photo by Jon Jensen -->

The Interchange ecommerce system recently reached 27 years old, measuring from the first public release of its predecessor MiniVend by its creator Mike Heins. It is still hard at work in quite a few ecommerce sites, serving pages, accepting and processing orders, managing warehouse logistics, and more. That is quite an accomplishment in the software world!

### The Interchange server/​daemon

Interchange is written in Perl and runs on Linux and other Unix-like servers as a daemon (persistent background process) that listens for requests. Why does it need to run as a daemon?

Like many applications, Interchange starts with a relatively slow initialization procedure that takes a couple of seconds to compile code, load modules, read configuration, connect to databases, and validate everything. We want it to do that only once when the daemon is started, and not for each user request, so it can make quick responses.

### Web server connector

General-purpose web servers normally sit in front of an application server, optimized to make speedy encrypted TLS sessions for HTTPS, control access to resources, log requests, redirect old URLs, route traffic to various applications, and directly serve static files such as HTML, CSS, JavaScript, and images.

How does the web server talk to the Interchange application server? Several protocols to do that would later become common, including:

* FastCGI (1996)
* Apache JServ Protocol or AJP (1997) for the Java world
* HTTP protocol reverse proxying for Ruby on Rails and eventually most other platforms

But in 1995 when Interchange was created, there was no widely-used standard, so it used its own custom protocol implemented in a small CGI program.

The data flows through these steps:

1. A user makes a request with a web browser to a web server, commonly Apache `httpd`.
1. The web server runs a new instance of the link program and passes request information to it.
1. The link program reformats the request into Interchange link protocol.
1. It then sends the request to the Interchange server.
1. It receives back a response from Interchange.
1. It sends the response to the web server.
1. It exits.
1. The web server sends the response back to the user's browser.

### Interchange link protocol

The Interchange link protocol uses plain text divided into lines to pass its information.

There are 2 sections:

* `arg` for command-line arguments, now rarely used, but long ago where search text appeared before the advent of HTML forms
* `env` for environment variables.

After each section label is the number of items in that section.

Then that many items are given on one line each, beginning with the number of bytes in the value, followed by a space and then the value.

Finally an `end` section concludes the preliminary values, and then the HTTP response body, if any, follows unmodified after the `entity` label and its length in bytes.

Here is an example request with an empty request body, as the CGI link program passes it to Interchange:

```plain
arg 0
env 29
52 CONTEXT_DOCUMENT_ROOT=/opt/homebrew/var/www/cgi-bin/
24 CONTEXT_PREFIX=/cgi-bin/
35 DOCUMENT_ROOT=/opt/homebrew/var/www
25 GATEWAY_INTERFACE=CGI/1.1
97 HTTP_ACCEPT=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
34 HTTP_ACCEPT_ENCODING=gzip, deflate
35 HTTP_ACCEPT_LANGUAGE=en-US,en;q=0.5
26 HTTP_CONNECTION=keep-alive
10 HTTP_DNT=1
23 HTTP_HOST=ruka.lan:8080
32 HTTP_UPGRADE_INSECURE_REQUESTS=1
86 HTTP_USER_AGENT=Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0
50 MINIVEND_SOCKET=/Users/user/interchange/etc/socket
18 PATH=/bin:/usr/bin
13 QUERY_STRING=
25 REMOTE_ADDR=192.168.1.215
17 REMOTE_PORT=36534
18 REQUEST_METHOD=GET
19 REQUEST_SCHEME=http
27 REQUEST_URI=/cgi-bin/strap1
52 SCRIPT_FILENAME=/opt/homebrew/var/www/cgi-bin/strap1
27 SCRIPT_NAME=/cgi-bin/strap1
24 SERVER_ADDR=192.168.1.59
28 SERVER_ADMIN=you@example.com
20 SERVER_NAME=ruka.lan
16 SERVER_PORT=8080
24 SERVER_PROTOCOL=HTTP/1.1
17 SERVER_SIGNATURE=
36 SERVER_SOFTWARE=Apache/2.4.56 (Unix)
end
```

Note that the CGI specification has HTTP request headers passed in environment variables beginning with `HTTP_` followed by the header name with `-` replaced by `_` and all letters capitalized.

The other environment variables give information about the request and context from the web server.

The environment variables appear in no particular order, but I sorted them here for readability.

### Interchange link implementations

Several implementations of this link functionality exist:

* Two sibling programs named `vlink` (for UNIX sockets in the filesystem) and `tlink` (for TCP sockets on the IP network), written in C and compiled, giving fast startup time and run speed
* Perl equivalents named `vlink.pl` and `tlink.pl` which are easy to customize and need no compilation, but are comparatively slow, adding ~100 ms or more to each request
* A Perl module `Interchange::Link` that runs precompiled in the Apache `httpd` module `mod_perl` and supports both UNIX and TCP sockets
* A compiled C module `mod_interchange` that also runs in the Apache `httpd` server and supports both UNIX and TCP sockets

You can even run Interchange entirely inside Apache `mod_perl` such that no connector link program is needed. But that has been only rarely used in production because it tightly couples Interchange with the web server and means it runs the application as the web server operating system user, which is not ideal for security.

After all these years, the original `vlink` compiled C program remains the default and popular way to connect a web server via CGI to Interchange. It is simple to use, fairly fast, and works with any web server that supports the CGI protocol.

### Enter Rust

The C `vlink` program isn't broken, so we don't really need to fix it. But occasionally we want to customize some part of the `vlink` behavior. Doing so in C can take more work than in more modern languages, depending on the programmer and what changes are needed.

But more importantly, programming in C introduces risk of bugs that could affect every request. C code is fertile ground for unsafe memory handling bugs that often lead to security problems.

Tim Hutt reviewed all the documented bugs of the `curl` project and found that over half were memory errors, and he noted that Google found that 70% of Chrome’s high-severity security bugs are memory errors. That is despite some of the world's extremely talented and careful programmers working on those projects!

These are the kinds of errors that the programming language Rust eliminates by disallowing such code at compilation time. Plenty of other new languages have cropped up in the past decade or so, vying to replace C and/or C++ and be safe from memory errors while retaining speed and low-level machine access by producing compiled native machine code: Go, Swift, Zig, Nim, and V are a few competitors, alongside Rust.

Rust is one of the more complex ones because you have to think about memory management instead of relying on a garbage collector. But that also can make it one of the highest performers using the least amount of memory. Rust gets plenty of press, much of it enthusiastic, so you can go read about it on your own if you'd like to learn more!

So two years ago I decided to port the `vlink` program to Rust so I could see how much work it took, how pleasant it was, and how fast and memory-efficient the resulting code was. Porting the link program to one of those other new languages would also be fun, but I haven't done that yet!

### rust_link

I called this program `rust_link`. Initially I made it as simple as possible, just a proof of concept: It consisted of one long function, had a hardcoded path to the Interchange UNIX socket file, and it died ungracefully on any error.

It came together fairly quickly and was fun to write, so I made it configurable via environment variables that can be set in the web server, added error handling, and broke it into smaller functions like the original `vlink` has.

Then I came across the Rust crate (Rust's term for a module) called `multisock`, which wraps up UNIX and INET socket support in a single package. Using that made it straightforward to merge `vlink` and `tlink` into a single program.

Most of the other link programs retry connecting to the Interchange socket every 1 or 2 seconds for something like 30 seconds. This is to handle gracefully a brief outage while the Interchange server is being restarted. However, if instead the Interchange server was overloaded or entirely down, this could lead to a big backlog of CGI link processes. I implemented this retry functionality too, and decided to have it check twice as often, but only for a maximum of 10 seconds. That still gives plenty of time for the link program to retry during a restart of the Interchange daemon, but lets it fail faster when the daemon isn't likely to come back.

There is one HTML document in the program, for an HTTP 503 error response body. Putting that HTML text directly in the code would mean using pesky `\` string escapes for quotation marks, newlines, etc., and then most text editors are unable to highlight the HTML syntax for readability. Since Rust has the easy `include_str!` macro, I put the HTTP 503 error response HTML body into a separate `503.html` file for simpler editing.

### Rust impressions

I was still new to Rust as I wrote this program, so there were various learning bumps along the way. It was a fun project. *The Rust Programming Language* book is excellent, and it is free online and also available in print.

One developer I read describing the experience of writing Rust code said that it can involve a lot of wrestling with the compiler to make it happy with variable lifetimes (borrowing and ownership), types, traits, and other details, but that once a program compiled, it usually worked without flaw.

I found that to most often be the case for me with `rust_link`. I had to correctly separate different sorts of data with distinct types for:

* byte arrays for the data sent from and to the web server over stdin and stdout streams
* "OS strings" for environment variable names & values and file paths & names
* UTF-8 strings in source code, messages and string-link type conversions

This required more thoughtful consideration and work up front, but eliminated the possibility of things later going wrong because of sloppiness about exactly what kind of data we have in each case.

The `rustc` compiler is very helpful in pointing the way with detailed error messages noted in relevant excerpts of the problem code, and gives references to further reading in the documentation.

### Testing in Rust

The Rust ecosystem and documentation aim to make testing a natural part of development, and as easy as possible. So I wrote unit tests to exercise some of my helper functions for representing numbers as strings for the wire protocol, parsing environment variable values into sockets, and getting errors where expected.

I also wrote a multi-threaded integration test to exercise sending the simplest response over a socket and verifying what is received on the other side. This is still very basic and could be fleshed out with more arguments, a response body with and without a CGI-specified `CONTENT_LENGTH`, etc.

Being able to run some tests is nice when first compiling the program for another platform, as I did here:

```plain
❯ cargo test
   Compiling rust_link v1.0.0 (/Users/user/repos/interchange/dist/src/rust_link)
    Finished test [unoptimized + debuginfo] target(s) in 1.48s
     Running unittests src/main.rs (target/debug/deps/rust_link-d008c1110239f0a1)

running 16 tests
test tests::get_entity_content_length_bad - should panic ... ok
test tests::get_socket_addr_from_env_host_ipv4 ... ok
test tests::get_entity_content_length_zero ... ok
test tests::get_entity_content_length_empty ... ok
test tests::get_socket_addr_from_env_host_ipv4_bad_host - should panic ... ok
test tests::get_entity_content_length_missing ... ok
test tests::get_socket_addr_from_env_host_ipv4_bad_port - should panic ... ok
test tests::get_socket_addr_from_env_host_ipv4_alt_port ... ok
test tests::number_to_text_bytes_0 ... ok
test tests::number_to_text_bytes_1 ... ok
test tests::number_to_text_bytes_259 ... ok
test tests::get_socket_addr_from_env_host_ipv6 - should panic ... ok
test tests::get_socket_addr_from_env_host_name ... ok
test tests::get_socket_addr_from_env_missing_vars - should panic ... ok
test tests::get_socket_addr_from_env_unix ... ok
test tests::send_arguments_output ... ok

test result: ok. 16 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.58s
```

### Performance and resources

I developed `rust_link` on Linux (x86_64) and also built and tested it on macOS (ARM 64-bit) and Linux on Raspberry Pi (ARM 32-bit), where it also worked fine, as expected.

The speed of this new `rust_link` compares well to the classic `vlink`. Startup time is the main concern as there is no significant processing done once the program is running. Measurements are essentially the same, within the margin of error.

Some of the link program implementations use a limited buffer size (such as 16 KiB for `vlink` and `tlink`) to spool data from Interchange back to the web server. It is common practice to send large response bodies as files directly from a web server rather than from dynamic Interchange responses to limit the time an Interchange worker process is occupied. Because of that, and since most servers have far more memory available now than in years past, I let `rust_link` read the entire response body into memory rather than using a fixed buffer size.

Because Rust crates are compiled into the `rust_link` executable, not linked as shared libraries as is typical with C programs, the executable program size is bigger for `rust_link` than `vlink`: 9× more on disk under ARM64 macOS! But that increase is from a small base of ~34 KiB to ~312 KiB. (This is for executables stripped of debugging symbols.) On modern operating systems with copy-on-write behavior, most of that memory is shared so it is a one-time cost, not multiplying per running CGI program instance.

### Publication

Since it works as well as the other implementations, I figured it was worth finally adding some documentation and releasing it as open source software alongside the other Interchange link programs, available for anyone who wants to avoid the risks of C to deploy with or without customization.

The [code is on GitHub ready to use](https://github.com/interchange/interchange/tree/master/dist/src/rust_link) and the `rust_link/README.md` explains how to build and install it.

### Reference

* [Interchange ecommerce project](https://www.interchangecommerce.org/)
* [Common Gateway Interface (CGI)](https://en.wikipedia.org/wiki/Common_Gateway_Interface)
  * [RFC 3875 section 4.4](https://www.rfc-editor.org/rfc/rfc3875.html#section-4.4) which defines the ancient and now almost completely defunct convention for CGI script command line arguments to contain an "indexed" HTTP query
* [FastCGI](https://en.wikipedia.org/wiki/FastCGI)
* [Apache JServ Protocol (AJP)](https://en.wikipedia.org/wiki/Apache_JServ_Protocol)
* [HTTP reverse proxy](https://en.wikipedia.org/wiki/Reverse_proxy)
* [Rust programming language](https://www.rust-lang.org/)
  * [Would Rust secure cURL?](https://blog.timhutt.co.uk/curl-vulnerabilities-rust/) by Tim Hutt
  * [Rust crate `multisock`](https://crates.io/crates/multisock)
  * [From Perl to Rust](https://oylenshpeegul.gitlab.io/from-perl-to-rust/)
