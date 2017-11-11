---
author: Josh Williams
gh_issue_number: 1179
tags: postgres, replication, ssl, sysadmin
title: Odd pg_basebackup Connectivity Failures Over SSL
---

A client recently came to me with an ongoing mystery: A remote Postgres replica needed replaced, but repeatedly failed to run pg_basebackup. It would stop part way through every time, reporting something along the lines of:

```
pg_basebackup: could not read COPY data: SSL error: decryption failed or bad record mac
```

The first hunch we had was to turn off SSL renegotiation, as that isn't supported in some OpenSSL versions. By default it renegotiates keys after 512MB of traffic, and setting ssl_renegotiation_limit to 0 in postgresql.conf disables it. That helped pg_basebackup get much further along, but they were still seeing the process bail out before completion.

The client's Chef has a strange habit of removing my ssh key from the database master, so while that was being fixed I connected in and took a look at the replica. Two pg_basebackup runs later, a pattern started to emerge:

```
$ du -s 9.2/data.test*
67097452        9.2/data.test
67097428        9.2/data.test2
```
While also being a nearly identical size, those numbers are also suspiciously close to 64GB. I like round numbers, when a problem happens close to one that's often a pretty good tell of some boundary or limit. On a hunch that it wasn't a coincidence I checked around for any similar references and found a recent openssl package bug report:

[https://rhn.redhat.com/errata/RHBA-2015-0772.html](https://rhn.redhat.com/errata/RHBA-2015-0772.html)

RHEL 6, check. SSL connection, check. Failure at 64 GiB, check. And lastly, a connection with psql confirmed AES-GCM:

```
SSL connection (cipher: DHE-RSA-AES256-GCM-SHA384, bits: 256)
```

Once the Postgres service could be restarted to load in the updated OpenSSL library, the base backup process completed without issue.

Remember, keep those packages updated!
