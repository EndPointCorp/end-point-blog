---
author: Brian Buchalter
gh_issue_number: 568
tags: hosting, monitoring
title: Check HTTP redirects with Nagios
---



Often times there are critical page redirects on a site that may want to be monitored. Often times, it can be as simple as making sure your checkout page is redirecting from HTTP to HTTPS. Or perhaps you have valuable old URLs which Google has been indexing and you want to make sure these redirects remain in place for your PageRank. Whatever your reason for checking HTTP redirects with Nagios, you'll find there are a few scripts available, but none (that I found) which are able to follow more than one redirect. For example, let's suppose we have a redirect chain that looks like this:

```bash
http://myshop.com/cart >> http://www.myshop.com/cart >> https://www.mycart.com/cart
```

### Following multiple redirects

In my travels, I found [check_http_redirect](http://exchange.nagios.org/directory/Plugins/Websites,-Forms-and-Transactions/Check-Http-Redirect/details) on Nagios Exchange. It was a well designed plugin, written by Eugene Kovalenja in 2009 and licensed under GPLv2. After experimenting with the plugin, I found it was unable to traverse multiple redirects. Fortunately, Perl's [LWP::UserAgent](http://search.cpan.org/~gaas/libwww-perl-6.04/lib/LWP/UserAgent.pm) class provides a nifty little option called max_redirect. By revising Eugene's work, I've exposed additional command arguments that help control how many redirects to follow. Here's a summary of usage:

```bash
-U          URL to retrieve (http or https)
        -R          URL that must be equal to Header Location Redirect URL
        -t          Timeout in seconds to wait for the URL to load. If the page fails to load, 
                    check_http_redirect will exit with UNKNOWN state (default 60)
        -c          Depth of redirects to follow (default 10)
        -v          Print redirect chain
```

If check_http_redirect is unable to find any redirects to follow or any of the redirects results in a 4xx or 5xx status code returned, the plugin will report a critical state code and the nature of the problem. Additionally, if the number of redirects exceeds the depth of redirects to follow as specified in the command arguments, it will notify you of this and exit with an unknown state code. An OK status will be returned only if the redirects result in a successful response to a URL which is a regex match against the options specified in the R argument.

The updated [check_http_redirect](https://github.com/bbuchalter/check_http_redirect/blob/master/check_http_redirect.pl) plugin is available on my [GitHub](https://github.com/bbuchalter) page along with several other Nagios plugins I'll write about in the coming weeks. Pull requests welcome, and thank you to Eugene for his original work on this plugin.


