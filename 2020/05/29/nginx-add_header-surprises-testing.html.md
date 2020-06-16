---
title: "Testing to defend against nginx add_header surprises"
author: Jon Jensen
tags: sysadmin, nginx, security, javascript, nodejs, testing
gh_issue_number: 1634
---

<img src="/blog/2020/05/29/nginx-add_header-surprises-testing/20200408-104315-mod.jpg" alt="Cute calico cat perched securely upon a trepidatious shoe" />

<!-- Photo by Jon Jensen -->

These days when hosting websites it is common to configure the web server to send several HTTP response headers with every single request for security purposes.

For example, using the nginx web server we may add these directives to our `http` configuration scope to apply to everything served, or to specific `server` configuration scopes to apply only to particular websites we serve:

```plain
add_header Strict-Transport-Security max-age=2592000 always;
add_header X-Content-Type-Options    nosniff         always;
```

(See [HTTP Strict Transport Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security) and [X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options) at MDN for details about these two particular headers.)

### The surprise (problem)

Once upon a time I ran into a case where nginx usually added the expected HTTP response headers, but later appeared to be inconsistent and sometimes did not. This is distressing!

Troubleshooting leads to the (re-)discovery that `add_header` directives are not always additive throughout the configuration as one would expect, and as every other server I can think of typically does.

If you define your `add_header` directives in the `http` block and then use an `add_header` directive in a `server` block, those from the `http` block will disappear.

If you define some `add_header` directives in the `server` block and then add another `add_header` directive in a `location` block, those from the `http` and/or `server` blocks will disappear.

This is even the case in an `if` block.

