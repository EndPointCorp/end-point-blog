---
author: Jon Jensen
title: On “valid” Unix usernames and one’s sanity
github_issue_number: 44
tags:
- perl
date: 2008-08-13
---

Today poor Kiel Christofferson ran into an agonizing bug. A few weeks ago, building a custom RPM of perl-5.10.0 (that is, the Perl distribution itself) wasn’t a problem. The unit tests passed with nary a care.

But today it no longer worked. I’ll omit details of the many false paths Kiel had to go down in trying to figure out why an obscure test in the Module::Build package was failing. Eventually I took a look and noted that he’d tried all the logical troubleshooting. Time to look at the ridiculous. What if the test was failing because the last time he built it successfully it was under the user “rpmbuild”, while he was now trying with user “rpmbuild-local”?

That was exactly the problem. Module::Build’s tilde directory (~username) parser was of the (false) opinion that usernames consist only of \w, that is, alphanumerics and underscores. The reality is that pretty much anything is valid in a username, though some characters will cause trouble in various contexts (think of / : . for example).

I explained in more detail in [CPAN bug #33492](https://rt.cpan.org/Public/Bug/Display.html?id=33492) which reports someone else’s experience with the test failing when the username had a backslash in it, such as the Active Directory name “RIA\dillman”.

Fun times.
