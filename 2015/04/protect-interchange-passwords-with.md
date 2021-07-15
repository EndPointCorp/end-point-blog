---
author: Mark Johnson
title: Protect Interchange Passwords with Bcrypt
github_issue_number: 1123
tags:
- bcrypt
- ecommerce
- interchange
- security
- sysadmin
date: 2015-04-28
---



Interchange default configurations have not done a good job of keeping up with the best available password security for its user accounts. Typically, there are two account profiles associated with a standard Interchange installation: one for admin users (access table) where the password is stored using Perl’s crypt() command (bad); and one for customers (userdb) where the password isn’t encrypted at all (even worse). Other hashing algorithms have long been available (MD5, salted MD5, SHA1) but are not used by default and have for some time not been useful protection. Part of this is convenience (tools for retrieving passwords and ability to distribute links into user assets) and part is inertia. And no small part was the absence of a strong cryptographic option for password storage until the [addition of Bcrypt](/blog/2014/07/interchange-582-release-with-bcrypt) to the account management module.

The challenge we face in protecting passwords is that hardware continues to advance at a rapid rate, and with more computational power and storage capacity, brute-force attacks become increasingly effective and widely available. Jeff Jarmoc’s [Enough with the Salts](http://chargen.matasano.com/chargen/2015/3/26/enough-with-the-salts-updates-on-secure-password-schemes.html) provides some excellent discussion and background on the subject. To counter the changing landscape, the main line of defense moves toward ensuring that the work required to create and test a given stored password is too expensive, too time-consuming, for brute-force attacks to be profitable.

One of the best options for handling encrypted password storage with a configurable “hardware cost” is Bcrypt. We chose to integrate Bcrypt into Interchange over other options primarily because of its long history of operation with no known exploits, and its cost parameter that allows an administrator to advance the work required to process a password slowly over time as hardware continues to increase in efficiency. The cost feature introduces an exponential increase in calculation iterations (i.e., required processing power and time) as powers of 2, from 1 (2 iterations, essentially no cost) to 31 (2^31, or 2,147,483,648 iterations). Ideally an administrator would want to identify a cost that causes no perceptible penalty to end users, but would be such a burden to any brute-force attack as to have no worthwhile return on investment to crack.

Converting an existing user base from any of the existing encryption schemes to Bcrypt is trivial in Interchange. The existing UserDB profile is changed to the “bcrypt” option and the “promote” boolean set to true. Promote allows your users to continue to validate against their existing stored password, but after the next access will upgrade their storage to the Bcrypt password. In the mean time, a backend process could be developed using the construct_bcrypt() routine in Vend::UserDB to update all outstanding accounts prior to being updated organically.

If the switch on the front end involves going from no encryption to any encrypted storage, including Bcrypt, and your front end uses the default tools for retrieving lost passwords, you’ll also need to construct some new code for resetting passwords instead. There is no such facility for the admin, and since the admin accounts are typically far more valuable than the front end accounts, making the change for the admin should be the first priority and have the least effort involved.

Switching accounts to Bcrypt password storage is a simple, effective means for increasing protection on your users’ and business’ information. Every bit as importantly, it also helps protect your business’ reputation, that can be severely damaged by a data breech. Lastly, in particular for your admin accounts, Bcrypt password storage is useful in meeting PCI DSS requirements for strong password hashing.


