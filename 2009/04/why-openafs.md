---
author: Steven Jenkins
title: Why OpenAFS?
github_issue_number: 133
tags:
- openafs
date: 2009-04-24
---

Once you’ve understood [what OpenAFS is](/blog/2009/01/what-is-openafs), you might ask “Why use OpenAFS?” There are several very good reasons to consider OpenAFS.

First, if you need a cross-platform network filesystem, OpenAFS is a
solid choice. While CIFS is the natural choice on Windows, and NFS is
a natural choice on Unix, OpenAFS gives a hetergeneous choice (and it
works on Mac OS X, too).

Setting aside which filesystem is natural for a given platform, though,
OpenAFS has a strong advantage with respect to remote access. While it’s
common to access systems remotely via a Virtual Private Network (VPN),
Secure Shell (SSH), or Remote Desktop, OpenAFS allows the actual files
themselves to be shared across a WAN, a dialup link, or a mobile device
(and since OpenAFS is cross platform, the issue of which remote sets
of remote access software to support is lessened). Having files appear
to be local to the device reduces the need for remote access systems and
simplifies access. The big win, though, is that OpenAFS’ file caching
helps performance and lessens bandwidth requirements.

Another reason to use OpenAFS is if you need your network filesystem to
be secure. While both CIFS and NFS have secure versions, in practice,
they are often configured to be backwards compatible to a least common
denominator and are relatively insecure. Typically, either they trust the
client to be secure (NFS), or the backwards compatibility significantly
lessens security (CIFS). While for an isolated or trusted network,
their security mechanisms may be acceptable, OpenAFS can relied on over an
untrusted network. Common practice for allowing CIFS and/or NFS accesses
over an untrusted network is to leverage a VPN, which introduces yet
another piece of software to manage. On the other hand, OpenAFS ’just
works’ over an untrusted network and it makes no assumptions about the
trustworthiness of the client.

Business growth often drives opening new offices. Sharing data across
those offices can be a challenge, and OpenAFS, because it was designed
to be a wide area filesystem, not just a local area filesystem, shines.
By creating a global namespace and linking the offices together, all
data in all offices can be accessed seamlessly. This can be as simple
as two offices, one central with OpenAFS servers and the other remote,
with only OpenAFS clients, or it can scale up a step to where each remote
office holds file and meta-data servers so that commonly shared local
files can be accessed more quickly. It can even scale up globally with a
more complex environment. Morgan Stanley’s environment as of Spring 2008
had around 500 servers globally, providing OpenAFS file services to tens
of thousands of Unix and Windows clients in approximately 100 offices.
No other network filesystem offers such amazing scalability.

Business challenges often mean closing offices, and OpenAFS’
flexibility works well here, too. Since data can be moved while
on-line, servers in an office can be migrated to a different location,
and OpenAFS clients will automatically get data from the new location,
making removal of the infrastructure in an office straightforward.

OpenAFS’s ability to scale down to a single office and up to a complex
global environment sets it apart from all other network filesystems.
If you need a network filesystem, why not choose OpenAFS? It will let
you grow without having to go through a filesystem switch when you find
that your current choice limits your ability to accomplish your goals.
