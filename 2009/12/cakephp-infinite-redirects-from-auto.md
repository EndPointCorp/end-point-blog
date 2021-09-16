---
author: Steph Skardal
title: CakePHP Infinite Redirects from Auto Login and Force Secure
github_issue_number: 233
tags:
- php
date: 2009-12-10
---

Lately, [Ron](/team/ron-phipps), Ethan, and I have been blogging about several of our CakePHP learning experiences, such as [incrementally migrating to CakePHP](/blog/2009/12/iterative-migration-of-legacy), [using the CakePHP Security component](/blog/2009/12/using-security-component-and), and [creating CakePHP fixtures for HABTM relationships](/blog/2009/11/test-fixtures-for-cakephp-has-and). This week, I came across another blog-worthy topic while troubleshooting for [JackThreads](https://www.jackthreads.com) that involved auto login, requests that were forced to be secure, and infinite redirects.

<a href="https://2.bp.blogspot.com/_wWmWqyCEKEs/SyErTpCsuAI/AAAAAAAACyU/mLM1yidKsK0/s1600-h/infinite_redirect.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5413655843510728706" src="/blog/2009/12/cakephp-infinite-redirects-from-auto/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 201px;"/></a>

Ack! Users were experiencing infinite redirects!

### The Problem

Some users were seeing infinite redirects. The following use cases identified the problem:

- Auto login true, click on link to secure or non-secure homepage => **Whammy: Infinite redirect!**
- Auto login false, click on link to secure or non-secure homepage => **No Whammy!**
- Auto login true, type in secure or non-secure homepage in new tab => **No Whammy!**
- Auto login false, type in secure or non-secure homepage in new tab => **No Whammy!**

So, the problem boiled down to an infinite redirect when auto login customers clicked to the site through a referer, such as a promotional email or a link to the site.

### Identifying the Cause of the Problem

After I applied initial surface-level debugging without success, I decided to add excessive debugging to the code. I added debug statements throughout:

- the CakePHP Auth object
- the CakePHP Session object
- the app’s app_controller beforeFilter that completed the auto login
- the app’s component that forced a secure redirect on several pages (login, checkout, home)

I output the session id and request location with the following debug statement:

```php
$this->log($this->Session->id().':'.$this->here.':'.'/*relevant message about whatsup*/', LOG_DEBUG);
```

With the debug statement shown above, I was able to compare the normal and infinite redirect output and identify a problem immediately:

#### normal output

```nohighlight
2009-12-09 11:44:55 Debug: d3c2297ddea9b76605cb7a459f45965b:/:     User does not exist!
2009-12-09 11:44:55 Debug: d3c2297ddea9b76605cb7a459f45965b:/:     Success in auto login!
2009-12-09 11:44:55 Debug: d3c2297ddea9b76605cb7a459f45965b:/:     redirecting to /sale
2009-12-09 11:44:55 Debug: d3c2297ddea9b76605cb7a459f45965b:/sale: User exists!
2009-12-09 11:44:55 Debug: d3c2297ddea9b76605cb7a459f45965b:/sale: calling action!
```

#### infinite redirect output

```nohighlight
2009-12-09 11:43:30 Debug: 65cb23e4ca358b7270513cca4a52e9b7:/:      User does not exist!
2009-12-09 11:43:30 Debug: 65cb23e4ca358b7270513cca4a52e9b7:/:      Success in auto login!
2009-12-09 11:43:30 Debug: 65cb23e4ca358b7270513cca4a52e9b7:/:      redirecting to /sale
2009-12-09 11:43:30 Debug: 397f099790347716e0bc58c73f23358d:/sale:  User does not exist!
2009-12-09 11:43:30 Debug: 397f099790347716e0bc58c73f23358d:/sale:  redirecting to /login
2009-12-09 11:43:30 Debug: 0dfee15a4295b26aad115ae37d470d30:/login: User does not exist!
2009-12-09 11:43:30 Debug: 0dfee15a4295b26aad115ae37d470d30:/login: Success in auto login!
2009-12-09 11:43:30 Debug: 0dfee15a4295b26aad115ae37d470d30 /login: redirecting to /sale
2009-12-09 11:43:31 Debug: 3f23b7f7bead5d23fd006b6d91b1d195:/sale:  User does not exist!
2009-12-09 11:43:31 Debug: 3f23b7f7bead5d23fd006b6d91b1d195:/sale:  redirecting to /login
...
<a href="https://1.bp.blogspot.com/_wWmWqyCEKEs/SyEsCNS5J6I/AAAAAAAACyc/B3qvQAD_XhA/s1600-h/whammy.jpg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5413656643516311458" src="/blog/2009/12/cakephp-infinite-redirects-from-auto/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 263px; height: 258px;"/></a>
```

What I immediately noticed was that sessions were dropped at every redirect on the infinite redirect path. So I researched a bit and found the following resources:

- [https://groups.google.com/forum/#!topic/cake-php/TXgHRlvlawM](https://groups.google.com/forum/#!topic/cake-php/TXgHRlvlawM): A CakePHP google group message about lost sessions.
- [http://book.cakephp.org/view/42/The-Configuration-Class](https://web.archive.org/web/20091210200338/http://book.cakephp.org/view/42/The-Configuration-Class): CakePHP documentation on the Security.level setting.
- [http://www.php.net/manual/en/session.configuration.php#ini.session.referer-check](https://web.archive.org/web/20091226154410/http://www.php.net/manual/en/session.configuration.php): PHP documentation on referer_check.

As it turns out, the Security.level configuration affected the referer check for redirects. The CakePHP Session object set the referer_check to HTTP_HOST if Security.level was equal to ‘high’ or ‘medium’. A couple of the resources mentioned above recommend to adjust the Security.level to ‘low’, which sounded like a potential solution. But I wasn’t certain that this was the cause of the redirect, so I tested several changes to verify the problem.

First, I tested the Security.levels to ‘high’, ‘medium’, and ‘low’. With the Security.level set to ‘low’, the infinite redirect would not happen and the debug log would show a consistent session id. Next, I commented out the code in the CakePHP Session object that set the referer_check and set the Security.level to ‘high’. This also seemed to fix the infinite redirect, although, it wasn’t ideal to make changes to the the core CakePHP code. Finally, I changed this->host to HTTPS_HOST instead of HTTP_HOST in the CakePHP Session object, so that the referer would be checked against the secure host rather than the non-secure host. This also fixed the infinite redirect, but again, it wasn’t ideal to change the core CakePHP code.

I concluded that the secure redirect to the homepage or login page coupled with the auto login caused this infinite redirect. As pages were redirected between /login and /sale, the session (that stored the auto logged in user) was dropped since the referer check against HTTP_HOST failed.

### The Solution

In an ideal world, I would like to see HTTP_HOST and HTTPS_HOST included in the CakePHP referer check. But because we didn’t want to edit the CakePHP core, I investigated the affect of changing the Security.level on the app:

<table width="100%">
<tbody><tr>
<td valign="top">
<p><b>Security.level == high</b><br/>
- session timeout is multiplied by a factor of 10<br/>
- cookie lifetime is set to 0<br/>
- config timeout is set<br/>
- inactiveMins is equal to 10</p>
</td>
<td valign="top">
<p><b>Security.level == medium</b><br/>
- session timeout is multiplied by a factor of 100<br/>
- cookie lifetime is set to 7 days<br/>
- inactiveMins is equal to 100</p>
</td>
</tr><tr>
<td valign="top">
<p><b>*Security.level == low</b><br/>
- session timeout is multiplied by a factor of 300<br/>
- cookie lifetime is set to 788940000s<br/>
- inactiveMins is equal to 300</p>
</td>
<td valign="top">
<p><b>Security.level is not set</b><br/>
- session timeout is multiplied by a factor of 10<br/>
- cookie lifetime is set to 788940000s<br/>
- inactiveMins is equal to 300<br/></p>
</td>
</tr>
</tbody></table>

I provided this information to the client and let them decide which scenario met their business needs. For this situation, I recommended commenting out the Security.level configuration so that the session timeout would stay the same, but the cookie lifetime and inactiveMins values would increase.

This was an interesting learning experience that helped me understand a bit more about how CakePHP handles sessions. It also gave me exposure to referer checks in PHP, which I haven’t dealt with much in the past.
