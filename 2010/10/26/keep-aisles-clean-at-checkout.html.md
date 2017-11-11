---
author: Mark Johnson
gh_issue_number: 378
tags: ecommerce, interchange, performance, tips
title: Keep the Aisles Clean at Checkout
---



It's no mystery in ecommerce that checkout processing must flow smoothly for an effective store. Providing products or services in high demand doesn't mean much if they cannot be purchased, or the purchase process is so burdensome that would-be customers give up in frustration.

Unfortunately, checkout also tends to include the most volatile elements of a web store. It virtually always involves database writes, which can be hindered by locking. It often involves real-time network access to 3rd-party providers, with payment transactions being at the top of the list. It can involve complex inventory assessments, where high concurrency can make what's normally routine highly unpredictable. Meanwhile, your customers wait, while the app sifts through complexity and waits on responses from various services. If they wait too long, you might lose sales; even worse, you might lose customers.

Even armed with the above knowledge, it's all too easy to fall into the trap of expediency. A particular action is so logically suited to be included as part of the checkout routine, and a superficial evaluation makes it seem like such a low-risk operation. That action can be tucked in there just after we've passed all the hurdles and are assured the order won't be rejected--why, it'll be so simple, and all the data we need for the action are readily at hand.

Just such expediency was at the heart of a checkout problem that had been plaguing an Interchange client of ours for months. The client would receive regular complaints that checkouts were timing out or taking so long that the customer was reloading and trying again. Many times, these customers would come to find that their orders had been placed, but that the time to complete them was exceeding the web server's timeout (or their patience). In far less common instances, but still occurring regularly, log and transaction evidence existed that showed an order attempt produced a valid payment transaction, but there was no hint of the order in their database or even in the application's system logs.

In the latter case of behavior, I had seen this before for other clients. If an action within order routing takes long enough, the Interchange server handling the request will be hammered by housekeeping. The telltale sign is the lack of log evidence for the attempt since order routes are logged at the end of the route's run; when that's interrupted, then no logging occurs.

I added considerably more explicit real-time logging and picked off some of the low-hanging fruit--code practices that had often been implicated before as the culprit in these circumstances. After collecting enough data for problematic order attempts, I was able to isolate the volatility to mail-list maintenance. The client utilizes a 3rd-party provider for managing their various mail lists, and that provider's API was contacted during order routing with all the data the provider needed for managing said lists. The data transfer for the API was very simple, and in most cases would process in sub-second time. Unfortunately, it turned out that, in enough cases, the calls to the API would take 10s to even 100s of seconds to process.

The placement of maintaining mail lists within order routing was merely convenience. The success or failure of adding to the mail lists was insignificant compared to the success or failure of the order itself. Once identified, the API calls were moved into a post-order processing routine, which was specifically built to anticipate the demonstrated volatility. As a result, complaints from customers on long or timed-out checkouts have dwindled to near zero, and the mail-list maintenance is more reliable since the background process is designed to catch excessively long process calls and retry until we receive an affirmative response from the list maintainers.

When deciding what belongs within checkout processing, ideally limit that activity to only those actions absolutely imperative to the success of the order. For each piece of functionality, ask yourself (or your client): is the outcome of this action worth adding to the wait a customer experiences placing an order? Should the outcome of this action affect whether the order attempt is successful? If the answer to those questions is "no", account for that action outside of checkout. It may be more work to do so, but keeping the checkout aisles clean, without obstruction, should be paramount.


