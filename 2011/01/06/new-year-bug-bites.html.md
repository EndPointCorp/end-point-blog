---
author: Ben Goldstein
gh_issue_number: 393
tags: analytics, ecommerce, interchange, javascript
title: New Year Bug Bites
---

Happy New Year! And what would a new year be without a new year bug bite? This year we had one where figuring out the species wasn't easy.

On January 2nd one of our ecommerce clients reported that starting with the new year a number of customers weren't able to complete their web orders because of credit card security code failures. Looking in the Interchange server error logs we indeed found a significant spike in the number of CVV2 code verification failures (Payflow Pro gateway error code "114") starting January 1st.

We hadn't made any programming or configuration changes on the system in the recent days. We double-checked to make sure: nope, no code changes. So it had to be a New Year's bug and presumably something with the Payflow Pro gateway or banks further upstream. We checked error logs for other customers to see if they were being similarly impacted, but they weren't. Our client contacted PayPal (the vendor for Payflow Pro) and they reported there were no problems with their system. The failures must indeed be card failures or a problem with the website according to them. We further checked our code looking for what we could possibly have done that might be the cause, double-checking our Git repository (which showed no recent changes) and reexamining our checkout code for possible year-based logic flaws.

Our client's top-notch customer service group got on the phone with a customer who'd gotten a security code failure and got PayPal tech support on another line. The customer service rep tried to place the customer's order on the website using the customer's credit card info and once again got the CVV2 error. She then did the credit card transaction using the swipe machine in the office, and lo and behold the order went through! What was going on??!

It turned out that despite the Payflow Pro gateway returning CVV2 verification errors what was really happening was that the year of the credit card was coming into the Payflow Pro gateway as "2012"—not as "2011" as entered into the checkout form. We knew all along that it was possible that the 114 error code responses were possibly misleading because payment gateway error codes are notorious this way. (Payment gateways blame the banks, saying they can only pass along what the banks give them. Some banks' credit card validations don't actually even care about the years being correct, but just that they not be in the past; but I digress...)

Previously we'd reviewed the checkout pages and the dropdown menus to verify that the dropdown menus weren't off, but nevertheless it very much sounded like this rather stupid problem could very well be the culprit. So we checked and checked again. What we found is that ***sometimes*** on the checkout form the year dropdown menu was mangled such that the values associated with the displayed years were YYYY+1.

The oddly intermittent behavior of the problem, the process of elimination and the all around hair pulling this loss of business was causing made somebody in the marketing group at our client realize that they are in fact still running an Omniture Test & Target A/B test on the checkout pages that they thought had been discontinued. To quote David Christensen (thanks, David!): "The Omniture system works by replacing select content for randomly chosen users in an effort to track user behavior/response to proposed site changes.  Alternate site content is created and dynamically replaced for these users as they use the site, such as the specific content on the checkout page in this instance."

We verified that the Omniture A/B test's JavaScript replacement code was alternately mangling and not mangling the year dropdown on the checkout form as mentioned. Our client took out the A/B test and the "security code errors" dropped back to a normal low level.

This was a difficult and expensive problem—not only was there business lost because of the problem, but there were a lot of resources put into troubleshooting it. We've come away from this episode with some lessons learned and with plenty of food for thought. I'll leave it to commentators to opine away on this, including the End Point folks who scratched this itch: [David Christensen](/team/david_christensen), Jeff Boes, [Mark Johnson](/team/mark_johnson), and [Jon Jensen](/team/jon_jensen).
