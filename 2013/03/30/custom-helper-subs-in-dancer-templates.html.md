---
author: Jon Jensen
gh_issue_number: 772
tags: dancer, perl
title: Custom helper subs in Dancer templates
---



I recently was writing some code using the [Dancer](http://perldancer.org/) Perl web framework, and had a set of HTML links in the template:

```xml
&lt;a href="/"&gt;Home&lt;/a&gt; |
&lt;a href="/contact"&gt;Contact&lt;/a&gt; |
[etc.]
```

Since it's possible this app could be relocated to a different path, say, /something/deeper instead of merely /, I wanted to use Dancer's handy [uri_for](https://metacpan.org/module/Dancer#uri_for)() routine to get the full URL, which would include any path relocation. (This concept will be familiar to [Interchange 5](http://www.icdevgroup.org/) users from its [area] and [page] tags.)

The uri_for function isn't available in templates. The easiest way to cope would be to just use it in my route sub where it works fine, and store the results in the template tokens as strings. But then for any new URL needed I would have to update the route sub and the template, and this feels like a quintessential template concern.

I found [this blog post](http://quispiam.com/adding-custom-helper-methods-to-dancer-templates/) explaining how to add custom functions to be used in templates, and it worked great. Now my template can look like this:

```xml
&lt;a href="&lt;% uri_for('/') %&gt;"&gt;Home&lt;/a&gt; |
&lt;a href="&lt;% uri_for('contact') %&gt;"&gt;Contact&lt;/a&gt; |
[etc.]
```

And the URLs are output fully qualified:

```nohighlight
http://localhost:3000/
http://localhost:3000/contact
```

Which is not always what I'd want, but in this case is.

The only final concern is that I am using Dancer version 1.3111 and I got this warning upon using the before_template setup mentioned in the blog:

```
Dancer::before_template has been deprecated since version 1.3080. use hooks!
But use hook 'before_template' =&gt; sub {} now instead.
```

So I updated my code, and the final result looks like this:

```perl
hook 'before_template' =&gt; sub {
    my $tokens = shift;
    $tokens-&gt;{uri_for} = \&amp;uri_for;
};
```

And that made both Dancer and me happy.


