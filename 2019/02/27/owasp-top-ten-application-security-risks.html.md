---
author: "Marco Pessotto"
title: "OWASP Top Ten Application Security Risks"
tags: security
gh_issue_number: 1502
---

![wasps](/blog/2019/02/27/owasp-top-ten-application-security-risks/wasps.jpg)

I don’t consider myself a security expert. Still, to my surprise, I
was asked to give a talk about security to all the End Point
developers. Obviously I realized too late what I was getting myself
into! Such an audience is not only pretty large, it is also
challenging, many are more competent than me, and the risk to bore them
is very high. Yet, the slides were prepared, the talk was given and
the feedback was good.

It goes without saying that a broad, generic training about security,
which still can give something to the listener, can’t be really
improvised.

The platform for the talk was the
[OWASP Top Ten 2017 Project](https://www.owasp.org/index.php/Category:OWASP_Top_Ten_2017_Project),
which discusses the most critical security risks to
web applications.

[OWASP](https://www.owasp.org/) stands for Open Web Application
Security Project and describes itself as “an open community dedicated
to enabling organizations to develop, purchase, and maintain
applications and APIs that can be trusted.” Its website provides
plenty of resources to the developers.

The Top Ten consists of 10 broad classes of vulnerabilities. The
data behind that comes from specialized firms and surveys, gathering
information from 100,000 real-world applications and APIs. Some of
these classes are very broad and have a taxonomic value. Saying, for
example, “Broken access control” or “Security misconfiguration”,
doesn’t say much what you are doing wrong. It still reminds us that a
lot of things can actually go wrong and that when working on a service
you should ask yourself how are you doing with regard to security.

The current (2017) Top Ten classes are:

1. Injection
1. Broken Authentication
1. Sensitive Data Exposure
1. XML External Entities (XXE)
1. Broken Access Control
1. Security Misconfiguration
1. Cross-Site Scripting (XSS)
1. Insecure Deserialization
1. Using Components with Known Vulnerabilities
1. Insufficient Logging &amp; Monitoring

I’m not going over the Top Ten in detail like I did at the training, but I’m
going to leave here a couple of brief notes.

**Injections:** in my naivety I was convinced that this class of
vulnerability, which is very specific and whose fix is well-​known, was
something belonging to the past, to legacy and neglected applications.
Still, it’s not so. It’s 2019 and injections are still winning.

If by chance you are still interpolating variables inside the SQL and not
using placeholders, it’s time to take a look at [Bobby
Tables](http://bobby-tables.com/) (or equivalent) and start doing it
right, as every major language has a library supporting them. Maybe
you avoid this vulnerability in your own code, but have inherited code
from others who did not defend against it. Look and see!

**Broken Authentication:** On the other hand, finding the authentication problems in second
place was not a surprise at all, given the frequency of leaked
databases. The recommended practice appears to be checking the
password against a list of known passwords and ensuring it has a
decent length. (Please note: no requiring regular password rotation, nor
uppercase/​lowercase/​digit enforcing.)

**XSS:** For web developers an interesting class is the ubiquitous Cross-Site
Scripting (XSS) vulnerability, which is found in two-​thirds of all
applications. Statistically speaking, it’s probable that the
application you are currently working on is affected.

XSS comes in many flavors, usually generated server-​side, when a
variable coming from user input is interpolated without proper
escaping into the HTML, opening the door to JavaScript execution, but
DOM XSS is also common. How many times did you see something like
this, for example, with jQuery:

```javascript
$('#app').html(string_from_user)
```

The `html()` method stuffs whatever string is provided by the user
into the HTML page. This should be rewritten as:

```javascript
$('#app').text(string_from_user)
```

If formatting is required, the `append()` method is your friend.

**CSRF:** Interestingly enough, Cross Site Request Forgery (when an
application doesn’t check if a POST request comes from the site itself
and not from a random site on the internet which is fooling the
authenticated browser to perform an operation on your site) didn’t
make into the Top Ten. This is probably due to the fact that
mainstream frameworks like Ruby on Rails and Django come with CSRF
protections almost out of the box.

The goal of the OWASP document is to increase the awareness about
security problem. We are trying to do our part to prevent security problems at End Point.
