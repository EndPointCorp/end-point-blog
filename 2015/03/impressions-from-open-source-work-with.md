---
author: Kamil Ciemniewski
title: Impressions from Open Source work with Elixir
github_issue_number: 1108
tags:
- elixir
- erlang
- functional-programming
- open-source
date: 2015-03-26
---

Some time ago I started working on the Elixir library that would allow me to send emails as easily as ActionMailer known from the Ruby world does.

The beginnings were exciting—​I got to play with a **very** clean and elegant new language which Elixir is. I also quickly learned about the openness of the Elixir community. After hacking some first draft-like version and posting it on GitHub and Google groups—​I got a **very** warm and thorough code review from the **language’s author** José Valim! That’s just impressive and it made me even more motivated to help out the community by getting my early code into a better shape.

Coding the ActionMailer like library in a language that was born 3 years ago doesn’t sound like a few hours job—​there’s lots of functionality to be covered. An email’s body has to be somehow compiled from the template but also the email message has to be transformed to the form in which the SMTP server can digest and relay it. It’s also great if the message’s body can be encoded with „quoted printable”—​this makes even the oldest SMTP server happy. But there’s lots more: connecting with external SMTP servers, using the local in-Elixir implementation, ability to test etc… 

Fortunately Elixir’s built on top of the Erlang’s „Virtual Machine”—​BEAM—​which makes you able to use its libraries—​a lot of them. For the huge part of the functionality I needed to cover I chose the great [gen_smtp library](https://github.com/Vagabond/gen_smtp). This allowed me to actually send emails to SMTP servers and have them properly encoded. With the focus on developer’s productivity, Elixir made me come up with the nice set of other features that you can check out [here](https://github.com/kamilc/mailman).

This serves as a shout out blog post for the Elixir ecosystem and community. The friendliness that it radiates with makes open source work like this very rewarding. I invite you to make your contributions as well—​you’ll like it.
