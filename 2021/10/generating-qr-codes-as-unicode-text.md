---
author: Bharathi Ponnusamy
title: Generating TOTP QR codes as Unicode text from the command line
date: 2021-10-28
tags:
- security
- unicode
github_issue_number: 1787
---

![banner, qr code, Unicode, text, security, console, terminal, command line](/blog/2021/10/generating-qr-codes-as-unicode-text/banner.jpg)
<!-- photo by Bharathi Ponnusamy -->

(QR = “Quick Response” — good to know!)

Python’s QR code generator library [qrcode](https://pypi.org/project/qrcode/) generates QR codes from a secret key and outputs to a terminal using Unicode characters, not a PNG graphic as most other libraries do. We can store that in a text file. This is a neat thing to do, but how is this functionality useful?

##### Benefits of having Unicode QR code as a text file:

* Storing the QR code as a text file takes less disk space than a PNG image.
* It is easy to read the QR code over ssh using the `cat` command; you don't even have to download the file to your own workstation.
* It is simpler to manage QR codes in Git as text files than as PNG images.

This can be used for any kind of QR code, but we have found it especially useful for managing shared multi-factor authentication (MFA, including 2FA for 2-factor authentication) secrets for TOTPs (Time-based One-Time Passwords).

### Multi-factor authentication (MFA)

Many services provide a separate account and login for each user so that accounts do not need to be shared, and thus passwords and multi-factor authentication secrets do not need to be shared either. This is ideal, and what we insist on for our most important accounts.

Unfortunately, however, some services provide only a single login per account, or only a single primary account login with the other accounts being limited in serious ways (no access to billing, account management, etc.) so that any business relying on them needs to share the access between several authorized users. A single point of failure in an account login is a serious problem when that one person is unavailable.

### TOTP mobile apps

There are many good mobile apps for managing TOTP keys and codes, including Aegis, FreeOTP, Google Authenticator, and many others. Look for one that works with no connection to the outside world, so that you won’t be stuck when off internet & data networks.

Most applications support scanning QR codes with the phone’s camera, or else typing in a secret key to import the accounts.

For those shared accounts with no option for fully empowered individual user accounts, we can convert secret keys into QR codes for easy sharing and easy imports.

First, note that you should never use online QR code generators for MFA secrets! You risk exposing your extra authentication factors and defeating the purpose of your extra work.

### Python’s 'qrcode' library

The `qrcode` Python library provides a `qr` executable that can print your QR code using UTF-8 characters on the console.

#### Installation

```plain
apt install python3-qrcode
```

Or visit https://pypi.org/project/qrcode/

The contents of the QR code are a URL in the format:

```plain
otpauth://totp/{username}?secret={key}&issuer={provider_name}
```

The `provider_name` can contain spaces; however, they need to be URL-encoded and entered as %20 for auth to work correctly on iOS. Otherwise, an invalid barcode error will be shown when adding the code.

For example, if you generate the QR code with key `JSZE5V4676DZFCUCFW4GLPAHEFDNY447` for the account `root@example.com`, the resulting command would be:

```plain
$ qr "otpauth://totp/Example:root@example.com?secret=JSZE5V4676DZFCUCFW4GLPAHEFDNY447&issuer=Superhost" 
```

Here's what its output looks like:

![qrcode](/blog/2021/10/generating-qr-codes-as-unicode-text/qrcode.jpg)

Providing the username and issuer will display it properly in the list of configured accounts in your authenticator application. For example: `Superhost (Example:root@example.com)`


### Reference

* See a [simple explanation of otpauth URI format](http://www1.auth.iij.jp/smartkey/en/uri_v1.html) used by TOTP.
* See [RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238) for full details about TOTP.
* See [RFC 4648](https://datatracker.ietf.org/doc/html/rfc4648#section-6) for the base 32 specification used to encode the secret key.
* A recent similar Perl implementation [Terminal: QR Code with Unicode characters](https://github.polettix.it/ETOOBUSY/2021/09/26/text-qrcode-unicode/) by Flavio Poletti that builds on `Text::QRCode`, which uses `libqrencode`.
