---
author: Kamil Ciemniewski
title: 'Announcing Ruby gem: email_verifier'
github_issue_number: 740
tags:
- ruby
- rails
date: 2012-12-21
---



How many times have you tried to provide a really nice validation solution for our fields containing user emails? Most of the time - the best we can come up with is some long and incomprehensible Regex we find on [StackOverflow](http://stackoverflow.com/questions/201323/using-a-regular-expression-to-validate-an-email-address) or somewhere else on the Internet.

But that's really only a partial solution. As much as email format correctness is a tricky thing to get right using regular expressions, it doesn't provide us with any assurance that user entered email address in reality **exists**.

**But it does a great job at finding out some typos and misspellings.. right?**

Yes - but I'd argue that it doesn't cover full range of that kind of data entry errors. The user could fill in 'whatever' and traditional validation through regexes would do a great job at finding out that it's not really an email address. But what I'm concerned with here are all those situations when I fat finger kaml@endpoint.com instead of kamil@endpoint.com.

Some would argue at this point that it's still recoverable since I can find out about the error on the next page in a submission workflow, but I don't want to spend another something-minutes on going through the whole process again (possibly filling out tens of form fields along the way).

And look at this issue from the point of view of a web application owner: You'd like to be sure that all those leads you have in your database point to some real people and that some percentage of them will end up paying you at some point real money, making you a living. What if even 10% of email addresses invalid (being valid email addresses but pointing to no real mailboxes) due to user error? What would that potentially mean to you **in cash**?

### The Solution

Recently, I faced this email validation question for [mobixa.com](http://mobixa.com). (By the way. if you own a smart phone that you'd like to sell - there is no better place than [mobixa.com](http://mobixa.com) to do it!)

The results of my work, I'd like to announce here and now. Please give a warm welcome to a newborn citizen of RubyGems society: [email_verifier](https://github.com/kamilc/email_verifier)

### How does it work?

Email verifier takes a different approach to email validation. Instead of checking just the format of given address in question - it actually tries to connect with a mail server and pretends to send a real mail message. We can call it 'asking mail server if recipient exists'.

### How to use it?

Add this line to your application's Gemfile:

```ruby
gem 'email_verifier'
```

And then execute:

```bash
$ bundle
```

Or install it yourself as:

```bash
$ gem install email_verifier
```

Some SMTP servers will not allow you to check if you will not present yourself as some real user. So first thing you'd need to set up is to put something like this either in initializer or in application.rb file:

```ruby
EmailVerifier.config do |config|
  config.verifier_email = "realname@realdomain.com"
end
```

Then add this to your model:

```ruby
validates_email_realness_of :email
```

Or - if you'd like to use it outside of your models:

```ruby
EmailValidator.check(youremail)
```

This method will return true or false, or - will throw exception with nicely detailed info about what's wrong.

Read More about the extension at [Email verifier RDoc](http://rubydoc.info/gems/email_verifier/0.0.4/frames) or try to sell your smartphone back here at [Mobixa.com](http://mobixa.com).


