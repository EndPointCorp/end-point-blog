---
author: "Elizabeth Garrett Christensen"
title: "Ecommerce sales tax primer"
tags: ecommerce, saas, payments, magento, interchange
gh_issue_number: 1583
---

Co-authored by [Greg Hanson](/team/greg_hanson)

![Roman tax burning](/blog/2020/01/13/ecommerce-sales-tax-primer/image-0.jpg)
[Source image](https://www.flickr.com/photos/internetarchivebookimages/14591980537)

Tax collection is one of the topics *du jour* for those of us in the ecommerce industry. Since state and local authorities are now able to levy taxes on ecommerce goods, taxation for online stores has become quite complicated. The purpose of this post is to give you some next steps and ideas on implementation if you’re new to the topic and need to know how to get started on tax collection for your ecommerce business.

Current ecommerce sales tax policy stems from the 2018 U.S. Supreme Court decision South Dakota v. Wayfair, Inc. Since that decision, favoring South Dakota, 30 states have enacted legislation to require ecommerce stores to pay sales tax if they fit the definition of having an ‘economic nexus’, that is, they do enough business in the state to be worth taxing.

###Talk to your Tax Accountant

So the first and most important note is to get your own legal counsel in regards to your taxes. There are many rules and things are changing every month with local and state authorities, so you’ll need reliable counsel on the topic.

If you’re looking for someone to help, make sure this person has:

1. Knowledge about product variants. For example, clothing may not be taxed in some areas.
1. Familiarity with tax policy in the entire country, and not just one local retail area.
1. The ability to help you determine in which states you have a tax ‘nexus’ and need to pay sales tax. For many small businesses, you might only do enough business to pay sales tax in your home state and a few large ones like California or New York.

###Research Software

Luckily for anyone starting to collect sales tax, there are some very good SaaS (software as a service) systems out there to make tax collection, reporting, and compliance easy. These software systems typically integrate with your ecommerce store by providing the store with the correct tax amount for the sale and collecting information for you on your reports and filing information to get the taxes paid to the correct authorities. Some systems might even file things for you.

After you’ve worked with your tax accountant on what you need, start looking at the available software. The two main companies End Point has worked with are [TaxJar](http://taxjar.com/) and [Avalara](https://www.avalara.com/), though there are a number of other vendors in the market.

<img src="/blog/2020/01/13/ecommerce-sales-tax-primer/image-1.svg" alt="TaxJar" width="48%" style="padding-right: 2%" />
<img src="/blog/2020/01/13/ecommerce-sales-tax-primer/image-2.svg" alt="Avalara" width="48%" style="padding-left: 2%" />

####Why use an automated tax solution?
- They automatically update tax rates as they change with local and state regulation.
- They can integrate into your checkout processes via API or plugin to automatically calculate the correct tax for the right location and product.
- They can have product-specific taxes, for things that might not be taxed like food and clothing in certain states.
- They give you end-of-year reports and help with your payments.
- You can customize settings, in case there are some states where you have a ‘nexus’ (are subject to sales tax) and other places where sales tax payments are not required.

####What to look for in automated tax software:
- Choose a reputable company with large brand presence. You don’t want to do anything experimental and unreliable here.
- Pick something with documentation you can understand. You don’t want working with your tax software to be a pain, and you might need to refer to their documentation when configuring it or changing things in the future. Make sure that company speaks your language and you can easily get answers to your questions.
- This company should be able to guide you through all aspects of tax collections, filing and payment. You will legally be liable for taxes on all sales in states where you have nexus, *whether you collect the taxes or not*! So make sure the company you select can work with you not only to set up the system, but on an ongoing basis providing support in filing reports and making payments.
- Integration with your platform is a key component of what you choose. Both Avalara and TaxJar have existing plugins for sites running on WordPress, Shopify, BigCommerce, Magento, and others. Keep in mind though that the integration might be different depending on your platform. If you’re on a custom platform, talk to your development team about integrations; they can read the docs and give you an estimate and recommendation for ease of implementation (that’s where we come in for many clients). For Interchange stores, we have integration code for both TaxJar and Avilara to leverage.
- Consider how your inventory or ERP system might be affected. Many of our ecommerce clients sell in-house or over the phone. Consider how your other systems might need to tie into this new tax system.

###Implementation

So you’ve done the hard part, right? You sorted out what states you need to be compliant with and picked a software solution. Now all you need to do is get it working. This is really where your software consultant, such as us at End Point, would come in and get you to the finish line. The steps to implementation are:

1. Set up your account and pay for your tax solution software.
1. Work with the tax solution provider to set up any required bank accounts or payment channels.
1. Configure your settings.
1. Share the API key and information with your developer.
1. Test the implementation. I recommend you do this with several orders in different scenarios: products that do and don’t have sales tax, locations that do and don’t have tax, locations that tax shipping, etc. Test all the variants you know about.
1. Go live with your tax solution on your site.
1. Make sure to check back for your reports and filings for later in the year.

Need help picking a system or looking at implementation? [Call us today](/contact) and we can help.


####Other resources
- [https://www.salestaxinstitute.com/sales_tax_faqs/wayfair-economic-nexus](https://www.salestaxinstitute.com/sales_tax_faqs/wayfair-economic-nexus)
- [https://www.thebalancesmb.com/how-to-collect-report-and-pay-state-sales-taxes-399043](https://www.thebalancesmb.com/how-to-collect-report-and-pay-state-sales-taxes-399043)
- [https://www.bigcommerce.com/blog/ecommerce-sales-tax/](https://www.bigcommerce.com/blog/ecommerce-sales-tax/)
- [https://www.taxjar.com/guides/intro-to-sales-tax/](https://www.taxjar.com/guides/intro-to-sales-tax/)
