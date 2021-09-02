---
author: Dan Collis-Puro
title: USPS changes the Web Tools Rate Calculator API
github_issue_number: 19
tags:
- ecommerce
- shipping
- api
date: 2007-05-14
---

End Point offers integration with online shipping APIs to provide "live lookups" of rates.

Advantages of "live lookups":

- Current rates
- Includes additional costs such as fuel surcharges
- No manual maintenance of rate tables

Disadvantages of "live lookups":

- Dependent on the availability and performance of the rate service
- Planning, programming and rolling out API changes

**CH CH CH CH CHANGES!**

Speaking of changes, the USPS has changed shipping rates as of May 14, 2007 (non-tech-friendly details [here](http://www.usps.com/ratecase/)). The changes include updates to rates, package attributes and shipping methods. These changes impact the XML-based Web Tools Rate Calculator, in some cases breaking lookups altogether. As of press time, the USPS hasn't documented the changes to the API. Broken lookups appear to be confined mostly to international shipping.

Many of the changes represent a simplification and restructuring of international shipping methods, detailed [here](http://www.usps.com/ratecase/simplified_international_rates.htm). This tweaking of international shipping methods is definitely an improvement — there were too many confusing options before. Unfortunately, these tweaks aren't backwards compatible — meaning nearly all old-style international API lookups are broken. The USPS still (as of press time) hasn't documented technical changes to the API.

**TECHIE BACKGROUND - OR "HOW THINGS GOT BROKEN"**

When you send an international rate request, the USPS API returns a "response" XML packet that includes the available shipping methods, e.g. "EXPRESS MAIL INTERNATIONAL (EMS)". Most of these shipping method names have changed in the response, leaving rate calculation code developed against the last released API in a broken state — you can't match a requested rate to a specific response.

Fortunately, the USPS has provided an undocumented staging API for customer testing, so we've been able to deduce most of the changes to the shipping method names through a battery of tests. Unfortunately, until the USPS releases new documentation we're left with an educated guess as to how to fix broken lookups.

**CONCLUSION**

The changes to international shipping methods are refreshing. However, the USPS release of an undocumented API into production for all customers has left developers guessing, especially since those changes aren't backwards-compatible.

**SELECTED TIMELINE OF API CHANGES**

- March 21, 2007. USPS notifies users that the Rate Calculator API will be changing
- April 26, 2007. USPS notifies users that they can use the staging API for testing ... on April 19.
- May 14, 2007. USPS switches to the still undocumented production API, breaking most international rate calculation lookups in the process.
