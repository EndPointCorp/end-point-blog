---
author: Tim Case
gh_issue_number: 739
tags: ecommerce, javascript
title: Verify Addresses the Easy Way with SmartyStreets
---



Adding an address form is a pretty common activity in web apps and even more so with ecommerce web apps.  Validations on forms allow us to guide the user to filling out all required fields and to make sure the fields conform to basic formats.  Up until now going further with addresses to verify they actually exist in the real world was a difficult enough task that most developers wouldn't bother with it. Imagine though the cost to the merchant who ships something to the wrong state because the customer accidently selected "SD" (South Dakota) when they thought they were selecting "SC" (South Carolina), a simple enough mistake to make and one that wouldn't be caught by most address forms.  In today's ecommerce world customers expect deliveries to be fast and reliable, and in this case the customer would have to wait until the package is returned to the merchant with "Address Unknown" only to have to wait even longer for the reshipment.  Even worse for the merchant, maybe the package never gets returned.  

[SmartyStreets](http://smartystreets.com/) is a new API web app that I implemented for our client [Mobixa](http://mobixa.com), a web app that allows people to sell their used mobile phones.  [Mobixa](http://mobixa.com) sends shipping labels and payment checks to customers so that they can send their phones to [Mobixa](http://mobixa.com) and get paid for it. Wrong addresses can delay the whole process and [Mobixa](http://mobixa.com) wanted to reduce the number of bad addresses that were being keyed in by the customers.  [SmartyStreets](http://smartystreets.com/) provides an easy way for developers to allow Address verification to their web forms so that addresses are verified against the US Postal Service's valid addresses.   [SmartyStreets](http://smartystreets.com/) is [CASS](http://en.wikipedia.org/wiki/Coding_Accuracy_Support_System) certified meaning that they meet the USPS accuracy requirements.

The big advantage of Smarty Streets is that adding address verification to a form can be as easy as adding a link to their jQuery based plugin and then a script tag with your [SmartyStreets](http://smartystreets.com/) API key.  The plugin autodetects address fields and when a minimum of 3 fields are entered (address, city, state), it will display an indicator sprite to the user and send an async request to the API for verification.  The verification has three possible outcomes:

1. The address is verified.  A valid address will display a verified image to the side of the zip code and all of the address fields will be modified with a more "correct" address, with correct being defined as what matches the USPS official definition for the matched address.  Zip codes will be modified with the carrier route code, so "92806" becomes "92806-3433".  An address modification would for example change "1735 pheasant" to "1731 N Pheasant St.". Proper casing and spelling errors will also be enacted.

1. The address is ambiguous.  An ambiguous address is one that returns multiple matches. Let's say for example that "1 Rosedale St.", could be "1 N Rosedale Street" or "1 S Rosedale Street".  In this case it displays a popup which allows the user to select the correct address or to override the suggestions and continue with the address they entered.

1. The address is invalid.  An invalid address informs the user that it's invalid and both the invalid address and the ambiguous address offer the user two additional choices.  "Double checking the address" will rerun the address validation after the user has modified the address.  "I certify that what I type is correct", is a second choice which allows the user to continue with the address they typed.  This last choice is important because it allows the user the power to continue with what they want instead of forcing them to conform to the address validation.

Checks are performed when [SmartyStreets](http://smartystreets.com/) senses that it has enough address information to run a search.  During this time the submit button to the form is disabled until the check is completed.  Once a check is performed once, it will not perform again unless the user elects to "Double check" the address, this is a good design choice to prevent the user from getting stuck in an infinite loop of sorts.

Our implementation of [SmartyStreets](http://smartystreets.com/) into [Mobixa](http://mobixa.com) included customizing it to do things a little bit differently than the out of the box defaults.  The jQuery plugin comes with many events and hooks for adding customization and if you want to go your own way you can implement everything on the frontend save for the API call yourself. Documentation on the website is useful, and the developers of [SmartyStreets](http://smartystreets.com/) conveniently answered my questions via an Olark chat window.

The costs of [SmartyStreets](http://smartystreets.com/) is that you have to spend time to implement it in your app, a monthly fee based on number of API calls, and also that your UI flow will change slightly in that the user will need to wait for the API call to complete before submitting the form.  I don't always implement validation when I have an address form in an app, but when I do, I like to use [SmartyStreets](http://smartystreets.com/).


