---
author: Josh Williams
gh_issue_number: 642
tags: security
title: 'Security review with Kiel: Time to be paranoid.'
---



<a href="https://www.flickr.com/photos/80083124@N08/7372414906/" style="clear:right; float:right; margin-left:1em; margin-bottom:1em" title="IMG_0814.JPG by endpoint920, on Flickr"><img alt="IMG_0814.JPG" height="180" src="/blog/2012/06/14/security-review-with-kiel-time-to-be/image-0.jpeg" width="240"/></a>

Interesting! From storing encrypted documents and occasionally signing email, to its usage in pgcrypto in Postgres, I’ve done a bit with PGP keys and public key cryptography. But Kiel’s been running through a quick tutorial on security topics, and some of the PKI components are more important than I originally realized. For instance, part of the security that the public key infrastructure provides is the web of trust, which defines how identities can be automatically trusted based on which keys have signed and trusted other keys. In fact, we’re about to have a key signing party...

In the mean time Kiel reminded us of some of the concerns surrounding other forms of PKI cryptography. The SSL infrastructure, for instance, relies on a set of provided certificate authorities which are assumed to be trusted, but may not be reliable. Plug-ins like Certificate Patrol can help, though. Of course also, as indicated by the recent collission attack, MD5 is no longer secure, and a number of CA’s still use it.

More generally, the security ninja reminded us of where security breaches can occur and how they can affect us, even if they happen in a space far outside our control. But there are a number of things we can control, so he gave us a few tips to follow:

- Use full disk encryption, or something like TrueCrypt that’ll encrypt data on the fly.
- Make use of public key cryptography where possible, even (or especially) on your local laptop.
- Get your public key out there, where people can see and mututally identify it.
- Also, lock your system when you walk away.
- Make sure your backups are secure.
- Avoid password re-use, of course.
- Avoid SQL injection attacks. (Oh wait, that was Greg’s talk.)

Now I’m feeling really paranoid.


