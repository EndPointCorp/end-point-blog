---
author: Steve McIntosh
gh_issue_number: 58
tags: security
title: Small changes can lead to significant improvements
---

Case in point: We've been investigating various system management tools for both internal use and possibly for some of our clients. One of these, Puppet from Reductive Labs has a lot of features that I like a lot and good references (Google uses it to maintain hundreds of Mac OS X laptop workstations).

I was asked to see if I could identify any performance bottlenecks and perhaps fix them. With the aid of dtrace (on my own Mac OS X workstation) and the Ruby dtrace library it was easy to spot that **a lot** of time was being eaten up in the "checksumming" routines.

As with all system management tools, security is really important and part of that security is making sure the files you are looking at and using are exactly the files you think they are. Thus as part of surveying a system for modified files, they are each checksummed using an MD5 hash.

To speed things up, at a small reduction in security, the Puppet checksumming routines have a "lite" option which only feeds the first 512 bytes of a file into the MD5 algorithm instead of the entire file, which can be quite large.

As with most security packages these days, the way you implement an MD5 hash is to get a "digest" object, initialized to use the MD5 algorithm. When Puppet checksums a file, it opens it and reads it in 512 byte chunks, handing each chunk to the digest to ... digest.  If the "lite" option is set, it stops after the first chunk.

Hard to see how we can improve on that, but it can be done. All of the digest methods, anticipating how they're going to be used most of the time, have a "file" option. You create the digest then hand it the file path.

The digest does the rest, and since it's part of a package which is part of the Ruby distribution, it's probably coded in compiled C and not interpreted.

Based on a number of benchmark tests using files both large and small we've found this small change yields about a 10% increase in performance and since this operation may be done hundreds of times for a single update run, that can add up.

(If you're interested in some of the raw numbers, please take a look at [http://stevemac.endpoint.com/puppet.html](http://stevemac.endpoint.com/puppet.html) for a summary of the original analysis and links or visit the Puppet developers forum at [http://groups.google.com/group/puppet-dev](http://groups.google.com/group/puppet-dev) and scan the archives).
