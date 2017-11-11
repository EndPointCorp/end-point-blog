---
author: David Christensen
gh_issue_number: 949
tags: interchange
title: Significant Whitespace in an Interchange UserTag
---

Here's a quick issue I ran into with an Interchange UserTag definition; I'd made some changes to a custom UserTag, but upon restarting the Interchange daemon, I ended up with a message like the following:

UserTag 'foo_user_tag' code is not a subroutine reference

This was odd, as I'd verified via perl -cw that the code in the UserTag itself was valid.  After hunting through the changes, I noticed that the UserTag definition file was itself in DOS line-ending mode, but the changes I'd made were in normal Unix line-ending mode.  This was apparently sufficient reason to confuse the UserTag parser.

Sure enough, changing all line endings in the file to match resulted in the successful use of the UserTag.  For what it's worth, it did not matter whether the line endings in the file were Unix or DOS, so long as it was consistent within the file itself.


