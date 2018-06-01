---
author: Steph Skardal
gh_issue_number: 591
tags: analytics, seo, testing
title: An Introduction to Google Website Optimizer
---

On End Point’s website, [Jon](/team/jon_jensen) and I recently discussed testing out use of Google Website Optimizer to run a few A/B tests on content and various website updates. I’ve worked with a couple of clients who use Google Website Optimizer, but I’ve never installed it from start to finish. Here are a few basic notes that I made during the process.

### What’s the Point?

Before I get into the technical details of the implementation, I’ll give a quick summary of why you would want to A/B test something. A basic A/B test will test user experiences of content A versus content B. The goal is to decide which of the two (content A or content B) leads to higher conversion (or higher user interactivity that indirectly leads to conversion). After testing, one would continue to use the higher converting content. An example of this in ecommerce may be product titles or descriptions.

### A/B tests in Google Website Optimizer

I jumped right into the Google Website Optimizer sign-up and wanted to set up a simple A/B test to test variations on our home page content. Unfortunately, I found right away that basic A/B tests in Google Website optimizer require two different URLs to test. In test A, the user would be see index.html, and in test B, the user would see index_alt.html. This is unfortunate because for SEO and technical reasons, I didn’t want to create an alternative index page.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="bottom"><img border="0" src="/blog/2012/04/17/google-website-optimizer-introduction/image-0.png" width="350"/></td>
<td valign="bottom"><img border="0" src="/blog/2012/04/17/google-website-optimizer-introduction/image-1.png" width="350"/>
</td>
</tr>
<tr>
<td>
<p><small>Test A: Keep existing text</small></p>
</td>
<td>
<p><small>Test B: Remove some paragraph text in first section</small></p>
</td>
</tr>
</tbody></table>

### Multivariate Testing

Rather than implement a basic A/B tests in Google Website optimizer, I decided to implement a multivariate test with just the two options (A and B). The basic setup required this:

- Copy provided JavaScript into my test page just above </head>
- Wrap <script>utmx_section("stephs_test")</script>...</noscript> around the section of text that will be modified by the test.
- Copy provided JavaScript into my converting test page just above </head>

Google Website Optimizer will verify the code and provide a user interface to enter the variations of the test text.

I used multivariate testing to test the homepage changes described above. After a couple of weeks of testing, my test results were inconclusive:

<img border="0" height="191" src="/blog/2012/04/17/google-website-optimizer-introduction/image-2.png" width="400"/><br/>
<small>Example multivariate test result in Google Website Optimizer</small>

### A Limitation with Multivariate Testing

One thing we wanted to test was a site-wide CSS change. Unfortunately, the multivariate testing in place is designed to test on page content only rather than global CSS changes. You could potentially come up with a “creative” hack and set a cookie inside the variation to specify which layout option you would use. And then the page would always look at that cookie while rendering to apply the special CSS behavior. However, this requires a bit of customization and development.
