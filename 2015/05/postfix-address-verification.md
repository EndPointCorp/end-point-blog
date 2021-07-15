---
author: Marco Matarazzo
title: Postfix Address Verification
github_issue_number: 1129
tags:
- email
- sysadmin
date: 2015-05-28
---



We recently upgraded some mail servers, moving from Exim to Postfix in the process. These server works as a front line spam/RBL filter, rejecting invalid message and relaying valid ones to different SMTP based on the destination domain.

While looking for the best configuration layout to achieve this, we found that Postfix has a very useful and interesting feature: Address Verification. This technique allows the Postfix server to check that a sender or a recipient address is valid before accepting a message, preventing junk messages from entering the queue.

### How does Address Verification work?

Upon receiving a message Postfix will probe the preferred MTA for the address. If that address is valid the message is accepted and processed, otherwise it is rejected.

Message Probes does not actually go through the whole delivery process; Postfix will just connect to the MTA, send a HELO + MAIL FROM + RCPT TO sequence and check its response. Probe checks results are cached on disk, minimizing network and resource impact. During this check the client is put “on hold”; if the probe takes too much a temporary reject is given; a legitimate mail server will have no problem retrying the delivery later, when the cached result will likely be available.

Everything is highly configurable: response codes, timeouts, cache storage type and location, and so on.

### Configure Recipient Address Verification

In our case, we wanted to only accept messages with a valid recipient address. Recipient Address Verification took care of this in a very smooth and elegant way.

Adding Recipient Address Verification it’s easy. Just add these lines to /etc/postfix/main.cf:

```nohighlight
# Your relaying configuration will already be in place. For example:
# relayhost = [next.hop.ip.address]

smtpd_recipient_restrictions = 
    permit_mynetworks
    reject_unauth_destination
    reject_unknown_recipient_domain
    reject_unverified_recipient

# Custom reply message when probe fails (Postfix 2.6 and later)
unverified_recipient_reject_reason = Address lookup failure
```

Settings order is important as they are verified one after another; when a decision is triggered (PERMIT or REJECT) the parsing process ends.

Let’s see them in details:

- **permit_mynetworks**: *permit* message from local or trusted addresses listed in $mynetworks;
- **reject_unauth_destination**: *reject* message unless recipient domain is a local one (typically in $mydestination, $virtual_alias_domains or $virtual_mailbox_domains) or is accepted for forwarding (in $relay_domains);
- **reject_unknown_recipient_domain**: *reject* message if recipient domain has no DNS MX and A record, or has a malformed MX record;
- **reject_unverified_recipient**: *reject* the message if the Recipient Address Verification fails.

If you want to learn more, the best place to find more information is the [Postfix Address Verification Howto](http://www.postfix.org/ADDRESS_VERIFICATION_README.html).


