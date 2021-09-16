---
author: Steph Skardal
title: Post Login Action in Interchange
github_issue_number: 883
tags:
- ecommerce
- interchange
- perl
date: 2013-11-14
---

A while back, I sent a request to a few coworkers looking for a post login hook in Interchange, meaning that I’d like to execute some code after a user logs in that would not require modifying the core Interchange code. This was prompted by the need to transfer and create database records of uploaded images (uploaded while not logged in) to be tied to a specific user after they log in. [Mark](/team/mark-johnson) found a simple and elegant solution and I’ve described it below.

### postlogin_action

The first step to adding a post login hook or method is to add the following to catalog.cfg:

```perl
UserDB  default  postlogin_action  transfer_user_images
```

The above code results in a call to the catalog or global sub *transfer_user_images* after a user logs in.

### Defining the Global Sub

Next, the sub needs to be defined. In our code, this looks like:

```perl
# custom/GlobalSub/transfer_user_images.sub
GlobalSub transfer_user_images IC::GlobalSubs::transfer_user_images
```

```perl
# custom/lib/IC/GlobalSubs.pm
sub transfer_user_images {
  #code here
}
```

In the above example a transfer_user_images sub points to a Perl module that contains all of our custom global subroutines. The GlobalSubs Perl module contains the code executed upon login.

### Add code!

After the simple steps above, code can be added inside the GlobalSub transfer_user_images subroutine. For this particular method, the simplified pseudocode looks something like:

```perl
sub transfer_user_images {
  # Create database connection
  # Foreach image stored in the session
  #   Move image to user specific location
  #   Record image to database, tied to user
  # Delete session images variable
}
```
