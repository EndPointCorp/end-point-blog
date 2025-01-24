---
author: Brian Buchalter
title: Using Gmail at Work
github_issue_number: 525
tags:
- email
- mobile
date: 2011-12-15
---

### The Short Story

For those who don’t care about why, just how...

1. Create a [new Gmail account](https://accounts.google.com/NewAccount?service=mail&continue=http://mail.google.com/mail/e-11-63fb73ea731526b75ac5a66a770b0-ee45c8c140b7a1c66d569e7562acee65c08f1c21&type=2)
1. Setup [Mail Fetcher](https://support.google.com/mail/bin/answer.py?hl=en&answer=21289)
1. Setup [send email from another account](https://support.google.com/mail/bin/answer.py?hl=en&answer=22370);and make it your default
1. Verify you send and receive as your corporate address by default using the web client
1. [Setup your mobile](https://www.google.com/gmail/about/)
1. From your mobile go to [m.google.com/sync](https://m.google.com/sync) and Enable “Send Mail As” for this device (tested only on iOS)
1. Verify you send and receive as your corporate address by default using your mobile client
1. Setup Google Authorship with your domain’s email address

### The Long Story

Here at End Point there are a lot of opinions about email clients. Our hardcore folks like [Alpine](https://en.wikipedia.org/wiki/Alpine_(email_client)) while for most people Evolution, Thunderbird, or Outlook will do. As a Gmail user since September 2004, I found I needed to figure out how get our corporate email system to work with my preferred client.

My first reaction was to have Gmail act as an IMAP client. I found ([as many others had](https://productforums.google.com/forum/?hl=en#!category-topic/gmail/managing-settings-and-mail/b0v5HHlqbHs)) that Gmail does not support IMAP integration with other accounts. However, Gmail does have a POP email client known as [Mail Fetcher](https://support.google.com/mail/answer/21289?hl=en). I found that Gmail does support encrypted connections via POP, so use them if your email server supports them. When combined with the [HTTPS by default](https://gmail.googleblog.com/2010/01/default-https-access-for-gmail.html), access to the Gmail web client seemed sufficiently secure.

I now needed to send email not as my Gmail address, but as my End Point address. Google has well documented how to [send email from another account](https://support.google.com/mail/bin/answer.py?hl=en&answer=22370). Again encrypted SMTP is supported and is strongly recommended. Also be sure to make your corporate email account the default account so you will always use your corporate email address and not the Gmail address.

After verifying I was sending and receiving email properly, I needed to get my mobile setup. There are a [variety of options](https://www.google.com/gmail/about/) available for all the mobile platforms. On my iPhone, I had several other accounts already setup and found the native client to be acceptable. I decided I would configure the native iPhone email app to access Gmail, as well as Contacts and Calendar using Google’s support for Microsoft’s ActiveSync protocol, which Google has licensed and rebranded as [Google Sync](https://support.google.com/a/users/answer/138740?visit_id=1-636676970400046677-2511485164&hl=en&rd=1).

I had used Google Sync for other Exchange accounts at my previous job and found it worked very well. However, there are some [known issues](https://support.google.com/a/users/answer/139635?visit_id=1-636676970400046677-2511485164&hl=en&rd=1), like not being able to accept event invitations recieved via POP. It’s worth checking these issues out to see if there are any blockers for you.

After setting up “Google Sync” on my iPhone, I tested again, and found that by default, it would use my Gmail account as my default outgoing email account, despite the setting in the Gmail web client. I needed to use my corporate address here at End Point for sending mail from mobile; I thought I was sunk!

Fortunately, it seems I over looked a section in the Google Sync setup documentation, labeled “Enable Send Mail As feature”. This feature solved my problem by having me go to [m.google.com/sync](https://get.google.com/apptips/apps/?utm_source=googlemobile&utm_campaign=redirect#!/all) from my iOS device and check Enable “Send Mail As” for this device. This would tell Google Sync to use the default outgoing account I had specified in the web client.

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2011/12/using-gmail-at-work/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2011/12/using-gmail-at-work/image-0.png"/></a></div>

<div class="separator" style="clear: both; text-align: center;"></div>

One requirement here at End Point which this configuration does not meet is support for PGP encryption/decryption of messages. There is a [Chrome plugin](https://web.archive.org/web/20111203170252/http://gpg4browsers.recurity.com/) that claims to offer support, but as the authors from [this post](http://www.theregister.co.uk/2011/11/23/browser_crypto_plugin_debuts/) highlight:

*There may also be resistance from crypto users – who already are a security-conscious lot – to trusting private keys and confidential messages to a set of PGP functions folded inside some JavaScript running inside a browser. *

I’d have to say I agree. After following the instructions to install the plugin, I balked when it asked for my private key; I just didn’t feel comfortable. Despite this shortfall, most End Point email isn’t encrypted end-to-end. However, I can feel good knowing that my “last mile” connection to End Point’s servers are encrypted, end-to-end using encrypted POP, SMTP, and HTTPS.
