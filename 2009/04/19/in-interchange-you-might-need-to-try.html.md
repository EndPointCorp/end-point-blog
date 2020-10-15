---
author: Mark Johnson
gh_issue_number: 131
tags: interchange, perl
title: In Interchange, You Might Need to [try] [goto]. What’s the [catch]?
---

Interchange provides tags that allow error trapping and handling within ITL—[try] and [catch]—that can be thought of as analogous to Perl’s `eval {}` followed by `if ($@) {}`. However, as I discovered the hard way, the analogy is not perfect.

I set up a block of ITL within [try] that had two major actions, with the 2nd depending on the success of the first. In particular, these two actions were a credit card authorization, followed by a capture of that auth as long as (a) the authorization succeeded, and (b) the merchant’s internal rules for analyzing order content compared to AVS results “passed”. (b) was necessary as a fraud-protection measure, tightening up the impact of AVS results based on the historic tendency of certain products to be targeted by crooks. In the event that the auth succeeded, but the tests from (b) failed, it is very important that the capture never be attempted because, to the gateway, the auth is entirely valid and the catpure attempt would succeed.

The code that assesses whether AVS passes is done in its own [calc]. From within the code, if the assessment does not pass, the code issues a die(), which in fact does trigger [try] to log the error that becomes accessible in [catch] via the $ERROR$ token, and thus does trigger [catch] to execute its body contents. In that way, the [try] *did* trap the error, and the error was handled in [catch], but of course that’s not the end of the story or this post wouldn’t exist.

After the code had been in production for some time, David Christensen brought to my attention that he noticed in development a test order attempt, where the order attempt failed, but both the auth and the capture succeeded. I was highly dubious of this claim and went over in great detail just what he had done. We narrowed down the condition that produced the problem to (b) above: a successful auth, but abort the order attempt anyway because a high-value product in the cart was coupled with a questionable AVS. When I went to the logs, I could see the result spelled out, but the result made no sense to my understanding:

```nohighlight
### starting credit card processing ###
Real-time full auth succeeded. ID=***
0
Real-time full capture succeeded. ID=***
Error detected for order xxx in the credit card charge.
```

The 0 indicated the [calc] had failed (died), yet the capture later in the [try] was still executing. The only conclusion was that, unlike eval {}, when [try] trapped an error, it just kept right on processing the continuing ITL. [try] always went forward and processed all its ITL to the end, and whatever happened to be the last die() called within that batch of ITL would be the thing that [catch] caught and displayed.

To resolve the problem, I introduced [goto] into the block, which stops the instance of interpolate_html() running at the point of encounter and returns. Continuing to use the die() call to populate the error code from [try], immediately after the [calc] test block I called [goto] conditionally on whether the [calc] block, in fact, died. The [goto] call then terminated the instance of interpolate_html() that [try] had invoked on its body, which had the effect of stopping ITL execution at the point of the die().

This approach to emulating `eval {}` and `if ($@) {}` has the significant flaw of developers needing to know ahead of time exactly *where* in the [try] block such failures are expected. If such is unknowable, it leaves developers in the unenviable position of having to follow each tag call with a conditional [goto] that has to know when the previous tag “failed” (i.e., triggered a die() somewhere).