In the [nginx `add_header` documentation](https://nginx.org/en/docs/http/ngx_http_headers_module.html#add_header) we find the reason for the behavior explained:

> There could be several add_header directives. These directives are inherited from the previous level if and only if there are no add_header directives defined on the current level.

This nginx directive has always behaved this way. Various people have warned about it in blog posts and online discussions for many years. But the situation remains the same, a trap for the unwary.

I have tried to imagine the rationale behind this behavior. Response headers often are set in groups, so the programmer who created this feature may have decided that any new scope’s `add_header` directives should start with a clean slate, unaffected by those set elsewhere. Hmm. The need for exclusive grouping of response headers is rare in my experience, and adding headers to the existing stack of tentative response headers is far more commonly what I want.

So while this behavior may make sense somewhere, it has not ever done so for me or anyone I have talked to about it. For us it is simply misbehavior, silent and easy to overlook when making later seemingly unrelated configuration adjustments.

### Dangers

It often has security implications when headers you thought were being added to every response are not. Consider more fine-tuned and consequential security-related headers such as [`Content-Security-Policy`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy), [`Vary`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Vary) for cache object separation, [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) headers `Access-Control-*`, etc.

Headers such as these are especially important when they need to be added based on logic spread across various configuration blocks, and that is exactly when nginx `add_headers` doesn’t work as expected.

Another pitfall is omitting the `always` option to `add_header`. Without that, the header will only be added to success responses (2XX and 3XX, but see the docs for specifics). We usually want security-related headers to be added even to 4XX and 5XX error responses.

### Workaround using include

My first instinct was to work around the problems caused by this behavior by putting the standard add_header list in a file that I include everywhere. In some cases that works.

But despite the [nginx include documentation](https://nginx.org/en/docs/ngx_core_module.html#include) saying that directive is allowed in “Context: any”, `include` is *not* allowed in an `if` block and will result in the fatal startup error:

> "include" directive is not allowed here

So the only recourse in those cases is to repeat all needed `add_header` directives in every `if` block that uses `add_header`. Gross.

Repeating configuration manually means almost surely having the `add_header` directives in different configuration areas drift over time. So if we have to repeat ourselves, at least let’s do it with automation, such as by using configuration templating and preprocessing.

That is what I have most recently done. And we can still use native nginx `include` directives everywhere those are allowed.

### nginx Headers More module

Many people have run into exactly this problem, and some of them developed a separate nginx module [ngx_headers_more](https://github.com/openresty/headers-more-nginx-module#readme) to solve most of these problems.

By using its `more_set_headers` directive, you get the expected additive behavior with previously-declared headers, regardless of the block scope:

> Directives inherited from an upper level scope (say, http block or server blocks) are executed before the directives in the location block.
>
> Note that although more_set_headers is allowed in location if blocks, it is not allowed in the server if blocks …

Fortunately I have not needed to use this in an `if` block in the `server` scope, so that one remaining limitation doesn’t pose a problem for me.

It also has options to set a header only for responses of a certain HTTP content type or status code.

The `more_clear_headers` directive allows the `*` wildcard for clearing all headers with the same prefix at once, such as `Access-Control-*`.

#### Installing ngx_headers_more

Because “Headers More” is a separate module, not part of standard nginx, it is not usually available without some extra work.

You can build it from source and install it manually, but of course that isn’t good to do on a production machine since it won’t get updated on its own.

You can use the [OpenResty](https://openresty.org/en/) server built around nginx, which “Headers More” is part of. But you may not want all of that if you’re not writing a Lua web application.

Many Linux distributions and 3rd-party package repositories have prebuilt packages for “Headers More” which you can use:

* Alpine
  + `nginx-mod-http-headers-more`
* Debian &amp; Ubuntu
  + `nginx-extras`
  + `libnginx-mod-http-headers-more-filter`
* RHEL/CentOS
  + GetPageSpeed &amp; Webtatic repos `nginx-module-headers-more`
  + Aeris repo `nginx-more`

Search the excellent [pkgs.org](https://pkgs.org/) to find what you need if it isn’t already available through your package manager.

### Apache

Apache httpd is still alive and well — actually better than ever. So depending on your situation, you may want to use that instead.

Apache’s [Header directive](https://httpd.apache.org/docs/2.4/mod/mod_headers.html#header) has intuitive (to me) default behavior for setting response headers across the whole configuration, and many ways to deal with a possibly already-existing header:

* add another header, or set exclusively (replace), or set only if this header doesn’t already exist
* append to or merge into an existing header (for headers that accept multiple values)
* edit an existing header with a regular expression search-and-replace
* unset a header if one was previously set

I don’t know a way to have Apache clear a group of headers with a wildcard, or all headers at once, so they need to be individually cleared by name if that’s what you want.

### Доверяй, но проверяй (Trust, but verify)

nginx was written by Igor Sysoev. Despite my disagreement with this one feature’s behavior, overall I find that nginx is excellent. Because of its open source release, excellent performance, and wide use, it has provided much-needed competition to Apache and Microsoft IIS. Thank you, Igor and all other contributors!

In the relevant spirit, since Igor is Russian, I close with the Russian proverb Доверяй, но проверяй: Trust, but verify.

Let us code (and configure) defensively, yet also test to avoid being surprised by missing headers.

We can manually test various HTTP responses are as we expect using `curl -v` or other HTTP clients to exercise various requests.

Even better, we can add to our automated test suite to confirm these HTTP response headers appear everywhere we expect, for static files and API endpoints backed by different application servers, and for various success and error responses.

Here is a test adapted from one I put together for one of our clients. It uses JavaScript in [Node.js](https://nodejs.org/), the [Jest](https://jestjs.io/) test framework, and the [Axios](https://github.com/axios/axios) HTTP client. It ensures the security headers example I showed at the beginning of this article keeps working, even as we make nginx configuration changes over time:

```js
const axios = require('axios');

const http = axios.create({
  baseURL: 'https://your.dom.ain',
});

describe('Check security headers', () => {
  const verifs = [
    { header: 'strict-transport-security', expect: (x) => x.toMatch(/max-age=\d{3,}/) },
    { header: 'x-content-type-options',    expect: (x) => x.toEqual('nosniff')        },
  ];

  const locs = [
    { path: '/robots.txt',                status: 200 },  // static
    { path: '/feed/endpoint/of/interest', status: 200 },  // API backend in PHP
    { path: '/api/other/auth/endpoint',   status: 403 },  // API backend in Perl
    { path: '/never/gonna/give/you/up!',  status: 404 },
    { path: '/api/dies/for/testing',      status: 500 },
  ];

  // throw no exceptions for non-success HTTP response status
  const conf = { validateStatus: () => true };

  for (const l of locs) {
    test(`${l.status} ${l.path}`, async () => {
      const res = await http.get(l.path, conf);
      expect(res.status).toBe(l.status);
      for (const v of verifs) {
        v.expect(expect(res.headers[v.header]));
      }
    });
  }
});

```

Here I run just this one test rather than the whole suite:

```plain
% jest -w 6 ./__tests__/webserver/security-headers.test.js
Determining test suites to run...
testing on https://https://your.dom.ain

 PASS  webserver/security-headers.test.js
  Check security headers
    ✓ 200 /robots.txt (55ms)
    ✓ 200 /feed/endpoint/of/interest (408ms)
    ✓ 403 /api/other/auth/endpoint (18ms)
    ✓ 404 /never/gonna/give/you/up! (6ms)
    ✓ 500 /api/dies/for/testing (12ms)

Test Suites: 1 passed, 1 total
Tests:       5 passed, 5 total
Snapshots:   0 total
Time:        2.721s, estimated 3s
Ran all test suites matching /.\/__tests__\/webserver\/security-headers.test.js/i.
```

This can also be extended to ensure that certain headers do not exist, or do not contain details that you do not want exposed:

* the `Server` header should not reveal the nginx (see [server_tokens](https://nginx.org/en/docs/http/ngx_http_core_module.html#server_tokens)) or Apache (see [ServerTokens](https://httpd.apache.org/docs/trunk/mod/core.html#servertokens)) version numbers
* the `X-Powered-By` header should be absent, not exposing the fact that you are using PHP, and the version number — see the [expose_php](https://www.php.net/manual/en/ini.core.php#ini.expose-php) directive for `php.ini`
* or with the Java Wildfly server, both of those headers are sent by default! — see instructions on how to omit them [by editing XML](https://zenidas.wordpress.com/recipes/hideexpose-http-headers-in-wildfly-10-1/) or [using jboss-cli](https://mariusz.wyszomierski.pl/en/turn-off-x-powered-by-i-server-headers-in-wildfly-10/)

Add to the `verifs` array in the code above:

```js
    { header: 'server',                    expect: (x) => x.not.toMatch(/\d/)         },
    { header: 'x-powered-by',              expect: (x) => x.toBeUndefined()           },
```

Now if (when) I forget about the nginx `add_headers` behavior, make changes, and inadvertently break things? Instead of it being unnoticed, my test suite will alert me so I can fix it before it goes into production!
