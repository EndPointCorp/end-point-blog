---
author: Steven Jenkins
gh_issue_number: 86
tags: openafs
title: What is OpenAFS?
---

A common question about OpenAFS adoption is "What is OpenAFS?" Usually,
the person asking the question is somewhat familiar with filesystems, but
doesn't follow the technical details of various filesystems.  This article
is designed to help that reader understand why OpenAFS could be a useful
solution (and understand where it is not a useful solution).

First, the basics. OpenAFS is an open source implementation of AFS:
from the OpenAFS [website](http://www.openafs.org/), OpenAFS
is a heterogeneous system that "offers client-server architecture for
federated file sharing and replicated read-only content distribution,
providing location independence, scalability, security, and transparent
migration capabilities".

Let's break that down:

First, OpenAFS is extremely cross-platform. OpenAFS clients exist for
small devices (e.g., the Nokia tablet) up to mainframes. Do you want
Windows with that? [Not a
problem](http://www.openafs.org/windows.html). On the other hand, OpenAFS servers are primarily available
on Unix-based platforms. Implementations of OpenAFS servers for Windows
do exist, but they are not recommended or supported (If you'd like to
change that, you are welcome to submit patches or to hire developers to
make that change.  That's a major advantage of an open source project.).

The second part of OpenAFS is rather straightforward: it is a
client-server distributed file system. Much like SMB/CIFS in the Windows
world, and NFS in the Unix world, OpenAFS lets file accesses take place
over a network. One feature that sets OpenAFS apart from CIFS and NFS,
though, is its strong file consistency semantics based on its use of
client-side caching and callbacks.  Client-side caching lets clients
access data from their local cache without going across the network for
every access.

Other distributed filesystems allow this as well, but OpenAFS is rather
unusual in that it guarantees that the clients will be notified if
the file changes. This caching plus the consistency guarantees make
OpenAFS especially useful across wide-area networks, not just local area
networks. With respect to consistency, most other distributed filesystems
use timeouts and/or some kind of FIFO or LRU algorithm for determining how
a client handles content in a cache. OpenAFS uses callbacks, which are
a promise from the file server to the client that if the file changes,
the server will contact the client to tell the client to invalidate the
cached contents. That notion of callbacks gives OpenAFS a much stronger
consistency guarantee than most other distributed filesystems.

Another unusual feature in OpenAFS is that it provides a mechanism
for replicated access to read-only data, without requiring any special
hardware or additional high-availability or replication technology. In a
sense, OpenAFS can be considered an inexpensive way to get a read-only
SAN. OpenAFS does this by classifying data as read-write or read-only,
and providing a mechanism to create replicas of read-only data. Up to
11 replicas of data can be made, allowing read access to be very widely
distributed.

The last four features mentioned in the website description are also
very interesting: location independence, scalability, security, and
transparent migration.

OpenAFS provides location independence by separating information about
where a file resides from the actual filesystem itself. This allows
separation of name service from file service, which lets OpenAFS scale
better. It also provides some functionality not present in other networked
filesystems in that changing the location of the data can be more easily
done. Because of the layer of indirection, OpenAFS is able to make a
copy of data behind the scenes, and after that data has been migrated,
to then update the location information. This allows for transparent
migration of data.

Because the location of data is separate from the data itself, if some of
the data is found to be more heavily used, that data can be migrated to a
separate server, so as to better balance out the accesses across multiple
servers. This can be done without negatively impacting the users. This
kind of feature is not usually found in networked filesystems but only
in either higher-end proprietary Network Attached Storage (NAS) systems,
or in Storage Area Networks (SANs).

Because of OpenAFS's use of client-side caching, read-only data, and
separation of location information from the filesystem itself, OpenAFS
can scale up quite well. The initial design of AFS was to be at least
10 times more scalable than the implementations of NFS at that time,
with a client to server ratio of 200:1. While client to server ratios
are highly dependent on hardware and filesystem access patterns, 200:1
is still easily achievable, and much higher ratios have been leveraged
in production environments. 600:1 is achievable in an environment where
the data is predominately read-only.

OpenAFS provides built-in security by leveraging Kerberos to provide
authentication services. The servers themselves rely on Kerberos to ensure
that a rogue host cannot successfully masquerade as an OpenAFS server,
even if DNS is compromised. OpenAFS itself is agnostic with respect to
what kind of Kerberos server is used, as long as it supports the Kerberos
5 protocol standards: a Windows Kerberos Domain Controller can provide
the Kerberos services for an OpenAFS installation, as can an MIT KDC or
a Heimdal one.

Additionally, traffic between the clients and servers can be encrypted
by OpenAFS itself (i.e., not just with SSH or VPN encryption).  This can
provide an extra layer of security.

Overall, OpenAFS provides some of the features of traditional network
filesystems like CIFS and NFS, but with better scalability, consistency
and security. Additionally, because of its ability to replicate and
transparently migrate data, OpenAFS can be leveraged much like a SAN,
but without the proprietary tie-ins to hardware.
