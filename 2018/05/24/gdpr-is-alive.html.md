---
author: Jon Jensen
title: "GDPR is alive!"
tags: compliance, privacy
gh_issue_number: 1425
---

<img src="/blog/2018/05/24/gdpr-is-alive/5740833496_9c8776282e_o-crop.jpg" width="770" height="354" alt="two men talking in a crowd at night"><br><a href="https://www.flickr.com/photos/julioalbarran/5740833496/">Photo by Julio Albarrán, CC BY-SA 2.0, cropped</a>

The European Union's General Data Protection Regulation (GDPR) that became law a little over two years ago, is now implemented as of 25 May 2018.

### Another GDPR article?

Over the past few weeks most of us have been receiving lots of GDPR-related email from companies sending us new privacy policies, so most people have heard at least something about GDPR. But we are finding that some still do not know the impact on their business, and they wonder if it has anything to do with them if they are outside the EU. This article is our attempt to help set those people on the path to finding answers.

I think the first thing to recognize is that the GDPR is a general *business* matter, not primarily a *technical* matter. The regulation focuses on business processes and information management (whether computerized or not), and law; it is not actually about software or legal verbiage on websites.

The GDPR is not the kind of law that can be complied with simply by adding a few features to software, changing a few configuration options, or updating a legal notice and moving on with no changes to actual practice.

Some people outside the EU wonder how it is possible that this regulation can affect them. Consider as an example that United States income tax law affects US citizens anywhere in the world, US banking rules affect banks in most parts of the world, and US sanctions affect people and businesses anywhere the world. The EU has a long reach as well.

As always, you may want to discuss questions about all this with a competent lawyer for clarification, to go into specifics about your business situation and get tailored advice.

### Who does the GDPR apply to?

The GDPR applies if (citing an EU guidance document):

* your company processes personal data and is based in the EU, regardless of where the actual data processing takes place; or 
* your company is established outside the EU but offers goods or services to, or monitors the behavior of, individuals within the EU.

This concept of personal data is similar to “personal identifying information” (PII) in the Payment Card Industry Data Security Standard (PCI DSS) and Protected Health Information (PHI) in the US Health Insurance Portability and Accountability Act (HIPAA), and includes such things as:

* names
* Social Security or other identifying numbers
* account and license numbers
* physical, mailing, and email addresses
* phone numbers
* location
* health records
* income and banking information
* IP addresses
* photographs, audio, and video

Past practices to “pseudonymize” such data have often fallen short and made it easy to de-anonymize the data. For example, HIPAA considers a ZIP code to be PHI, even if all obvious personal data is detached from it. Only an entire US state is large enough to be considered depersonalized, or the first 3 digits of a ZIP code if the data set meets certain criteria. The same goes for dates: anything more granular than a year cannot be considered anonymous. That is HIPAA, not GDPR, but illustrates that our intuition about anonymity is often wrong when many data points can be used to de-anonymize someone.

### What do businesses need to do?

Other people have recently written excellent, accessible summaries, so I will point to a few good ones I have seen.

#### “Understand the GDPR in 10 minutes”

A fine place to start is Adam Geitgey’s [Understand the GDPR in 10 minutes or, “Just tell me what I have to do, man.”](https://medium.com/@ageitgey/understand-the-gdpr-in-10-minutes-407f4b54111f)

#### “GDPR Hysteria”

Next, Jacques Mattheij has written an excellent two-part series on his blog “Technology, Coding and Business”. Here is an abbreviated action list that illustrates how simple he has made it:

**Things you can no longer do:**

* store all the data you can get your hands on forever
* ignore requests for deletion, correction, or insight from your users
* wipe breaches under the carpet and pretend they did not happen
* pretend the data on your systems is yours rather than the end-users’
* treat data security like it is optional
* sell end user data with abandon
* fail to obtain consent

**Things you will have to do:**

* enable data life-cycle management
* figure out what data you have that is in scope for the GDPR
* ensure your systems are secure
* disclose all uses of the data you collect in your privacy policy
* enter into DPAs (data processing agreements) with all those that you farm out data processing to
* disclose those companies that you have DPAs with
* obtain consent from your users for the use of their data
* plan for the withdrawal of consent
* report breaches immediately if they cross the reporting threshold

**Selected recommendations:**

* delete data that you no longer use
* do annual penetration tests / audits
* cut down on the number of parties that you ship your users data to
* apply GDPR principles globally to make your work easier (as [Microsoft is doing](https://blogs.microsoft.com/on-the-issues/2018/05/21/microsofts-commitment-to-gdpr-privacy-and-putting-customers-in-control-of-their-own-data/))

They are good articles and I recommend reading them yourself:

* [GDPR Hysteria](https://jacquesmattheij.com/gdpr-hysteria)
* [GDPR Hysteria Part II, Nuts and Bolts, actionable advice](https://jacquesmattheij.com/gdpr-hysteria-part-ii-nuts-and-bolts)

#### “Preparing for the GDPR”

[The SSL Store series “Preparing for the GDPR”](https://www.thesslstore.com/blog/preparing-gdpr-introduction-1/) includes these articles:

* How it affects the Domain Industry
* How it affects Web Hosts
* Problems for ICANN/WHOIS?
* Complying with EU-US Privacy Shield
* What is a Data Protection Officer?
* Best Practices for Privacy Notices
* What you need to know about Cookies
* What is the Right to be Forgotten?
* How to perform a Data Audit
* Encryption Best Practices

#### “No one’s ready for GDPR”

An article in The Verge gives another summary point of view: [No one’s ready for GDPR: ‘Very few companies are going to be 100 percent compliant on May 25th’](https://www.theverge.com/2018/5/22/17378688/gdpr-general-data-protection-regulation-eu).

### Other resources

As is often the case, Wikipedia has helpfully distilled things down in their article [General Data Protection Regulation](https://en.wikipedia.org/wiki/General_Data_Protection_Regulation).

The [Microsoft Trust Center resources on the GDPR](https://www.microsoft.com/en-us/TrustCenter/Privacy/gdpr/default.aspx) is good too.

And of course, look to the source, the European Union itself. They provide variety of documents giving illustrated guidance, as well as the complete law:

* [2018 reform of EU data protection rules](https://ec.europa.eu/commission/priorities/justice-and-fundamental-rights/data-protection/2018-reform-eu-data-protection-rules_en)
* [Data protection: Rules for the protection of personal data inside and outside the EU](https://ec.europa.eu/info/law/law-topic/data-protection_en)

Everyone is responsible for their own compliance with the regulation, but we are happy to help our clients adapt their systems and implement technical accommodations they determine are needed.

If you have not yet begun, it is not too late — the EU goal clearly seems to be getting everyone to improve handling of others’ personal data, not to panic or fixate on enforcement fears.
