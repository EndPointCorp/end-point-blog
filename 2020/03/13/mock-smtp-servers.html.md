---
author: "Patrick Lewis"
title: "Capturing Outgoing Email With Mock SMTP Servers"
tags: ruby, rails, email, testing
gh_issue_number: 1604
---

<img src="/blog/2020/03/13/mock-smtp-servers/banner.jpg" alt="Mailboxes" /> [Photo](https://flic.kr/p/5pw1mA) by [Seattleye](https://www.flickr.com/photos/seattleye/), used under [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), cropped from original.

Sending automated email to users is a common requirement of most web applications and can take the form of things like password reset emails or order confirmation invoices.

It is important for developers working in development/staging environments to verify that an application is sending email correctly without _actually_ delivering messages to users’ inboxes. If you were testing a background task that searches an e-commerce site for abandoned shopping carts and emails users to remind them that they have not completed a checkout, you would not want to run that in development and end up repeatedly emailing live user email addresses.

A mock SMTP server is useful for development and testing because it lets you configure the email settings of your development environment almost exactly the same as you would for outgoing SMTP email in your production site. The mock SMTP server will capture all of the outbound email and allow you to review it in a web interface instead of actually delivering it to users’ inboxes.

### Mock SMTP Servers

There are a variety of standalone/free and hosted/commercial options for mock SMTP servers including:

* [MailHog](https://github.com/mailhog/MailHog) (free)
* [MailSlurper](https://mailslurper.com) (free)
* [MailCatcher](https://mailcatcher.me) (free)
* [Mailtrap](https://mailtrap.io) (free for small solo projects/paid)
* [Mailosaur](https://mailosaur.com) (paid)

The standalone/free options have been sufficient for the projects I have worked on. Some of the features offered by the hosted solutions like Mailtrap and Mailosaur may be appealing to larger development teams.

MailHog is my go-to mock SMTP server because it has a nice web interface and is extremely easy to install and configure for typical use. The standalone solutions that I have tried all work similarly; they listen for SMTP email on one port, and provide a web interface on a separate port for reviewing captured email.

### Configuring a Rails Application to use MailHog

Installation and use of MailHog is very simple: download and run the `mailhog` executable to have it start listening for SMTP email on port 1025 and hosting a web interface on port 8025. Then edit the Rails development environment config file to send email using an SMTP server running on local port 1025:

```ruby
# config/environments/development.rb
Rails.application.configure do
# …
  config.action_mailer.delivery_method = :smtp
  config.action_mailer.perform_deliveries = true
  config.action_mailer.smtp_settings = { address: 'localhost', port: 1025 }
# …
end
```

MailHog runs in the foreground and will display output as it receives outbound email. Opening a web browser to http://localhost:8025 shows MailHog’s web interface and allows you to view a list of the email that it has captured or click on an email to show its full details:

<img src="/blog/2020/03/13/mock-smtp-servers/mailhog.png" alt="Mailhog screenshot" />

### Conclusion

 I have found MailHog to be helpful when developing a variety of different web applications, particularly ones that generate email for user notifications and confirmations. Thanks to its ease of installation and use, I would recommend it (or an equivalent mock SMTP solution) to any developer that needs to test outgoing email features in their web applications.
