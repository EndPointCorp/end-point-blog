---
author: "Jon Jensen"
title: "Useful terminal tools"
tags: tips, tools
gh_issue_number: 1584
---

<img src="/blog/2020/01/03/useful-terminal-tools/41825658781_b9f7f79fc1_o-crop.jpg" alt="Móricz Zsigmond körtér Underground Station (people, escalators)" /><br><a href="https://www.flickr.com/photos/tcee35mm/41825658781/">Photo by Tee Cee</a> · <a href="https://creativecommons.org/licenses/by/2.0/">CC BY 2.0</a>, cropped

Like most of my co-workers, I spend a lot of time in a terminal emulator (console) in a shell at the Linux command line. I often come across tools that make work there nicer, but sometimes I forget about them before I integrate them into my workflow. So here are notes about a few of them for myself and anyone else who may find them useful.

### HTTPie

[HTTPie](https://httpie.org/) is:

> a command line HTTP client with an intuitive UI, JSON support, syntax highlighting, wget-like downloads, plugins, and more. 

Given how commonly-used curl, wget, and GET/POST (lwp-request) are, it is nice to see some innovation in this space to enhance usability.

Here is a simple example that demonstrates several HTTP redirects with full request and response headers, colorized:

```bash
http -v --pretty=all --follow endpoint.com | less -R
```

The color highlighting of the body, not just response headers, is the main difference here from curl, wget, etc.

Also nice for ad-hoc interactive use is that the verbose header output is sent to `stdout` instead of `stderr`, so it shows up in `less` without needing to have the shell merge it with `2>&1` before piping to `less`.

#### An aside on HTTP redirects

In the above example, the client makes 3 requests, because the first 2 are redirects:

* http://endpoint.com/
* https://endpoint.com/
* https://www.endpoint.com/

Normally we would want to reduce the number of HTTP redirects, so why not redirect straight from `http://endpoint.com/` to `https://www.endpoint.com/`?

Before the introduction of [HTTP Strict Transport Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security) (HSTS) to the web, that is what we did.

But with HSTS it is better to pass through HTTPS for each hostname, so that the `Strict-Transport-Security` HTTP response header can be sent and the browser can cache the fact that both the bare yourdomain.tld and www.yourdomain.tld should only be accessed via HTTPS.

See the thorough description at the [Sentinel Stand blog post](https://www.sentinelstand.com/article/http-strict-transport-security-hsts-canonical-www-redirects) for more details, including a discussion of `includeSubDomains` traps.

#### JSON pretty-printing

HTTPie also can pretty-print JSON responses. For example, compare this [sample JSON from MDN](https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json) raw from `curl`:

<code class="hljs">
% curl -i https://www.endpoint.com/blog/2020/01/03/useful-terminal-tools/super-hero-squad.json<br>
HTTP/1.1 200 OK<br>
<span style="font-weight:bold;">Date</span>: Tue, 14 Jan 2020 01:48:58 GMT<br>
<span style="font-weight:bold;">Server</span>: Apache<br>
<span style="font-weight:bold;">Last-Modified</span>: Tue, 23 Apr 2019 00:43:10 GMT<br>
<span style="font-weight:bold;">ETag</span>: "22a-58727de80a380"<br>
<span style="font-weight:bold;">Accept-Ranges</span>: bytes<br>
<span style="font-weight:bold;">Content-Length</span>: 554<br>
<span style="font-weight:bold;">Content-Type</span>: application/json<br>
<br>
{"squadName":"Super hero squad","homeTown":"Metro City","formed":2016,"secretBase":"Super tower","active":true,"members":[{"name":"Molecule Man","age":29,"secretIdentity":"Dan Jukes","powers":["Radiation resistance","Turning tiny","Radiation blast"]},{"name":"Madame Uppercut","age":39,"secretIdentity":"Jane Wilson","powers":["Million tonne punch","Damage resistance","Superhuman reflexes"]},{"name":"Eternal Flame","age":1000000,"secretIdentity":"Unknown","powers":["Immortality","Heat Immunity","Inferno","Teleportation","Interdimensional travel"]}]}
</code>

to HTTPie’s pretty-printed output:

<code class="hljs">
% http https://www.endpoint.com/blog/2020/01/03/useful-terminal-tools/super-hero-squad.json<br>
<span style="color: rgb(0,135,255);">HTTP</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">/</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">1.1</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">200</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(175,135,0);">OK</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">Accept-Ranges</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">bytes</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">Connection</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">Keep-Alive</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">Content-Length</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">554</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">Content-Type</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">application/json</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">Date</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">Tue, 14 Jan 2020 02:27:29 GMT</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">ETag</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;22a-58727de80a380&quot;</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">Keep-Alive</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">timeout=5, max=100</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">Last-Modified</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">Tue, 23 Apr 2019 00:43:10 GMT</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">Server</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">Apache</span><span style="color:white;"><br>
<br>
</span><span style="color: rgb(138,138,138);">{</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;active&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(215,95,0);">true</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;formed&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">2016</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;homeTown&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Metro City&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;members&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(138,138,138);">[</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">{</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;age&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">29</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;name&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Molecule Man&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;powers&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(138,138,138);">[</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Radiation resistance&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Turning tiny&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Radiation blast&quot;</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">]</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;secretIdentity&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Dan Jukes&quot;</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">}</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">{</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;age&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">39</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;name&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Madame Uppercut&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;powers&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(138,138,138);">[</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Million tonne punch&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Damage resistance&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Superhuman reflexes&quot;</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">]</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;secretIdentity&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Jane Wilson&quot;</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">}</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">{</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;age&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">1000000</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;name&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Eternal Flame&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;powers&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(138,138,138);">[</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Immortality&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Heat Immunity&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Inferno&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Teleportation&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Interdimensional travel&quot;</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">]</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;secretIdentity&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Unknown&quot;</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">}</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">]</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;secretBase&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Super tower&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">,</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:white;"></span><span style="color: rgb(0,135,255);">&quot;squadName&quot;</span><span style="color:white;"></span><span style="color: rgb(138,138,138);">:</span><span style="color:white;"></span><span style="color: rgb(138,138,138);"> </span><span style="color:white;"></span><span style="color: rgb(0,175,175);">&quot;Super hero squad&quot;</span><span style="color:white;"><br>
</span><span style="color: rgb(138,138,138);">}</span>
</code>

Of course you can use something like the popular `jq` to do your pretty-printing, but getting it in one tool with no options is nice.

Perhaps the hardest thing for me to remember with HTTPie is the program name, simply `http`. I forget and type `httpie` and get nothing. But no, I won’t give in and create an alias or symlink to it with that name. It is shorter and the default and I need to learn it!

### htty

Related, but on the opposite end of the user interface spectrum, is [htty, the HTTP TTY](https://htty.github.io/htty/). It has its own shell and state that you work with. The examples give a good feel for it.

Keeping the context and history in a console interface is really nice for interactive work compared to the one-shot nature of curl, wget, etc.

### Exporting ANSI terminal colors

Many command-line tools can now output colors, bold and underlined type, etc. for interactive user readability. But how do we convert those escape codes to HTML so we can show them on the Web, as I did above?

[aha (Ansi HTML Adapter)](https://github.com/theZiz/aha) (C), [ansi2html](https://github.com/ralphbean/ansi2html) (Python), and [ansi2html.sh](https://github.com/pixelb/scripts/blob/master/scripts/ansi2html.sh) (Bourne shell) are 3 different ways to accomplish that.

If you have any trouble getting a program to output ANSI color codes to a file (since many of them refuse to do that when the output is not an interactive terminal), you can use `script`:

```bash
script -q -c "/the/command/here with options" /path/to/output
```

to capture it verbatim. Since `script` is part of the standard `util-linux` package, you probably already have it on any Linux system.

### Git browsing

These two programs are really nice Git repository browsers for the terminal:

* [tig (Text-mode Interface for Git)](https://jonas.github.io/tig/)
* [grv (Git Repository Viewer)](https://github.com/rgburke/grv)

Just go to their project pages and look at the screenshots and try them out on a repository of your own. Experiencing that is better than what I could generically show you. They are great for browsing branches in complex merge histories, files, etc.

### Introductory manual pages

You are probably aware that the shorthand “TL;DR” means “too long; didn’t read”. There is now a project called [TLDR pages](https://tldr.sh/) whic is “a community effort to simplify the beloved man pages with practical examples”.

I have been trying to get used to the newer `ss` (which stands for “socket statistics”) which can replace `netstat` and `lsof`, so I took a look at what the TLDR pages had to say about it:

```plain
% tldr ss

  ss

  Utility to investigate sockets.

  - Show all TCP/UDP/RAW/UNIX sockets:
    ss -a -t|-u|-w|-x

  - Filter TCP sockets by states, only/exclude:
    ss state/exclude bucket/big/connected/synchronized/...

  - Show all TCP sockets connected to the local HTTPS port (443):
    ss -t src :443

  - Show all TCP sockets along with processes connected to a remote ssh port:
    ss -pt dst :ssh

  - Show all UDP sockets connected on specific source and destination ports:
    ss -u 'sport == :source_port and dport == :destination_port'

  - Show all TCP IPv4 sockets locally connected on the subnet 192.168.0.0/16:
    ss -4t src 192.168/16
```

That gets me started a lot faster than the ~350 lines that `man ss` gives me. And the full details are always still there for me when I need them.

There are TLDR pages on many commands!

### Ping graph

[Check out gping](https://github.com/orf/gping), which makes a textual graph of ping responses. Simple and handy.

### Finding Unicode characters

There is a nice command-line utility for dealing with Unicode in various ways. Ricardo Signes explains why he wrote it and demonstrates how to use it in [“I rewrote uni”](https://rjbs.manxome.org/rubric/entry/2061).

Install with `cpanm App::Uni` or however else you prefer to install Perl modules from CPAN. It has a few useful options:

```plain
% uni
usage:
  uni SEARCH-TERMS...    - find codepoints with matching names or values
  uni [-s] ONE-CHARACTER - print the codepoint and name of one character
  uni -n SEARCH-TERMS... - find codepoints with matching names
  uni -c STRINGS...      - print out the codepoints in a string
  uni -u CODEPOINTS...   - look up and print hex codepoints

  Other switches:
      -8                 - also show the UTF-8 bytes to encode
```

If you see a Unicode character out in the wild and can copy and paste it, `uni` can identify it for you:

```plain
% uni 🦆
🦆 - U+1F986 - DUCK
```

I most commonly use its implicit search function:

```plain
% uni horse
⻢- U+02EE2 - CJK RADICAL C-SIMPLIFIED HORSE
⾺- U+02FBA - KANGXI RADICAL HORSE
🎠 - U+1F3A0 - CAROUSEL HORSE
🏇 - U+1F3C7 - HORSE RACING
🐎 - U+1F40E - HORSE
🐴 - U+1F434 - HORSE FACE
🝖 - U+1F756 - ALCHEMICAL SYMBOL FOR HORSE DUNG
🩣 - U+1FA63 - XIANGQI RED HORSE
🩪 - U+1FA6A - XIANGQI BLACK HORSE
```

That Unicode character 🝖 = “alchemical symbol for horse dung” is a delight. I know I will be using that one often! 😜

`uni` is also useful for showing the characters for given code points:

```plain
% uni -u 25c8 25c9 25ca
◈ - U+025C8 - WHITE DIAMOND CONTAINING BLACK SMALL DIAMOND
◉ - U+025C9 - FISHEYE
◊ - U+025CA - LOZENGE
```

There is also an unrelated [Go version of `uni`](https://github.com/arp242/uni) that is fairly similar: 

```plain
% uni help
Usage: uni [-hrq] [help | identify | search | print | emoji]

Flags:
    -q      Quiet output; don't print header, "no matches", etc.
    -r      "Raw" output instead of displaying graphical variants for control
            characters and ◌ (U+25CC) before combining characters.

Commands:
    identify [string string ...]
        Idenfity all the characters in the given strings.

    search [word word ...]
        Search description for any of the words.

    print [ident ident ...]
        Print characters by codepoint, category, or block:

            Codepoints             U+2042, U+2042..U+2050
            Categories and Blocks  OtherPunctuation, Po, GeneralPunctuation
            all                    Everything

        Names are matched case insensitive; spaces and commas are optional and
        can be replaced with an underscore. "Po", "po", "punction, OTHER",
        "Punctuation_other", and PunctuationOther are all identical.

    emoji [-tone tone,..] [-gender gender,..] [-groups word] [word word ...]
        Search emojis. The special keyword "all" prints all emojis.

        -group   comma-separated list of group and/or subgroup names.
        -tone    comma-separated list of light, mediumlight, medium,
                 mediumdark, dark. Default is to include none.
        -gender  comma-separated list of person, man, or woman.
                 Default is to include all.

        Note: output may contain unprintable character (U+200D and U+FE0F) which
        may not survive a select and copy operation from text-based applications
        such as terminals. It's recommended to copy to the clipboard directly
        with e.g. xclip.
```

Its search function is roughly the same as its Perl counterpart with the `-8` option and additionally showing the decimal code point (which I’ve never seen used) and the HTML hex entity:

```plain
% uni search horse
     cpoint  dec    utf-8       html       name
'⻢' U+2EE2  12002  e2 bb a2    &#x2ee2;   CJK RADICAL C-SIMPLIFIED HORSE (Other_Symbol)
'⾺' U+2FBA  12218  e2 be ba    &#x2fba;   KANGXI RADICAL HORSE (Other_Symbol)
'🎠' U+1F3A0 127904 f0 9f 8e a0 &#x1f3a0;  CAROUSEL HORSE (Other_Symbol)
'🏇' U+1F3C7 127943 f0 9f 8f 87 &#x1f3c7;  HORSE RACING (Other_Symbol)
'🐎' U+1F40E 128014 f0 9f 90 8e &#x1f40e;  HORSE (Other_Symbol)
'🐴' U+1F434 128052 f0 9f 90 b4 &#x1f434;  HORSE FACE (Other_Symbol)
'🝖'  U+1F756 128854 f0 9f 9d 96 &#x1f756;  ALCHEMICAL SYMBOL FOR HORSE DUNG (Other_Symbol)
'🩣'  U+1FA63 129635 f0 9f a9 a3 &#x1fa63;  XIANGQI RED HORSE (Other_Symbol)
'🩪'  U+1FA6A 129642 f0 9f a9 aa &#x1fa6a;  XIANGQI BLACK HORSE (Other_Symbol)
```

### Dashboard

The [WTF terminal dashboard](https://wtfutil.com/) looks pretty neat, but at the moment, it feels like too much. I may come back to it later.

### Chromecast

I never knew I want a way to cast video and audio to my Chromecast, but with [catt (Cast All The Things)](https://github.com/skorokithakis/catt/#cast-all-the-things) that is what we get!

It works well for me. Sadly, Google discontinued manufacturing the Chromecast Audio in 2019. Ours still works and I hope it continues to for a long time to come.

### Mega-meta list of tools

Finally, if the above has not given you enough new toys to play with, see [The Book of Secret Knowledge](https://github.com/trimstray/the-book-of-secret-knowledge), “A collection of inspiring lists, manuals, cheatsheets, blogs, hacks, one-liners, CLI/web tools, and more”.

Some of its list is links to other lists. I’ll see you in a few years when you get through all that!
