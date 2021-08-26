---
author: Kirk Harr
title: Raw Packet Manipulation with Scapy
github_issue_number: 1125
tags:
- python
date: 2015-04-29
---



### Installation

[Scapy](http://www.secdev.org/projects/scapy/) is a Python-based packet manipulation tool which has a number of useful features for those looking to perform raw TCP/IP requests and analysis. To get Scapy installed in your environment the best options are to either build from the distributed zip of the current version, or there are also some pre-built packages for Red Hat and Debian derived linux OS.

### Using Scapy

When getting started with Scapy, it’s useful to start to understand how all the aspects of the connection get encapsulated into the Python syntax. Here is an example of creating a simple IP request:

```python
Welcome to Scapy (2.2.0)
>>> a=IP(ttl=10)
>>> a
<IP  ttl=10 |>
>>> a.dst="10.1.0.1"
>>> a
<IP  ttl=10 dst=10.1.0.1 |>
>>> a.src
'10.1.0.2'
>>> a.ttl
10
```

In this case I created a single request which was point from one host on my network to the default gateway on the same network. Scapy will allow the capability to create any TCP/IP request in raw form. There are a huge number of possible options for Scapy that can be applied, as well as huge number of possible packet types defined. The [documentation](https://scapy.readthedocs.io/en/latest/) with these options and packet types is available on the main site for Scapy.

### Creating custom scripts with Scapy

Using Scapy within Python rather than as a standalone application would allow for creating more complex packets, sending them, and then parsing the response that is given. Here is a simple tester script example in which I will initiate a HTTP 1.1 request:

```python
#! /usr/bin/env python
import logging
logging.getLogger("scapy").setLevel(1)

from scapy.all import *

def make_test(x,y):
    request = "GET / HTTP/1.1\r\nHost: " + y  + "\r\n"
    p = IP(dst=x)/TCP()/request
    out = sr1(p)
    if out:
        out.show()
if __name__ == "__main__":
    interact(mydict=globals(), mybanner="Scapy HTTP Tester")
```

Within this script there is the make_test function which takes as parameters the destination address and host header string respectively. The script will attempt to send the HTTP GET request to that address with the proper Host header set. If the request is successful, it will print out the details of the response packet. It would also be possible to perform more complex analysis of this response packet using the built in psdump and pdfdump functions which will create a human readable analysis of the packet in PostScript and PDF respectively.

```python
Welcome to Scapy (2.2.0)
Scapy HTTP Tester
>>> make_test("www.google.com","google.com")
Begin emission:
...Finished to send 1 packets.
.*
Received 5 packets, got 1 answers, remaining 0 packets
###[ IP ]###
  version= 4L
  ihl= 5L
  tos= 0x20
  len= 56
  id= 64670
  flags=
  frag= 0L
  ttl= 42
  proto= tcp
  chksum= 0x231b
  src= 74.125.28.103
  dst= 10.1.0.2
  \options\
###[ TCP ]###
     sport= http
     dport= ftp_data
     seq= 1130043850
     ack= 1
     dataofs= 9L
     reserved= 0L
     flags= SA
     window= 42900
     chksum= 0x8c7e
     urgptr= 0
     options= [('MSS', 1430), (254, '\xf9\x89\xce\x04bm\x13\xd3)\xc8')]
>>>
```

### Conclusions

Scapy is a powerful tool, if a bit daunting in syntax initially. Creating raw TCP/IP packets systematically will probably challenge most people’s understanding of the TCP/IP stack (it certainly did mine!) but exposing this level of configuration has serious advantages. Full control of the requests and responses as well as ability to add custom Python logic allows Scapy to become a packet foundry which you can use for things like unit testing of web applications, verification of state of an unknown network, etc. I will definitely be using Scapy in the future when performing raw HTTP testing of web applications.


