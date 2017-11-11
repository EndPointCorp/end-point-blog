---
author: Jon Jensen
gh_issue_number: 174
tags: mobile
title: Gmail Contacts Notes Converter
---

As I [mentioned previously](http://blog.endpoint.com/2009/05/google-io-2009-day-1.html), I recently got a Google Ion phone running Android. I recently began using it as my main mobile phone, and thus needed to finally migrate the contacts from my Nokia 6126 phone to Android.

This is apparently easy to do by first copying all the contacts from the Nokia 6126 internal memory to the SIM card, then moving the SIM card to the Ion and importing the contacts. But that only works if all your contacts fit on the SIM card. If not, they're truncated, and you have to delete many contacts on the Nokia to fit more, which would be a nonreversable move.

Several posts describe ways to do the export and import, such as [this one](http://blog.lickmyear.org/2009/01/story-of-nokia-and-android-contact.html) that didn't really apply to my phone, and [this one that involves VCF export & import](http://www.javaworld.com/community/node/2184) which I didn't see a way to do.

Ultimately I found an article that described [Nokia's PC Suite](https://www.nokiausa.com/get-support-and-software/software/nokia-suites-for-your-pc) software that I'd never heard of before, which I downloaded on an old Windows machine and used to download the contacts from the phone via Bluetooth, then export to a CSV file and import into Gmail. So far, so good.

Except as [this post](http://forums.t-mobile.com/tmbl/board/message?board.id=Android3&thread.id=20593) and [another post](http://www.theinquirer.net/inquirer/news/1049400/fiddling-with-android-does-your-brain-in) describe, then all the contact data showed up in a single Notes field, useless for dialing or emailing.

I decided it would be easiest to convert the Notes data into normal phone fields since I already had some contact information in the phone and couldn't find any other reasonable way.

I came up with this [Gmail Contacts Notes Converter](http://gist.github.com/151139) script to solve the problem. It takes Gmail-exported CSV as input, converts any Notes field data into standard Work or Personal contacts, and outputs CSV that can be re-imported into Gmail. It requires Perl 5.10.0 and I've only tested it on Linux. (It could be modified to work with earlier Perl versions fairly easily.)

Perhaps it will be useful to someone else as well.
