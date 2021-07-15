---
author: Patrick Lewis
title: Parsing Email Addresses in Rails with Mail::Address
github_issue_number: 1041
tags:
- email
- rails
date: 2014-10-03
---

I've recently discovered the Mail::Address class and have started using it for storing and working with email addresses in Rails applications. Working with an email address as an Address object rather than a String makes it easy to retrieve different parts of the address and I recommend trying it out if you're dealing with email addresses in your application.

[Mail](https://github.com/mikel/mail) is a Ruby library that handles email generation, parsing, and sending. Rails' own ActionMailer module is dependent on the Mail gem, so you'll find that Mail has already been included as part of your Rails application installations and is ready for use without any additional installation or configuration.

The Mail::Address class within the library can be used in Rails applications to provide convenient, object-oriented ways of working with email addresses.

The [class documentation](http://rdoc.info/github/mikel/mail/Mail/Address) provides some of the highlights:

```ruby
a = Address.new('Patrick Lewis (My email address) <patrick@example.endpoint.com>')
a.format       #=> 'Patrick Lewis <patrick@example.endpoint.com> (My email address)'
a.address      #=> 'patrick@example.endpoint.com
a.display_name #=> 'Patrick Lewis'
a.local        #=> 'patrick'
a.domain       #=> 'example.endpoint.com'
a.comments     #=> ['My email address']
a.to_s         #=> 'Patrick Lewis <patrick@example.endpoint.com> (My email address)'
```

Mail::Address makes it trivial to extract the username, domain name, or just about any other component part of an email address string. Also, its #format and #to_s methods allow you to easily return the full address as needed without having to recombine things yourself.

You can also build a Mail::Address object by assigning email and display name strings:

```ruby
a = Address.new
a.address = "patrick@example.endpoint.com"
a.display_name = "Patrick Lewis"
a #=> #<Mail::Address:69846669408060 Address: |Patrick Lewis <patrick@example.endpoint.com>| >
a.display_name = "Patrick J. Lewis"
a #=> #<Mail::Address:69846669408060 Address: |"Patrick J. Lewis" <patrick@example.endpoint.com>| >
a.domain #=> "example.endpoint.com"
```

This provides an easy, reliable way to generate Mail::Address objects that catches input errors if the supplied address or display name are not parseable.

I encourage anyone who's manipulating email addresses in their Rails applications to try using this class. I've found it especially useful for defining application-wide constants for the 'From' addresses in my mailers; by creating them as Mail::Address objects I can access their full strings with display names and addresses in my mailers, but also grab just the email addresses themselves for obfuscation or other display purposes in my views.
