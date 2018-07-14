---
author: Ron Phipps
gh_issue_number: 108
tags: environment, rails
title: Passenger and SELinux
---



We recently ran into an issue when launching a client’s site using Phusion Passenger where it would not function with SELinux enabled. It ended up being an issue with Apache having the ability to read/write the Passenger sockets. In researching the issue we found another engineer had reported the problem and there was discussion about having the ability to configure where the sockets could be placed. This solution would allow someone to place the sockets in a directory other than /tmp and set the context on the directory so that sockets created within it have the same context and then grant httpd the ability to read/write to sockets with that specific context. This is a win over granting httpd the ability to read/write to all sockets in /tmp since many other services place their sockets there and you may not want httpd to be able to read/write to those sockets.

End Point had planned to take on the task of patching passenger and submitting the patch. While collecting information about the issue this morning to pass to Max I found this in the issue tracker for Passenger:

```
Comment 4 by honglilai, Feb 21, 2009 Implemented.

Status: Fixed
Labels: Milestone-2.1.0
```

Excellent! We’ll be testing this internally soon and will post a new blog entry with our solution for Passenger + SELinux. Thanks to the Passenger engineers for taking the request seriously and working on an update with the PassengerTempDir configuration directive included.


