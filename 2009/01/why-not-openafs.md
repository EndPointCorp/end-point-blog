---
author: Steven Jenkins
title: Why not OpenAFS?
github_issue_number: 92
tags:
- openafs
date: 2009-01-28
---



[OpenAFS](https://www.openafs.org/) is not always the right answer for a filesystem. While it is a good network filesystem, there are usage patterns that don’t fit well with OpenAFS, and there are some issues with OpenAFS that should be considered before adopting or using it.

First, if you don’t really need a network filesystem, the overhead of OpenAFS may not be worthwhile. If you mostly write data, but seldom read it across a network, then the cache of OpenAFS may hinder performance rather than help. OpenAFS might not a good place to put web server logs, for example, that get written to very frequently, but seldom read.

OpenAFS is neither a parallel filesystem nor a high-performance filesystem. In high-performance computing (HPC) situations, a single system (or small set of systems) may write a large amount of data, and then a large number of systems may read from that. In general, OpenAFS does not scale well for multiple parallel reads of read-write data, but it scales very well for parallel reads of replicated read-only data. Because read-only replication is not instantaneous, depending on the latencies that can be tolerated, OpenAFS may or may not be a good choice. If you need to write and immediately read gigabytes or terabytes of data, OpenAFS may not work well for you.

It should be noted, though, that Hartmut Reuter and others have developed 
[
extensions to OpenAFS](http://workshop.openafs.org/afsbpw08/talks/thu_3/OpenAFS+ObjectStorage.pdf) that allow for parallel access to read-write data, and their testing has shown that accesses scale linearly with the degree of parallelism. Work to integrate their extensions into core OpenAFS is ongoing.

Additionally, if your environment needs to leverage special-purpose high-speed networks and does not leverage IP for connectivity, then OpenAFS will not be a good choice. It only communicates over IP and does not do Infiniband or Myrinet, for example.

OpenAFS is also more difficult than NFS or CIFS to set up and administer. For those two products, simple configurations can be set up in minutes, often just requiring editing a few files and/or clicking on a simple GUI to ‘share’ some files. 

OpenAFS, on the other hand, requires configuration on the client, and setup of both fileservers and the other infrastructure servers (e.g., Kerberos, the user and group management server, and the location server). Thus, OpenAFS has a higher hurdle for getting started.

As mentioned, OpenAFS requires [Kerberos](http://www.kerberos.org/). For an environment that already has Kerberos infrastructure, whether via Active Directory, MIT Kerberos, Heimdal, or another implementation, this might not be a large challenge. For an environment that does not leverage Kerberos, though, determining the right Kerberos infrastructure, the policies to manage it, and getting the implementation done can be a significant hurdle.

Also, as OpenAFS has its own user and group management components, the interaction of those with existing components (or lack thereof) also needs to be resolved. An organization that uses LDAP (or Active Directory), for example, might need to leverage some add-ons to more smoothly integrate with OpenAFS, or new code might need to be written to make that integration work better.

While both Kerberos and integration of user and group management are good system administration practices, for an organization that does not already have these practices, needing to adopt them in order to reasonably evaluate and use OpenAFS can be daunting.

The filesystem semantics of OpenAFS can also be a barrier to adoption. OpenAFS only uses the owner bits for Unix file permissions, for example, so the group and other bits are completely unused (OpenAFS preserves them, but just doesn’t consult them for access control). This can cause issues with software that relies on group permissions to manage access. OpenAFS uses access control lists (ACLs) to do this, which are similar to those used on Windows but do not implement the traditional Unix semantics.

Another semantic difference is that OpenAFS does not implement byte-range locking but only implements file-level locking. Some software (e.g., Microsoft Access) requires byte-range locking in order to work properly; thus, OpenAFS is not a good place to store Microsoft Access databases.

Network filesystems often have semantic differences from local filesystems, and OpenAFS is no different. For OpenAFS, the big difference for developers is that it does not implement write on commit semantics but rather write on close. In other words, when a client issues a write request, that request does not necessarily cause other clients reading the data to be aware of the new contents. Instead, OpenAFS will write on the closing of the file (or an fsync() call). While this is not necessarily specific to OpenAFS, it is a subtlety of networked filesystems that many developers may not be aware of, so they need to be more careful about checking the return status of file close() calls, and they also need to be aware of the differences so that they can properly handle an cross-system coordination if based on contents of files.

While OpenAFS is a solid network filesystem, there are scenarios in which OpenAFS might be too heavyweight, might not perform as well as needed, or behave differently from what is required. Understanding these issues is helpful in making a reasoned choice about a network filesystem.


