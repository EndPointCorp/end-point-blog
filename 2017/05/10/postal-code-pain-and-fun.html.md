---
author: Jon Jensen
gh_issue_number: 1304
tags: ecommerce, perl, ruby, shipping
title: Postal code pain and fun
---

<img align="right" src="/blog/2017/05/10/postal-code-pain-and-fun/image-0.jpeg" style="margin: 1em" width="200"/>We do a lot of ecommerce development at End Point. You know the usual flow as a customer: Select products, add to the shopping cart, then check out. Checkout asks questions about the buyer, payment, and delivery, at least. Some online sales are for “soft goods”, downloadable items that don’t require a delivery address. Much of online sales are still for physical goods to be delivered to an address. For that, a postal code or zip code is usually required.

### No postal code?

I say *usually* because there are some countries that do not use postal codes at all. An ecommerce site that expects to ship products to buyers in one of those countries needs to allow for an empty postal code at checkout time. Otherwise, customers may leave thinking they aren’t welcome there. The more creative among them will make up something to put in there, such as “00000” or “99999” or “NONE”.

Someone has helpfully assembled and maintains a machine-readable (in Ruby, easily convertible to JSON or other formats) [list of the countries that don’t require a postal code](https://gist.github.com/kennwilson/3902548). You may be surprised to see on the list such countries as Hong Kong, Ireland, Panama, Saudi Arabia, and South Africa. Some countries on the list actually do have postal codes but do not require them or commonly use them.

### Do you really need the customer’s address?

<img align="right" src="/blog/2017/05/10/postal-code-pain-and-fun/image-1.jpeg" style="margin: 1em" width="200"/>When selling both downloadable and shipped products, it would be nice to not bother asking the customer for an address at all. Unfortunately even when there is no shipping address because there’s nothing to ship, the billing address is still needed if payment is made by credit card through a normal credit card payment gateway—​as opposed to PayPal, Amazon Pay, Venmo, Bitcoin, or other alternative payment methods.

The credit card [Address Verification System (AVS)](https://en.wikipedia.org/wiki/Address_Verification_System) allows merchants to ask a credit card issuing bank whether the mailing address provided matches the address on file for that credit card. Normally only two parts are checked: (1) the street address numeric part, for example, “123” if “123 Main St.” was provided; (2) the zip or postal code, normally only the first 5 digits for US zip codes, and often non-US postal code AVS doesn’t work at all with non-US banks.

Before sending the address to AVS, validating the *format* of postal codes is simple for many countries: 5 digits in the US (allowing an optional *-nnnn* for ZIP+4), and 4 or 5 digits in most others countries—​see the Wikipedia [List of postal codes](https://en.wikipedia.org/wiki/List_of_postal_codes) in various countries for a high-level view. Canada is slightly more complicated: 6 characters total, alternating a letter followed by a number, formally with a space in the middle, like K1A 0B1 as explained in Wikipedia’s [components of a Canadian postal code](https://en.wikipedia.org/wiki/Postal_codes_in_Canada#Components_of_a_postal_code).

So most countries’ postal codes can be validated in software with simple regular expressions, to catch typos such as transpositions and missing or extra characters.

### UK postcodes

<img align="right" src="/blog/2017/05/10/postal-code-pain-and-fun/image-2.jpeg" style="margin: 1em" width="200"/>The most complicated postal codes I have worked with is the United Kingdom’s, because they can be from 5 to 7 characters, with an unpredictable mix of letters and numbers, normally formatted with a space in the middle. The benefit they bring is that they encode a lot of detail about the address, and it’s possible to catch transposed character errors that would be missed in a purely numeric postal code. The Wikipedia article [Postcodes in the United Kingdom](https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom) has the gory details.

It is common to use a regular expression to validate UK postcodes in software, and many of these regexes are to some degree wrong. Most let through many invalid postcodes, and some disallow valid codes.

We recently had a client get a customer report of a valid UK postcode being rejected during checkout on their ecommerce site. The validation code was using a regex that is widely copied in software in the wild:

```nohighlight
[A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]?[0-9][ABD-HJLN-UW-Z]{2}
```

(This example removes support for the odd exception GIR 0AA for simplicity’s sake.)

The customer’s valid postcode that doesn’t pass that test was W1F 0DP, in London, which the Royal Mail website confirms is valid. The problem is that the regex above doesn’t allow for F in the third position, as that was not valid at the time the regex was written.

This is one problem with being too strict in validations of this sort: The rules change over time, usually to allow things that once were not allowed. Reusable, maintained software libraries that specialize in UK postal codes can keep up, but there is always lag time between when updates are released and when they’re incorporated into production software. And copied or customized regexes will likely stay the way they are until someone runs into a problem.

The ecommerce site in question is running on the [Interchange](http://www.icdevgroup.org/) ecommerce platform, which is based on Perl, so the most natural place to look for an updated validation routine is on CPAN, the Perl network of open source library code. There we find the nice module [Geo::UK::Postcode](https://metacpan.org/pod/Geo::UK::Postcode) which has a more current validation routine and a nice interface. It also has a function to format a UK postcode in the canonical way, capitalized (easy) and with the space in the correct place (less easy).

It also presents us with a new decision: Should we use the basic “valid” test, or the “strict” one? This is where it gets a little trickier. The “valid” check uses a regex validation approach will still let through some invalid postcodes, because it doesn’t know what all the current valid delivery destinations are. This module has a “strict” check that uses a [comprehensive list of all the “outcode” data](https://github.com/mjemmeson/Geo-UK-Postcode-Regex/blob/master/lib/Geo/UK/Postcode/Regex.pm#L664-L3652)—​which as you can see if you look at that source code, is extensive.

The bulkiness of that list, and its short shelf life—​the likelihood that it will become outdated and reject a future valid postcode—​makes strict validation checks like this of questionable value for basic ecommerce needs. Often it is better to let a few invalid postcodes through now so that future valid ones will also be allowed.

The ecommerce site I mentioned also does in-browser validation via JavaScript before ever submitting the order to the server. Loading a huge list of valid outcodes would waste a lot of bandwidth and slow down checkout loading, especially on mobile devices. So a more lax regex check there is a good choice.

### When Christmas comes

There’s no Christmas gift of a single UK postal code validation solution for all needs, but there are some fun trivia notes in the Wikipedia page covering [Non-geographic postal codes](https://en.wikipedia.org/wiki/Postal_code#Non-geographic_codes):

> A fictional address is used by UK Royal Mail for letters to Santa Claus:
> 
> Santa’s Grotto  
> Reindeerland XM4 5HQ
> 
> Previously, the postcode SAN TA1 was used.
> 
> In Finland the special postal code 99999 is for Korvatunturi, the place where Santa Claus (Joulupukki in Finnish) is said to live, although mail is delivered to the Santa Claus Village in Rovaniemi.
> 
> In Canada the amount of mail sent to Santa Claus increased every Christmas, up to the point that Canada Post decided to start an official Santa Claus letter-response program in 1983. Approximately one million letters come in to Santa Claus each Christmas, including from outside of Canada, and they are answered in the same languages in which they are written. Canada Post introduced a special address for mail to Santa Claus, complete with its own postal code:
>
> SANTA CLAUS  
> NORTH POLE  H0H 0H0
> 
> In Belgium bpost sends a small present to children who have written a letter to Sinterklaas. They can use the non-geographic postal code 0612, which refers to the date Sinterklaas is celebrated (6 December), although a fictional town, street and house number are also used. In Dutch, the address is:
> 
> Sinterklaas  
> Spanjestraat 1  
> 0612 Hemel
>
> This translates as “1 Spain Street, 0612 Heaven”. In French, the street is called “Paradise Street”:
> 
> Saint-Nicolas  
> Rue du Paradis 1  
> 0612 Ciel

That UK postcode for Santa doesn’t validate in some of the regexes, but the simpler Finnish, Canadian, and Belgian ones do, so if you want to order something online for Santa, you may want to choose one of those countries for delivery. :)
