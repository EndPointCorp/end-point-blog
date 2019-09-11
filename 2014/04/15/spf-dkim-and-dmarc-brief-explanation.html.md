---
author: Emanuele “Lele” Calò
gh_issue_number: 963
tags: email
title: SPF, DKIM and DMARC brief explanation and best practices
---

Spam mail messages have been a plague since the Internet became popular and they kept growing more and more as the number of devices and people connected grew. Despite the numerous attempts of creation of anti-spam tools, there’s still a fairly high number of unwanted messages sent every day.

Luckily it seems that lately something is changing with the adoption of three (relatively) new tools which are starting to be widely used: SPF, DKIM and DMARC. Let’s have a quick look at each of these tools and what they achieve.

### What are SPF, DKIM and DMARC

SPF (Sender Policy Framework) is a DNS text entry which shows a list of servers that should be considered allowed to send mail for a specific domain. Incidentally the fact that SPF is a DNS entry can also considered a way to enforce the fact that the list is authoritative for the domain, since the owners/administrators are the only people allowed to add/change that main domain zone.

DKIM (DomainKeys Identified Mail) should be instead considered a method to verify that the messages’ **content** are trustworthy, meaning that they weren’t changed from the moment the message left the initial mail server. This additional layer of trustability is achieved by an implementation of the standard public/private key signing process. Once again the owners of the domain add a DNS entry with the **public DKIM key** which will be used by receivers to verify that the message DKIM signature is correct, while on the sender side the server will sign the entitled mail messages with the corresponding private key.

DMARC (Domain-based Message Authentication, Reporting and Conformance) empowers SPF and DKIM by stating a clear policy which should be used about both the aforementioned tools and allows to set an address which can be used to send reports about the mail messages statistics gathered by receivers against the specific domain [1].

### How do they work?

All these tools relies heavily on DNS and luckily their functioning process, after all the setup phase is finished, is simple enough to be (roughly) explained below:

#### SPF

- upon receipt the HELO message and the sender address are fetched by the receiving mail server
- the receiving mail server runs an TXT DNS query against the claimed domain SPF entry
- the SPF entry data is then used to verify the sender server
- in case the check fails a rejection message is given to the sender server

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/04/15/spf-dkim-and-dmarc-brief-explanation/image-0-big.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/04/15/spf-dkim-and-dmarc-brief-explanation/image-0.png"/></a><br/><br/>
<span style="font-weight: lighter; size: 0.25em;">Image by Ale2006-from-en, licensed under <a href="https://creativecommons.org/licenses/by-sa/3.0/deed.en">CC BY-SA 3.0</a> from <a href="https://en.wikipedia.org/wiki/E-mail_authentication">Wikipedia</a></span></div>

#### DKIM

- when sending an outgoing message, the last server within the domain infrastructure checks against its internal settings if the domain used in the “From:” header is included in its “signing table”. If not the process stops here
- a new header, called “DKIM-Signature”, is added to the mail message by using the private part of the key on the message content
- from here on the message *main* content cannot be modified otherwise the DKIM header won’t match anymore
- upon reception the receiving server will make a TXT DNS query to retrieve the key used in the DKIM-Signature field
- the DKIM header check result can be then used when deciding if a message is fraudulent or trustworthy

<div class="separator" style="clear: both; text-align: center;"><a href="http://2.bp.blogspot.com/-eQ123eQEqB4/U0yIgEIXf_I/AAAAAAAAAS8/Kbwz5xMrP4Q/s1600/DomainKeys_Identified_Mail_(DKIM).png" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/04/15/spf-dkim-and-dmarc-brief-explanation/image-1.png"/></a><br/><br/>
<span style="font-weight: lighter; size: 0.25em;">Image by Ludovic Rembert of <a href="https://privacycanada.net">PrivacyCanada.net</a>, licensed under <a href="https://creativecommons.org/licenses/by-sa/3.0/deed.en">CC BY-SA 3.0</a>, cited in <a href="https://en.wikipedia.org/wiki/E-mail_authentication">Wikipedia</a></span></div>

#### DMARC

- upon reception the receiving mail server checks if there is any existing DMARC policy published in the domain used by the SPF and/or DKIM checks

- if *one or both* the SPF and DKIM checks succeed while still being *aligned* with the policy set by DMARC, then the check is considered successful, otherwise it’s set as failed

- if the check fails, based on the action published by the DMARC policy, different actions are taken

<div class="separator" style="clear: both; text-align: center;"><a href="/blog/2014/04/15/spf-dkim-and-dmarc-brief-explanation/image-2-big.jpeg" imageanchor="1" style="margin-left: 1em; margin-right: 1em;"><img border="0" src="/blog/2014/04/15/spf-dkim-and-dmarc-brief-explanation/image-2.jpeg"/></a><br/><br/>
<span style="font-weight: lighter; size: 0.25em;">Source <a href="https://dmarc.org/overview.html">DMARC.org</a>, licensed under <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a></span></div>

### The bad news: limits and best practices

Unfortunately even by having a perfectly functional mail system with all the above tools enforced you won’t be 100% safe from the bad guys out there. Not all servers are using all three tools shown above. It’s enough to take a look at the table shown in Wikipedia [2] to see how that’s possible.

Furthermore there are some limits that you should always consider when dealing with SPF, DKIM and DMARC:

- as already said above DKIM alone doesn’t grant in any way that the sender server is allowed to send outgoing mail for the specific domain
- SPF is powerless with messages forged in shared hosting scenario as all the mail will appear as the same coming IP
- DMARC is still in its early age and unfortunately not used as much as hoped to make a huge difference
- DMARC can (and will) break your mail flow if you don’t set up **both** SPF and DKIM **before** changing DMARC policy to anything above “none”.

Please work through the proper process carefully, otherwise your precious messages won’t be delivered to your users as potentially seen as fraudulent by a wrong SPF, DKIM or DMARC setup.

### What’s the message behind all this? Should I use these tools or not?

The short answer is: Yes. The longer answer is that everybody should and eventually will in future, but we’re just not there yet. So even if all these tools already have a lot of power, they’re not still shining as bright as they should because of poor adoption.

Hopefully things will change soon and that starts by every one of us adopting these tools as soon as possible.

-----

[1] The lack of such a monitoring tool is considered one of the reasons why other tools (such as ADSP) in past have failed during the adoption phase.

[2] [Comparison of mail servers on Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_mail_servers)
