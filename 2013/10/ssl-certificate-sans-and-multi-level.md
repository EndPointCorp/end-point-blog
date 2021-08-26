---
author: Cas Rusnov
title: SSL Certificate SANs and Multi-level Wildcards
github_issue_number: 869
tags:
- security
- tls
- sysadmin
date: 2013-10-29
---

Some bits of advice for those that run their own Certificate Authorities or use self-signed certificates, related to multiple matches and wildcard domains.

In some circumstances it’s desirable to match multiple levels of wildcards in an SSL certificate. One example of this is in our Camp development system (whose domain names are in the format *n*.camp.foo.com, where *n* is a numeric identifier of the camp), where having a certificate which matches something like fr.0.camp.foo.com and also en.91.camp.foo.com would be needed.

The most obvious way to do this is to create a certificate whose commonName is *.*.camp.foo.com; unfortunately this is also not a working solution, as it is unsupported with current-day browsers. The alternative is to create a *subjectAltName* (which is an alias within the certificate for the subject of the certificate, abbreviated *SAN*) for each subdomain which we want to wildcard. For Camps this works well because the subdomains are in an extremely regular format so we can create a SAN for each [0..99].camp.foo.com. One caveat is that if SANs are in use they must also contain the commonName (CN) as an alternate name, since the browser will ignore the CN in that case (in this example, a SAN for *.camp.foo.com and camp.foo.com would be added).

SANs are added to the certificate when the certificate signing request is created. Assuming that the key for the certificate has already been generated as camp.foo.com.key, the first step is to make a copy ofthe system’s openssl.cnf file, naming it something like foo.com.openssl.cnf. Next this file is edited to add the SANs.

First uncomment the line which says:

```nohighlight
req_extensions = v3_req
```

Next in the [v3_req] section, add the SANs. There are two ways to do this, either inline or as a separate section. Inline is in the format:

```nohighlight
subjectAltName=DNS:*.0.camp.foo.com,DNS:*.1.camp.foo.com [...]
```

Sectional is in the format:

```nohighlight
subjectAltName=@alt_names
```

And then a section [alt_names] is created later in the file:

```nohighlight
[alt_names]
DNS.1=*.0.camp.foo.com
DNS.2=*.1.camp.foo.com
[...]
```

Note that in the *DNS.n* lines, the n enumerates the entry number starting at 1.

The sectional format seems more convenient for programmatic generation of the cnf file, since a simple template could be made that is merely appended to.

Once the cnf file is created, the CSR is generated in the normal way, with the new cnf file specified:

```nohighlight
openssl req -new -out camp.foo.com.csr -key camp.foo.com.key -config foo.com.openssl.cnf
```

This creates the CSR file, which can then be signed by the CA or the camp.foo.com key in the normal way, with one important point: the cnf file used by the CA must have the following line uncommented:

```nohighlight
copy_extensions = copy
```

This line ensures that the v3 extension sections for subjectAltNames are copied from the CSR into the newly minted certificate. The reason that this is commented out by default is that it introduces a security risk if used against CSRs that aren’t strictly controlled since some extensions may cause the CSRs to produce certificate signing certificates.

The resultant certificate will contain the subjectAltNames specified, and can be verified by looking at the contents of the certificate with:

```nohighlight
openssl x509 -in camp.foo.com.crt -text -noout
```

There will be a lot of output, but will contain something like:

```nohighlight
X509v3 Subject Alternative Name:
     DNS:*.0.camp.foo.com, DNS:*.1.camp.foo.com, DNS:*.2.camp.foo.com [...]
```

When you see this, you’ll know everything worked. I hope this summary will help anyone who has this need, and here’s to the day when browsers support multiple-level wildcard certificates and this advice is moot.
