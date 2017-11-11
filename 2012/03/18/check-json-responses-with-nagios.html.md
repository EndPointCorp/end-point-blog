---
author: Brian Buchalter
gh_issue_number: 571
tags: hosting, monitoring
title: Check JSON responses with Nagios
---



As the developer's love affair with JSON [continues](http://blog.programmableweb.com/2010/08/11/is-json-the-developers-choice/) [to](http://stereolambda.com/2010/03/19/why-is-json-so-popular-developers-want-out-of-the-syntax-business/) [grow](https://devcentral.f5.com/weblogs/macvittie/archive/2011/04/27/the-stealthy-ascendancy-of-json.aspx), the need to monitor successful JSON output does as well. I wanted a Nagios plugin which would do a few things:

- Confirm the content-type of the response header was "application/json"
- Decode the response to verify it is parsable JSON
- Optionally, verify the JSON response against a data file

### Verify content of JSON response

For the most part, Perl's [LWP::UserAgent](http://search.cpan.org/~gaas/libwww-perl-6.04/lib/LWP/UserAgent.pm) class makes short work of the first requirement. Using $response->header("content-type") the plugin is able to check the content-type easily. Next up, we use the [JSON module's decode function](http://search.cpan.org/~makamaka/JSON-2.53/lib/JSON.pm#decode_json) to see if we can successfully decode $response->content.

Optionally, we can give the plugin an absolute path to a file which contains a Perl hash which can be iterated through in attempt to find corresponding key/value pairs in the decoded JSON response. For each key/value in the hash it doesn't find in the JSON response, it will append the expected and actual results to the output string, exiting with a critical status. Currently there's no way to check a key/value does not appear in the response, but feel free to make a pull request on [check_json](https://github.com/bbuchalter/check_json) on my GitHub page.


