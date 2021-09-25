---
author: Greg Sabino Mullane
title: Verifying Postgres tarballs with PGP
github_issue_number: 240
tags:
- database
- open-source
- postgres
- security
date: 2009-12-21
---



If you are downloading the [Postgres source code tarballs](https://www.postgresql.org/ftp/source/) from a mirror, how can you tell if these are the same tarballs that were created by the packagers? You can’t really—​although they come with a MD5 checksum file, these files are packaged right alongside the tarballs themselves, so it would be easy enough for someone to create an evil tarball along with a new MD5 file. All you could do is perhaps check if the tarball that came from mirror A has a matching checksum file from mirror B, or even the main repository itself.

One way around this is to use PGP (which almost always means [GnuPG](https://gnupg.org/) in the open-source software world) to digitally sign the tarballs. Until the Postgres project gets an official key and starts doing this, one workaround is to at least know the checksums from one single point in time. To that end, I’ve been digitally signing messages containing the checksums for the tarballs for many years now and posting them to pgsql-announce. You’ll need a copy of [my public key](http://www.gtsm.com/Greg_Sabino_Mullane.key.html) (0x14964AC8m fingerprint 2529 DF6A B8F7 9407 E944 45B4 BC9B 9067 1496 4AC8) to verify the messages. A copy of the latest announcement message is below.

Note that I’ve also added a sha1sum for each tarball, as a precaution against relying on a single MD5 checksum (sha1sum does a SHA-1 checksum, naturally). Also note that rather than signing each tarball, I’ve simply signed a message containing the checksums for each one.

While this is far from a fool-proof system, it’s much, much better than the existing system, and provides a way for changed tarballs to be detected. If anyone ever finds a mismatch please let me know (or better yet, email pgsql-general@postgresql.org)

```plain
-----BEGIN PGP SIGNED MESSAGE-----                                   
Hash: RIPEMD160                                                      

Source code MD5 and SHA1 checksums for PostgreSQL 
versions 8.4.2, 8.3.9, 8.2.15, 8.1.19, 8.0.23, and 7.4.27

For instructions on how to use this file to verify Postgres 
tarballs, please see:                                       

http://www.gtsm.com/postgres_sigs.html

## Created with md5sum:
1bc9cdc76c6a2a13bd7fdc0f3f53667f  postgresql-8.4.2.tar.gz
d738227e2f1f742d2f2d4ab56496c5c6  postgresql-8.4.2.tar.bz2
4f176a4e7c0a9f8a7673bec99d1905a0  postgresql-8.3.9.tar.gz 
e120b001354851b5df26cbee8c2786d5  postgresql-8.3.9.tar.bz2
a9d97def309c93998f4ff3e360f3f226  postgresql-8.2.15.tar.gz
e6f2274613ad42fe82f4267183ff174a  postgresql-8.2.15.tar.bz2
335d8c42bd6e7522bb310d19d1f9a91b  postgresql-8.1.19.tar.gz 
ba84995e1e2d53b0d750b75adfaeede3  postgresql-8.1.19.tar.bz2
eb35f66d1c49d87c27f2ab79f0cebf8e  postgresql-8.0.23.tar.gz 
1c6fac4265e71b4f314a827ca5f58f6a  postgresql-8.0.23.tar.bz2
77d09f4806bd913820f82abc27aca70e  postgresql-7.4.27.tar.gz 
1fd1d2702303f9b29b5dba1ec4e1aade  postgresql-7.4.27.tar.bz2

## Created with sha1sum:
563caa3da16ca84608e5ff9c487753f3bd127883  postgresql-8.4.2.tar.gz
a617698ef3b41a74fe2c4af346172eb03e7f8a7f  postgresql-8.4.2.tar.bz2
6ee1e384bdd37150ce6fafa309a3516ec3bbef02  postgresql-8.3.9.tar.gz 
5403f13bb14fe568e2b46a3350d6e28808d93a2c  postgresql-8.3.9.tar.bz2
bd803d74bf9aeac756cb69ae6c1c261046d90772  postgresql-8.2.15.tar.gz
4de199b3223dba2164a9e56d998f6deb708f0f74  postgresql-8.2.15.tar.bz2
233a365985a5a636a97f9d1ab4e777418937caed  postgresql-8.1.19.tar.gz 
f1667a64e92a365ae3d46903382648bdc0daa1ba  postgresql-8.1.19.tar.bz2
7783dc54638e044cff3c339d9fd960a9b65a31df  postgresql-8.0.23.tar.gz 
a2c37eb802a4d67bc2508f72035dae6fb29494df  postgresql-8.0.23.tar.bz2
405909d755aa907fc176d22d1b51d6b5704eb3b4  postgresql-7.4.27.tar.gz 
bb35cc844157b8a0d0b2e9e1ab25b6597c82dd1c  postgresql-7.4.27.tar.bz2

- -- 
Greg Sabino Mullane greg@turnstep.com
PGP Key: 0x14964AC8 200912151528     
http://biglumber.com/x/web?pk=2529DF6AB8F79407E94445B4BC9B906714964AC8

-----BEGIN PGP SIGNATURE-----

iEYEAREDAAYFAksoDPgACgkQvJuQZxSWSsikVQCgiE34ycdexL9lwSfZ+TLTZh5m
G3AAnRkazEu/uHLJCNvDZe2cmqCrCkem                                
=HjAS                                                           
-----END PGP SIGNATURE-----
```

