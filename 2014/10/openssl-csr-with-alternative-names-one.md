---
author: Emanuele “Lele” Calò
title: OpenSSL CSR with Alternative Names one-line
github_issue_number: 1048
tags:
- security
- sysadmin
- tls
date: 2014-10-30
---

2017-02-16—​Edit—​I changed this post to use a different method than what I used in the original version cause X509v3 extensions were not created or seen correctly by many certificate providers.

I find it hard to remember a period in my whole life in which I issued, reissued, renewed and revoked so many certificates.

And while that’s usually fun and interesting, there’s one thing I often needed and never figured out, till a few days ago, which is how to generate CSRs (Certificate Signing Requests) with AlternativeNames (eg: including www and non-www domain in the same cert) with a one-liner command.

This need is due to the fact that some certificate providers (like GeoTrust) don’t cover the parent domain when requesting a new certificate (eg: CSR for www&#x2e;endpoint.com won’t cover endpoint.com), unless you specifically request so.

Luckily that’s not the case with other Certificate products (like RapidSSL) which already offer this feature built-in.

This scenario is starting to be problematic more often since we’re seeing a growing number of customers supporting sites with HTTPs connections covering both www and “non-www” subdomains for their site.

Luckily the solution is pretty simple and straight-forward and the only requirement is that you should type the CSR subject on the command line directly, basically without the use of the interactive question mechanism.

If you managed to understand how an SSL certificate works this shouldn’t be a huge problem, anyway just as a recap here’s the list of the meaning for the common Subject entries you’ll need:

- `C` — Country
- `ST` — State
- `L` — City
- `O` — Organization
- `OU` — Organization Unit
- `CN` — Common Name (eg: the main domain the certificate should cover)
- `emailAddress` — main administrative point of contact for the certificate

So by using the common syntax for OpenSSL subject written via command line you need to specify all of the above (the OU is optional) and add another section called **subjectAltName=**.

By adding **DNS.n** (where *n* is a sequential number) entries under the “subjectAltName” field you’ll be able to add as many additional “alternate names” as you want, even not related to the main domain.

Obviously the first-level parent domain will be covered by most SSL products, unless specified differently.

So here’s an example to generate a CSR which will cover *.your-new-domain.com and your-new-domain.com, all in one command:

```bash
openssl req -new -sha256 -nodes -out \*.your-new-domain.com.csr -newkey rsa:2048 -keyout \*.your-new-domain.com.key -config <(
cat <<-EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
C=US
ST=New York
L=Rochester
O=End Point
OU=Testing Domain
emailAddress=your-administrative-address@your-awesome-existing-domain.com
CN = www.your-new-domain.com

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = your-new-domain.com
DNS.2 = www.your-new-domain.com
EOF
)
```

To be honest, that’s a sub-optimal solution for a few reasons but mostly that it’s not comfortable to fix in case you did a typo or similar.

That’s why I prefer creating a dedicated file (that you can also reuse in future) and then pipe that in openssl.

Of course you can use your text editor of choice, I used HEREDOC mostly because it shows better through blog posts in my opinion.

```bash
cat > csr_details.txt <<-EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
C=US
ST=New York
L=Rochester
O=End Point
OU=Testing Domain
emailAddress=your-administrative-address@your-awesome-existing-domain.com
CN = www.your-new-domain.com

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = your-new-domain.com
DNS.2 = www.your-new-domain.com
EOF

# Let’s call openssl now by piping the newly created file in
openssl req -new -sha256 -nodes -out \*.your-new-domain.com.csr -newkey rsa:2048 -keyout \*.your-new-domain.com.key -config <( cat csr_details.txt )
```

Now with that I’m able to generate proper multi-domain CSRs effectively.

Please note the use of the **-sha256** option to enable SHA256 signing instead of the old (and now definitely deprecated SHA1).

Thanks to all our readers for all the hints, ideas and suggestiong they gave me to improve this post, which apparently is still very useful to a lot of System Administrators out there.
