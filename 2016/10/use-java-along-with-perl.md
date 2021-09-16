---
author: Szymon Lipiński
title: Use Java along with Perl
github_issue_number: 1263
tags:
- java
- perl
date: 2016-10-18
---

While working with one of our clients, I was tasked with integrating a Java project with a Perl project. The Perl project is a web application which has a specific URL for the Java application to use. To ensure that the URL is called only from the Java application, I wanted to send a special hash value calculated using the request parameters, a timestamp, and a secret value.

The Perl code calculating the hash value looks like this:

```perl
use strict;
use warnings;

use LWP::UserAgent;
use Digest::HMAC_SHA1;
use Data::Dumper;

my $uri = 'param1/param2/params3';

my $ua = LWP::UserAgent->new;
my $hmac = Digest::HMAC_SHA1->new('secret_something');

my $ts = time;

$hmac->add($_) for (split (m{/}, $uri));
$hmac->add($ts);

my $calculated_hash = $hmac->hexdigest;
```

My first try for calculating the same hash in the Java code looked something like this (without class/package overhead):

```java
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import org.apache.commons.codec.binary.Hex;

public String calculateHash(String[] values) throws NoSuchAlgorithmException, UnsupportedEncodingException, InvalidKeyException {

    java.util.Date date= new java.util.Date();
    Integer timestamp = (int) date.getTime()/1000;

    Mac mac = Mac.getInstance("HmacSHA1");

    SecretKeySpec signingKey = new SecretKeySpec("secret_something".getBytes(), "HmacSHA1");
    mac.init(signingKey);

    for(String value: values) {
        mac.update(value.getBytes());
    }

    mac.update(timestamp.getBytes());
    byte[] rawHmac = mac.doFinal();
    byte[] hexBytes = new Hex().encode(rawHmac);
    return new String(hexBytes, "UTF-8");
}
```

The code looks good and successfully calculated a hash. However, using the same parameters for the Perl and Java code, they were returning different results. After some debugging, I found that the only parameter causing problems was the timestamp. My first guess was that the problem was caused by the use of Integer as the timestamp type instead of some other numeric type. I tried a few things to get around that, but none of them worked.

Another idea was to check why it works for the String params, but not for Integer. I found that Perl treats the timestamp as a string and passes a string to the hash calculating method, so I tried emulating this by converting the timestamp into a String before using the getBytes() method:

```java
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import org.apache.commons.codec.binary.Hex;

public String calculateHash(String[] values) throws NoSuchAlgorithmException, UnsupportedEncodingException, InvalidKeyException {

    java.util.Date date= new java.util.Date();
    Integer timestamp = (int) date.getTime()/1000;

    Mac mac = Mac.getInstance("HmacSHA1");

    SecretKeySpec signingKey = new SecretKeySpec("secret_something".getBytes(), "HmacSHA1");
    mac.init(signingKey);

    for(String value: values) {
        mac.update(value.getBytes());
    }

    mac.update(timestamp.toString().getBytes());
    byte[] rawHmac = mac.doFinal();
    byte[] hexBytes = new Hex().encode(rawHmac);
    return new String(hexBytes, "UTF-8");
}
```

This worked perfectly, and there were no other problems with calculating the hash in Perl and Java.
