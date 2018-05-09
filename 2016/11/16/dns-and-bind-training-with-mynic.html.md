---
author: Muhammad Najmi bin Ahmad Zabidi
gh_issue_number: 1267
tags: sysadmin
title: DNS and BIND Training with MyNIC
---



This is yet another yesteryear’s story!

I had a chance to attend a DNS/Bind training which was organized by Malaysia’s domain registry [(MyNIC)](https://www.mynic.my/en/). The training took two days and was organized in Bangi, Selangor, Malaysia. Dated November 23 to 24, 2015, the two days’ training was packed with technical training for the Domain Name System (DNS) using BIND software. Our trainer was Mr Amir Haris, who is running his own DNS specialist company named [Localhost Sendirian Berhad](http://www.localhost.my/) (Sendirian Berhad is equivalent to “Private Limited”).

## Day One

For Day One, the trainer, Mr Amir Haris taught us on the theoretical details of the DNS. For a start, Mr Amir explained to us on the DNS operation, in which he explained the basic of what DNS is and the function of root servers. Later he explained further on the root servers’ functions and locations. It was the followed by the explanation of query process.

<a href="/blog/2016/11/16/dns-and-bind-training-with-mynic/image-0-big.jpeg" imageanchor="1"><img alt="alternate text" border="0" height="height" src="/blog/2016/11/16/dns-and-bind-training-with-mynic/image-0.jpeg" style="float:right" width="width"/></a>

  

Mr Amir also explained to us the difference of DNS implementations across different operating system platforms. As for the training since we were using BIND as the name server’s software, we we exposed to the historical background of BIND.

The concept of master and slave DNS server was also being taught. In the master, the server will notify the secondary server if any change happened by the NOTIFY message. The NOTIFY message serves as a method to info the slave(s) that the zone file has changed. The NS records in the zone files are being used to determine who the slave(s) are. The benefit of NOTIFY is that it cuts down the delay for changes.

## Day Two

For the second day we were doing pretty much on the DNS practical implementation. Each of us were a given a virtual machine access in order to experience our own BIND setup.

The contents of our lab training are as follows:

- Installing BIND 9 
- Setting up RNDC 
- Setting up logging 
- Recursive and Cache DNS 
- Authoritative NS—​Master and Slave 
- Delegation 
- IPv6 
- DNS Security Extensions (DNSSEC) 
- Stealth (split) DNS 
- Hardening DNS systems 

### Recursive and Cache Nameserver

Three minimum zone files is needed which are:

- localhost (forward zone)
- localhost (reverse zone)
- root 

#### Forward zone file

```diff
;filename 127.0.0.fwd
$TTL 345600
@               IN      SOA     localhost. hostmaster.localhost. (
                                2015112401      ; Serial
                                3600            ; Refresh
                                900             ; Retry
                                3600000         ; Expire
                                3600            ; Min TTL
                                )
                IN      NS      localhost.
localhost.      IN      A 127.0.0.1
```

#### Reverse zone file

```diff
; filename 127.0.0.rev
$TTL 345600
@               IN      SOA     localhost. hostmaster.localhost.        (
                                2015112401      ; Serial
                                3600            ; Refresh
                                900             ; Retry
                                3600000         ; Expire
                                3600            ; Min TTL
                                )
                IN      NS      localhost.
1               IN      PTR     localhost.
```

We also had chance to “get our hands dirty” for domain name setup with the DNSSEC key.

At the end of the training we were given brief explanation on DNS hardening. In short they are as follows:

- Isolate DNS from other service
- Run named as non-root
- Hide BIND version
- Use logging
- Control zone transfer and queries
- Prevent DNS server from responding to DNS traffic from certain networks
- Patch BIND whenever a patch is available or when current bind version has vulnerabilities

In conclusion we were pretty much exposed to the introductory part of DNS. Honestly two days are not enough to cover all in detail but it was well done and gave a good start for attendees to initiate further self study and experimentation.

At End Point we are experienced hosting our own and clients’ DNS service using BIND (including in more exotic split-horizon setups) and nsd, and using common SaaS DNS providers such as UltraDNS, SoftLayer, Amazon Web Services Route 53, Hurricane Electric, etc.

DNS has largely become an unseen commodity service to Internet users in general, but that makes it all the more important to have skill handling DNS changes safely, and due to the occasional need for unusual configurations and coping with DDoS attacks such as the recent major attack on Dyn.


