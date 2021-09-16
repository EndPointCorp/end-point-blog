---
author: Greg Sabino Mullane
title: Tail_n_Mail does Windows (log file monitoring)
github_issue_number: 301
tags:
- database
- monitoring
- postgres
date: 2010-05-09
---

I’ve just released version 1.10.1 of [tail_n_mail.pl](https://bucardo.org/tail_n_mail), the handy script for watching over your Postgres logs and sending email when interesting things happen.

Much of the recent work on tail_n_mail has been in improving the parsing of statements in order to normalize them and give reports like this:

```nohighlight
[1] From files A to Q Count: 839
First: [A] 2010-05-08T05:10:46-05:00 alpha postgres[13567]
Last:  [Q] 2010-05-09T05:02:27-05:00 bravo postgres[19334]
ERROR: duplicate key violates unique constraint "unique_email_address"
STATEMENT: INSERT INTO email_table (id, email, request, token) VALUES (?)

[2] From files C to E (between lines 12523 of A and 268431 of B, occurs 6159 times)
First: [C] 2010-05-04 16:32:23 UTC [22504]
Last:  [E] 2010-05-05 05:04:53 UTC [23907]
ERROR: invalid byte sequence for encoding "UTF8": 0x????
HINT: This error can also happen if the byte sequence does not
match the encoding expected by the server, which is controlled
by "client_encoding".

## The above examples are from two separate instances, the first
## of which has the "find_line_number" option turned off
```

However, I’ve only ever used tail_n_mail on Linux-like systems, so it will not work on Windows systems...until now. Thanks to an error report and patch from Paulo Saudin, this program will now work on Windows. There is an new option, **mailmode**, which defaults to ‘sendmail’, for the same behavior as previous versions of tail_n_mail. This assumes you have access to a **sendmail** binary (which may or may not be from the actual Sendmail program: many mail programs provide a compatible binary of the same name). If you don’t have sendmail, you can now specify an argument of ‘smtp’ to the mailmode argument (you can also simply use **--smtp**). This switches to using the [Net::SMTP::SSL module](https://metacpan.org/pod/release/CWEST/Net-SMTP-SSL-1.01/lib/Net/SMTP/SSL.pm) to send the mail instead of sendmail.

Switching the mailmode is not enough, of course, so there are some additional flags to help the mail go out:

- **--mailserver** : the name of the outgoing SMTP server- **--mailuser** : the user to authenticate with- **--mailpass** : the password of the user- **--mailport** : the port to use: defaults to 465

Needless to say, using the --mailpass option from the command line or even in a script is not the best practice, so it is highly recommended that you put the new variables inside a **tailnmailrc** file. When the script starts, it looks for a file named **.tailnmailrc** in the current directory. If that is not found, it looks for the same file in your home directory (or technically, whatever the **HOME** environment variable is set to). If that does not exist, it checks for the file **/etc/tailnmailrc**. You can override those checks by specifying the file directly with the **--tailnmailrc=** option, or disable all rc files with the **--no-tailnmailrc** option.

The tailnmailrc file is very straightforward: each line is a name and value pair, separated by a colon or an equal sign. Lines starting with a ‘#’ indicate a comment and are skipped. So someone using the new Net::SMTP::SSL method might have a .tailnmailrc in their home directory that looks like this:

```nohighlight
mailmode=smtp
mailserver=mail.example.com
mailuser=greg@example.com
mailpass=mysupersekretpassword
```

The tail_n_mail program is open source and BSD licensed. Contributions are always welcome: send a patch, fork a version, or submit bug reports and feature requests through [the Github repository](https://github.com/bucardo/tail_n_mail).
