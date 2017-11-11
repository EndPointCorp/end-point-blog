---
author: Patrick Lewis
gh_issue_number: 1176
tags: email, sysadmin
title: Taking control of your IMAP mail with IMAPFilter
---

Organizing and dealing with incoming email can be tedious, but with [IMAPFilter](https://github.com/lefcha/imapfilter)'s simple configuration syntax you can automate any action that you might want to perform on an email and focus your attention on the messages that are most important to you.

Most desktop and mobile email clients include support for rules or filters to deal with incoming mail messages but I was interested in finding a client-agnostic solution that could run in the background, processing incoming messages before they ever reached my phone, tablet or laptop. Configuring a set of rules in a desktop email client isn't as useful when you might also be checking your mail from a web interface or mobile client; either you need to leave your desktop client running 24/7 or end up with an unfiltered mailbox on your other devices.

I've configured [IMAPFilter](https://github.com/lefcha/imapfilter) to run on my home Linux server and it's doing a great job of processing my incoming mail, automatically sorting things like newsletters and automated Git commit messages into separate mailboxes and reserving my inbox for higher priority incoming mail.

IMAPFilter is available in most package managers and easily configured with a single ~/.imapfilter/config.lua file. A helpful [example config.lua](https://github.com/lefcha/imapfilter/blob/master/samples/config.lua) is available in IMAPFilter's GitHub repository and is what I used as the basis for my personal configuration.

A few of my favorite IMAPFilter rules (where 'endpoint' is configured as my work IMAP account):

```html
<span style="color: #75715e">-- Mark daily timesheet reports as read, move them into a Timesheets archive mailbox</span>
<span style="color: #f8f8f2">timesheets</span> <span style="color: #f92672">=</span> <span style="color: #f8f8f2">endpoint[</span><span style="color: #e6db74">'INBOX'</span><span style="color: #f8f8f2">]:contain_from(</span><span style="color: #e6db74">'timesheet@example.com'</span><span style="color: #f8f8f2">)</span>
<span style="color: #f8f8f2">timesheets:mark_seen()</span>
<span style="color: #f8f8f2">timesheets:move_messages(endpoint[</span><span style="color: #e6db74">'Archive/Timesheets'</span><span style="color: #f8f8f2">])</span>
```

```html
<span style="color: #75715e">-- Sort newsletters into newsletter-specific mailboxes</span>
<span style="color: #f8f8f2">jsweekly</span> <span style="color: #f92672">=</span> <span style="color: #f8f8f2">endpoint[</span><span style="color: #e6db74">'INBOX'</span><span style="color: #f8f8f2">]:contain_from(</span><span style="color: #e6db74">'jsw@peterc.org'</span><span style="color: #f8f8f2">)</span>
<span style="color: #f8f8f2">jsweekly:move_messages(endpoint[</span><span style="color: #e6db74">'Newsletters/JavaScript Weekly'</span><span style="color: #f8f8f2">])</span>

<span style="color: #f8f8f2">hn</span> <span style="color: #f92672">=</span> <span style="color: #f8f8f2">endpoint[</span><span style="color: #e6db74">'INBOX'</span><span style="color: #f8f8f2">]:contain_from(</span><span style="color: #e6db74">'kale@hackernewsletter.com'</span><span style="color: #f8f8f2">)</span>
<span style="color: #f8f8f2">hn:move_messages(endpoint[</span><span style="color: #e6db74">'Newsletters/Hacker Newsletter'</span><span style="color: #f8f8f2">])</span>
```

Note that IMAPFilter will create missing mailboxes when running 'move_messages', so you don't need to set those up ahead of time. These are basic examples but the [sample config.lua](https://github.com/lefcha/imapfilter/blob/master/samples/config.lua) is a good source of other filter ideas, including combining messages matching multiple criteria into a single result set.

In addition to these basic rules, IMAPFilter also supports more advanced configurations including the ability to perform actions on messages based on the results of passing their content through an external command. This opens up possibilities like performing your own local spam filtering by sending each message through SpamAssassin and moving messages into spam mailboxes based on the exit codes returned by spamc. As of this writing I'm still in the process of training SpamAssassin to reliably recognize spam vs. ham but hope to integrate its spam detection into my own IMAPFilter configuration soon.
