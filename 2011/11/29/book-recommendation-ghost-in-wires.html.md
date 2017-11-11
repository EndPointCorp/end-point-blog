---
author: Steph Skardal
gh_issue_number: 516
tags: books, security
title: 'Book Recommendation: Ghost in the Wires'
---



<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td style="padding-top:10px;" valign="top"><a href="http://www.amazon.com/Ghost-Wires-Adventures-Worlds-Wanted/dp/0316037702"><img border="0" height="280" src="/blog/2011/11/29/book-recommendation-ghost-in-wires/image-0.png"/></a></td>
<td style="padding-left:10px;">
<p>I recently listened to <a href="http://www.amazon.com/Ghost-Wires-Adventures-Worlds-Wanted/dp/0316037702">Ghost in the Wires</a> by Kevin Mitnick as an audiobook during my long Thanksgiving vacation drives. This non-fiction book is a first-person account about Kevin Mitnick's phone and computer break-in (or what he claims to be ethical hacking) adventures in the late eighties and early nineties, and it touches on the following legal proceedings from 1995 on. A couple of interesting things stood out to me:</p>
<ul>
<li>Kevin's tactics revolve around <a href="http://en.wikipedia.org/wiki/Social_engineering_(security)">social engineering</a>, or techniques that capitalize on flaws in "human hardware" to gain information. The book was an eye opener in terms of how easily Kevin gained access to systems, as there are countless examples of Kevin's ability to gain credibility, pretext, introduce diversions, etc.</li>
<li>Another highlight of the book for me was learning details of how bug reports were exploited to gain sensitive information. Kevin gained access to bug reports on proprietary software to exploit the software and gain access to the systems running the software. I don't think of my own clients' bug reports as an extremely valuable source of information for exploiting vulnerabilities to gain user information, but there have been a few instances in the past where bugs could have been used maliciously.</li>
</ul>
</td>
</tr>
</tbody></table>

### Follow-up Comments

One thing that strikes me is how the internet and technology has changed since Kevin's infringements, specifically in the development of open source software. End Point works with open source operating systems, packages, monolithic ecommerce applications, and modular open source elements (e.g. Rails gems, CPAN modules). Bug reports on open source applications are easily accessible. For example, [here](http://weblog.rubyonrails.org/2011/11/18/rails-3-1-2-has-been-released) is an article on the security vulnerabilities in recent versions of Rails.

The responsibility of keeping up with security updates shifts to the website owner leveraging these open source solutions (or the hosting provider and/or developer in some cases). I spoke with a few developers a couple of years ago about how public WordPress security vulnerabilities enable unethical hackers to easily gain access to sites running WordPress without the security updates. With the increased popularity of open source and visibility of security vulnerabilities, it's important to keep up with security updates, especially those which might make sensitive user information available.

With the advancement in technology, security processes should become a normal part of development. For example, End Point has standard security processes in place such as use of ssh keys, firewalls for server access, and PGP encryption. Our clients also follow [PCI compliance](https://www.pcisecuritystandards.org/) regulations regarding storing credit card numbers and security numbers in encrypted form only, or in some cases not at all if a third party payment processor is used. It's nice to use a third party service for storing credit card data since the responsibility of storing sensitive cardholder data shifts to the third party (however, the interaction between your site and the third party must be protected).

This is an interesting read (or listen) that I recommend to anyone working with sensitive information in the tech field. Learning about the social engineering techniques was fascinating in itself and technical bits are scattered throughout the book which make it suitable for tech-savvy and non-tech-savvy readers.


