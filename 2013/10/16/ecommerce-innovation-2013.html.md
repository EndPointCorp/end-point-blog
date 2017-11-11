---
author: Richard Templet
gh_issue_number: 864
tags: camps, community, conference, dancer, database, ecommerce, interchange, perl
title: Ecommerce Innovation 2013
---

Mark Johnson and I went to the [Ecommerce Innovation 2013](http://www.ecommerce-innovation.com/) conference in beautiful Hancock, NY. The event was hosted by Sam Batschelet of [West Branch Resort](http://www.westbranchresort.com/). The conference was spread out over three days and was very well planned. We had plenty of time in between talks to mingle with the other people. All of the talks were very insightful and informative. I found the mixture of technology and marketing talks beneficial. I have already discussed some things with my clients that I learned.

### A brief overview of the talks

- Jure Kodzoman of [Informa](http://www.informa.si/) had two different subjects.

        - His first talk was about Template::Flute which is a Perl based template system which is the default template for Interchange 6. It utilizes the use of html classes to figure out where to parse in the data returned from your Perl code. Overall it seems pretty straight forward to use.
        - His second talk was about the current state of the new Interchange 6 demo store.

- Ana Kozole of Informa had a talk named "Remarketing with Banners" that was really informative.The base of this is to have the ability to show specific banners to visitors on different websites.  She discussed different remarketing techniques including creating specific lists based on different criteria like all visitors, people who got to the checkout page but didn't checkout or people who used a coupon code etc. You can also use remarketing lists for search ads.

- Luka Klemenc of Informa gave two talks.

        - He discussed some a CRM system that they had developed in house and some of the pros and cons.
        - Luka gave us short talk about the ways to know whether or not your newsletter is effective.

- Josh Lavin of [Perusion](http://www.perusion.com) talked about a new template for Interchange 5 called Strap which is based on [Bootstrap](http://getbootstrap.com/2.3.2/) version 2.3.2. With this new template they have created a bunch of page and url changes to make the stock Interchange much more SEO friendly. This also makes a few underlying changes like assuming the username to login would be your email address and creating a multiple page checkout.

- Mike Heins of Perusion gave us a brief history of Interchange and compared it to modern day frameworks like Dancer. He also gave us a brief overview of PCI compliance and how Interchange holds up. He introduced us to the features of the Perusion Payment Server which is a remote credit card processing system that helps with PCI compliance.

- Stefan Hornburg of [LinuXia Systems](http://www.linuxia.de/) discussed two different topics with us.

        - gave us an overview of where the Interchange 6 project currently is and where it's going. He gave us some code samples of the way we can do simple things like add an item to the cart, fetch the subtotal of the cart and talk to the database.
        - Stefan walked us through an integration he did for OpenERP with Interchange 5 using RPC::XML.

- [Mark Johnson](/team/mark_johnson) gave us a review of the modifications to Interchange 5 to allow web servers like [nginx](http://www.nginx.com) or [Apache](http://www.apache.org) to cache entire pages. He discussed how we modified Interchange 5 for a customer to help with a DDoS attack. He laid out all of the new usertags and directives you will need to set to get pages to be cachable including some "gotchas" like not sending cookie information if you want this page to be cached. We hope that this feature will be included in the Interchange 5.8.1 release.

- Sam Batschelet gave a talk about [DevCamps](http://www.devcamps.org/) and the reasons why it is so great. He discussed things like using Perlbrew and Carton in camps to help get around the fact that most Linux operating systems ship with a pretty old version of Perl. He also expanded on a few features that we hope to get released soon.

The last big item on the schedule was a 2 hour round table discussion about the database schema for Interchange 6. It was a very good discussion with many different opinions for adjustments. Most of us based our suggestions on past experience with clients. I do not think we are finished making adjustments to it but we are on the right path to a very flexible setup.

Overall I thought the conference was a great success. It was great to meet in person some people I had only seen on a mailing list before and pass around ideas for the future. I cannot wait to see what cool new things we will have to discuss next year!
