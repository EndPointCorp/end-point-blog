---
author: Jon Jensen
gh_issue_number: 1142
tags: programming
title: Nothing more permanent than a temporary fix
---



A brief thought:

You may have heard the saying that nothing is more permanent than a temporary fix. Or that prototypes are things we just haven’t yet recognized will be permanent. Or some variation on the theme.

As an illustration of this, I recently came across the initial commit to the source code repository of our endpoint.com website when we ported it to Ruby on Rails back in April 2007. Our then co-worker PJ’s comment is a perfect example of how long-lasting some of our planned temporary work can be:

```nohighlight
commit 2ee55da6ed953c049b3ef6f9f132ed3c1e0d4de9
Author: PJ Cabreras <pj@endpoint.com>
Date:   Wed Apr 18 13:07:46 2007 +0000

    Initial test setup of repository for mkcamp testing -- will probably throw away later
    
    git-svn-id: file:///home/camp/endpoint/svnrepo/trunk@1 7e1941c4-622e-0410-b359-a11864f70de7

```

It’s wise to avoid big architecture up front for experimental things we don’t know the needed shape and size of. But we should plan on iterating and being agile (in the real basic sense of the word), because we may never have the chance to start over from scratch. And starting over from scratch is often ill-advised in any case.


