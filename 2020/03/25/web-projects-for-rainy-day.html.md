---
author: "Elizabeth Garrett Christensen"
title: "Web Projects for a Rainy Day"
tags: optimization, development, seo, reporting, testing
gh_issue_number: 1609
---

![raindrops on a plant](/blog/posts/2020/03/25/web-projects-for-rainy-day/image-0.jpg)

[Image](https://www.flickr.com/photos/yellowstonenps/32984582893/) by [Yellowstone NPS on Flickr](https://www.flickr.com/photos/yellowstonenps/)

With the COVID-19 quarantine disrupting life for many of us, I thought I’d put together a list of things you can do with your website on a rainy day. These are things to keep your business moving even if you’re at home and some of your projects are stuck waiting on things to reopen. If you’re looking for some useful things to do to fill your days over the next few months, this post is for you!

### Major Version Updates

Make a list of your entire stack, from OS to database to development frameworks. Note the current version and research the current supported versions. I find Wikipedia pages to be fairly reliable for this (e.g. [https://en.wikipedia.org/wiki/CentOS](https://en.wikipedia.org/wiki/CentOS)). Ok, so what things need to be updated, or will need to be in the next year? Start on those now and use some downtime to get ahead of your updates.

#### Sample of a client’s stack review

<div class="table-scroll">
  <table>
    <thead>
      <td>Software</td>
      <td>Purpose</td>
      <td>Our version</td>
      <td>Release date</td>
      <td>End of support</td>
      <td>Next update</td>
      <td>Newest version</td>
      <td>Notes</td>
    </thead>
    <tr>
      <td>CentOS</td>
      <td>OS for e-commerce server</td>
      <td>7</td>
      <td>July 2014</td>
      <td>June 2024</td>
      <td>Not imminent</td>
      <td>8</td>
      <td><a href="https://wiki.centos.org/About/Product">https://wiki.centos.org/About/Product</a></td>
    </tr>
    <tr>
      <td>Nginx</td>
      <td>Web server</td>
      <td>1.16.0</td>
      <td>March 2020</td>
      <td>Unclear</td>
      <td>Not imminent</td>
      <td>1.16.1</td>
      <td><a href="https://nginx.org/">https://nginx.org/</a></td>
    </tr>
    <tr>
      <td>PostgreSQL</td>
      <td>Database server</td>
      <td>9.5.20</td>
      <td>January 2016</td>
      <td>Feb 2020</td>
      <td>Medium term, to version 11</td>
      <td>12</td>
      <td><a href="https://www.postgresql.org/support/versioning/">https://www.postgresql.org/support/versioning/</a></td>
    </tr>
    <tr>
      <td>Rails</td>
      <td>App framework for store</td>
      <td>5.1</td>
      <td>February 2017</td>
      <td>Current</td>
      <td>Long Term, to version 6</td>
      <td>6</td>
      <td><a href="https://rubygems.org/gems/rails/versions>https://rubygems.org/gems/rails/versions</a></td>
    </tr>
    <tr>
      <td>Spree</td>
      <td>Ecommerce and admin gem</td>
      <td>3.3</td>
      <td>April 2017</td>
      <td>Current</td>
      <td>Long Term, to version 4</td>
      <td>4</td>
      <td><a href="https://rubygems.org/gems/spree/versions">https://rubygems.org/gems/spree/versions</a></td>
    </tr>
    <tr>
      <td>Elasticsearch</td>
      <td>Search platform for product import/search</td>
      <td>5.6.x</td>
      <td>September 2017</td>
      <td>March 2019</td>
      <td>Immediate, to version 6.8</td>
      <td>7.4</td>
      <td><a href="https://www.elastic.co/support/eol">https://www.elastic.co/support/eol</a></td>
    </tr>
    <tr>
      <td>WordPress</td>
      <td>Info site</td>
      <td>5.2.3</td>
      <td>September 2019</td>
      <td>Unclear</td>
      <td>5.2.4 shipped recently</td>
      <td>5.2</td>
      <td><a href="https://codex.wordpress.org/Supported_Versions">https://codex.wordpress.org/Supported_Versions</a></td>
    </tr>
  </table>
</div>

### Content Cleanup & SEO Review

Everyone’s website gets cluttered with outdated content. Take a look at your pages, review, and update what needs to be changed. Pay attention to search engine optimization (SEO) concerns as you go through it. Make sure your content has headers, accurate keywords, and good meta-descriptions. Research SEO best practices if you need a refresher.

Nowadays, reducing repeated content has huge benefits for SEO so we recommend any content review includes a review of duplication. If you have a small site, you can go through your content and SEO manually. Larger projects can utilize tools on the market such as [Siteliner](http://www.siteliner.com/) or [WPOptimize](https://wordpress.org/plugins/wp-optimize/).

While you’re taking a dive into content, don’t forget to review your Google Analytics and understand what content is being used and what isn’t. Google has added many new features to Analytics and Ads, so it’s a good idea to refresh yourself on the updated documentation and new features.

### Reporting

A lot of clients with big ecommerce data sets or other applications that collect data benefit from a separate reporting or business analytics tool. A rainy day can be a good time to think about what reports you want on last year’s business, what data will help you plan for the future. End Point has worked with a few different reporting tools that easily add on to your database, like [Pentaho](https://www.hitachivantara.com/en-us/products/data-management-analytics/pentaho-platform.html) or [Jasper](https://www.jaspersoft.com/reporting-software) and those can be really useful.

### Documentation

I wouldn’t be a good project manager if I didn’t throw this one in the list. Documentation is so, so important, yet really we can always do more. End Point uses a few different tools, including wikis running [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki)  and Google Docs, for keeping track of project details. Now’s a good time to set up a nice documentation system or do a big review and make sure everything is updated and back in order. Maybe dream of a vacation you *might* be able to take when this is over and make sure everything’s ready for you to do that.

### Disaster Recovery Tests

For anyone with business-critical infrastructure, you need to ensure you know how to get everything back up and running in the case of a major failure, either with on-premises or cloud hosting. Now’s a good time to clarify with your hosting vendor things like: What are your backups like? What is your disaster recovery plan? What is the timeline for recovering the application in the event of a major failure? If you can, take time to do a simulation and make sure all the pieces are there if they need to be. Simply said, we also need to test our backups in order to ensure that they actually work.

### Redesign

If you’ve been meaning to refresh your website, a rainy day is prime time to do it. Designers and developers are looking for projects and you’ll have extra time on your hands to oversee the process, spend time reviewing and testing, and get things done just the way you want.

### Automated Testing

Good developers want an automated test suite as part of their application. Not all applications were built with this from the beginning and many didn’t have the budget or time to get it done. With extra time on your hands, this can be a great time to start building your test suite or to improve the coverage of your existing one.

Unit tests in particular are a good place to start. Unit tests are great not only because they help validate software correctness and protect against regressions, but also because they require a well-factored and modular system. This means that, while writing your unit tests, you will often be forced to go back to your application’s code base and refactor it to make it testable, to make it better. Investing in creating a solid unit test suite is a great bang for your buck. You can also look at implementing continuous integration—having a pipeline to let multiple developers deploy code throughout the day and configure your automated tests into the workflow.

### Versioning & Deployment Tools

When you’re cleaning house, take a look at your Git version control repository and make sure everything important is in there. We have a few projects that have a main project in Git, but sometimes the smaller projects and one-offs can go astray. This is a good time to get everything organized into one repository, or make sure external repositories are connected and integrated.

Automated DevOps deployment tools can also be nice to work on. Tools like Ansible and Chef can take a lot of time to set up and test, but they have some great time-saving and accuracy advantages down the line. Our in-house security experts also recommend tools like AIDE and OSSEC which automate monitoring file changes daily.

### Security Audit and Monitoring

Taking a few days to review your personal security and that of your application is something you should do regularly and now’s a good time to plan for it. Charlie’s got [a great security post](/blog/2020/02/05/end-point-security-tips) that’s a good top-level review. For application security, End Point uses some tools for vulnerability scanning. We also have a checklist of basic security items that include password handling, PII data, and other common security holes. For certain projects/clients we must also take HIPAA or PCI DSS compliance into account. Also, don’t neglect to review your TLS status and ensure that web applications run on TLS 1.2 and are TLS 1.3 ready. This also may relate to the underlying operating systems—whether they are able to support the latest TLS version natively.

### Optimization and Performance:

Most of the time new features have higher priority than improving the performance of an existing system. It could be the right time to review core functionalities and list out the areas that need improvement in serving a better experience to customers by optimization. The areas can be focused on optimizing code, database queries, image size, data compression over network,  adding cache, CDN, and so on. We’ve been moving quite a few clients to the [Cloudflare](https://www.cloudflare.com/) DNS and CDN service and we’ve been really happy with it. Optimization work will definitely influence the customer retention rate which helps to increase profitability long term.

### Refactoring

Along the same lines as optimization, code refactoring can have long term gains in performance and ease of future development. Think of this like house cleaning. It is always easier to find any item in the house when things are arranged in an orderly manner. Similarly, the organized and clean code base will play a vital role in future code changes and development, helping to reduce the chances of unexpected bugs, save time making changes at one place and improving code readability. Disciplined refactoring delivers readable, reusable, non-redundant code. Refactoring can be applied to your databases and user interfaces as well.

Want to get started on some background projects for your website? [Talk to us today](/contact).
