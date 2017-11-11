---
author: Ron Phipps
gh_issue_number: 291
tags: ecommerce, interchange, open-source
title: Using charge tag in Interchange's profiles, and trickiness with logic and tag
  interpolation order
---



One of the standard ways to charging in older versions of the Interchange demo was to do the charging from a profile using the &charge command. New versions of the demo store do the charging from log_transaction once the order profiles have finished, so it is not an issue there. I've come across quite a few catalogs where the &charge command is replaced with the [charge] tag wrapped in if-then-else blocks in an order profile. It had been so long since I had used &charge so I needed to lookup how options are passed to it, which may be why people tend to use the tag version instead of the &charge command. The problem here is that Interchange tags interpolate before any of the profile specifications execute, so if you have a [charge] tag in an order profile, it executes before any of the other checks, such as validation of fields.

Here's a stripped down example of where a profile will have tags executed before the other profile checks:

```nohighlight
lname=required Last name required
fname=required First name required
&amp;fatal=yes
&amp;credit_card=standard keep

[charge route="[var MV_PAYMENT_MODE]" amount="[scratch some_total_calculation]"]

&amp;final=yes
```

In this situation even if lname, fname or the credit card number are invalid, charge will execute before all of those checks occur, calling your payment gateway with invalid parameters. This could even cause a weird state where a credit card was charged, but the order not placed because the last name check fails for example, after the charge is successful.

The way around this is either to move the credit card charging out of the order profile into log_transaction or use the &charge command like so:

```nohighlight
&amp;charge=[var MV_PAYMENT_MODE] amount=[scratch some_total_calculation]
```

Another situation where you should be careful is using if-then-else blocks, if you need to do a profile checks that are dependent upon the results of other calls in the profile then you will need to create a custom order check to do that processing, otherwise sections of your if-then-else may execute that are not intended to.


