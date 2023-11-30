---
author: Jon Jensen
title: Interchange 5.4 Released
github_issue_number: 6
tags:
- interchange
date: 2006-01-07
---

At the end of December 2005, a new major version of [Interchange](/expertise/perl-interchange/) was released, making widely available the improvements developed over the previous year and a half.

While many of the hundreds of important changes are small and incremental, Interchange 5.4 offers a number of larger improvements as well:

- Improved pre-fork server model supports higher traffic.

- Extensible architecture improvements allow more customization (Feature, AccumulateCode, TagRepository, DispatchRoutines).

- Shopping cart triggers have been added, for easier control over complex shopping cart behaviors.

- Multiple "discount spaces" may be defined, for complex discounting schemes.

- The "permanent more" facility allows shared pageable searches, for reduced database load and paging disk space.

- The email interception feature reroutes outgoing email to one or more developer addresses, stopping email from accidentally going to real users during testing.

- Quicker development of email functions using HTML parts or attached files.

- A new demo application, called "Standard", was added.

- Access to loop data in embedded Perl is now easier with the new $Row object.

- User-defined subroutines can be accessed more ways with the new $Sub object.

- More payment gateways are supported, including an interface to CPAN's Business::OnlinePayment.

- More languages are supported in the admin area.

- ... and many other feature enhancements and bugfixes.

Ethan Rowe and [Jon Jensen](/team/jon-jensen/), two End Point engineers and members of the Interchange Development Group, added several of these new features based on work done earlier for our clients. We value highly the whole Interchange team's commitment to stability and reliability in the code, and cooperation and ongoing improvement together. In particular we appreciate the efforts of Mike Heins, Stefan Hornburg, and Davor Ocelic, whose regular contributions make Interchange's progress impressive. And Interchange would be weaker without the valuable work of Kevin Walsh, Ton Verhagen, Jonathan Clark, Dan Browning, Paul Vinciguerra, Ed LaFrance, and others.

We look forward to seeing this latest and greatest version of Interchange being used by the wider Interchange community.
