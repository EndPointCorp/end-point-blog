---
author: Selvakumar Arumugam
gh_issue_number: 1330
tags: java, tls
title: PKIX path validation failed —​ Debugging
---

I recently ran into a case working on an application with a PKIX path validation error on a site that had a valid certificate. I was able to solve the issue using OpenSSL to debug.

Typically, the PKIX path validation error arises due to SSL certificate expiry, but I ran into the same error even when the system was configured with a valid certificate. There are two web applications in our scenario, AppX and AppY. AppX uses AppY's authentication mechanism to allow the users to login with same user account. AppX sends a POST request using HttpClient with necessary arguments to SSL enabled AppY and allows the user to login based on the response.

```java
HttpClient httpclient = new DefaultHttpClient();
// ...
HttpPost httppost = new HttpPost("https://app2domain.com/sessions");

try {
    resp = httpclient.execute(httppost);
}
catch (Exception e) {
    throw new Exception("Exception: ", e);
}
```

### Error

The AppX was isolated to new server and it started throwing PKIX path validation failed error while sending requests to AppY.

```shell
Exception: javax.net.ssl.SSLHandshakeException:
sun.security.validator.ValidatorException: PKIX path validation failed:
java.security.cert.CertPathValidatorException: timestamp check failed
```
PKIX (Public-Key Infrastructure —​ X.509) is standard for key based encryption mechanism. The PKIX path related errors come up due to the failure establishing the connection with SSL applications.

### Debug

It is good to identify the root cause of the problem since there are few possible reasons for the same error. Let's start debugging...

- Check the Certificate status and expiration date in your browser
The browser reports that the certificate is valid and will expire at a future date for AppY's domain name. So now on to the detailed debugging using OpenSSL.
- OpenSSL validation
The openssl tool is a handy utility to validate the SSL certificate for any domain. It reports error with return code 20 (unable to get local issuer certificate) when checking the status of certificate — which is in contrast with browser's report on the same certificate.

```shell
$ echo -n | openssl s_client -CApath /etc/ssl/certs/ -connect app2domain.com:443
...
Start Time: 1482921042
Timeout   : 300 (sec)
Verify return code: 20 (unable to get local issuer certificate)

$ echo -n | openssl s_client -CApath /etc/ssl/certs/ -connect app2domain.com:443 </dev/null | openssl x509 -noout -dates

verify error:num=20:unable to get local issuer certificate
DONE
notBefore=May  4 00:00:00 2013 GMT
notAfter=May 14 23:59:59 2015 GMT
```

### Root Cause

The openssl tool reported certificate details another unused and expired domain. Since this is configured on the same server, it is causing the error in our case. The same scenario happened to the AppX when sending request to AppX. It may have tried to establish connection through the expired certificate. So, the lesson here is that it is necessary to clean up the expired certificates when the connection is established through HttpClient utilities. Also, a specific domain name can be validated by passing the -servername option (for SNI) to the openssl, which in this case reports appYdomain.com has valid certificate.

```shell
$ echo -n | openssl s_client -CApath /etc/ssl/certs/ -connect app2domain.com:443 -servername app2domain.com
...
Start Time: 1482920942
Timeout   : 300 (sec)
Verify return code: 0 (ok)

$ echo -n | openssl s_client -CApath /etc/ssl/certs/ -connect app2domain.com:443 -servername app2domain.com </dev/null | openssl x509 -noout -dates
...
verify return:0
DONE
notBefore=Sep 26 11:52:51 2015 GMT
notAfter=Apr  1 12:35:52 2018 GMT
```

### Conclusion

In most cases, the PKIX path validation error comes up when the SSL certificate is expired for the domain name, however, there may be different reasons such as certificate expiry, picking wrong certificate, etc. It is always helpful to debug with the openssl tool to identify the root cause. This specific issue was fixed by removing the unused expired certificate.
