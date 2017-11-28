---
author: Steph Skardal
gh_issue_number: 437
tags: ecommerce, ruby, rails
title: Ruby, Rails, and Ecommerce
---



I'm a big fan of Ruby. And I like Rails too. Lately, I've been investigating several Ruby, Rails, and Rails ecommerce framework options (follow-up to [discussing general ecommerce options](/blog/2011/02/28/ecommerce-solutions-options)). I've also recently written about developing ecommerce on Sinatra ([one](/blog/2011/01/17/sinatra-ecommerce-tutorial), [two](/blog/2011/01/22/ruby-ecommerce-sinatra-products-admin), and [three](/blog/2011/03/04/ecommerce-sinatra-shopping-cart)). Most of End Point's clients are ecommerce clients, so we've seen it all in terms of feature requests (third party integration like QuickBooks, search, PayPal, product features like best sellers, recommended items, related items, checkout features like one-page checkout, guest checkout, backend features like advanced reporting, sales management, inventory management). Our services also include hosting and database consulting for many of our ecommerce clients, so we have a great understanding of what it takes to run an ecommerce solution.

When it comes to ecommerce development, someone who likes coding in Ruby (like me) has a few options:

- Ruby DSL (e.g. Sinatra)
- Pure Rails
- Open Source Ecommerce on Rails: Spree, ROR-Ecommerce, Substruct. End Point admittedly has the most experience with Spree.

Here's a run down of some pros and cons of each option:

<table cellpadding="10" cellspacing="0" width="100%">
<tbody><tr>
<td>
</td>
<td align="center" width="300">Pros</td>
<td align="center" width="300">Cons</td>
</tr>
<tr style="background:#DDE4DF;">
<td valign="top"><br/>Ruby DSL</td>
<td>
<ul>
<li>Removes the bloat of Rails and may have better performance at the onset</li>
<li>API friendly (i.e. writing APIs to handle both web and mobile apps is pleasant)</li>
<li>Ruby gems are available, such as ActiveMerchant, ActiveShipping, Paperclip.</li>
<li>Routing in DSL might be easier to work with than Rails.</li>
<li>Extremely flexible</li>
</ul>
</td>
<td valign="top">
<ul>
<li>Minimal view and form helpers</li>
<li>A smaller community than Rails (likely)</li>
<li>As your application grows, you essentially need to implement conventions that mimic those of Rails to keep code organized.</li>
<li>Too much flexibility can result in convoluted, disorganized code.</li>
</ul>
</td>
</tr>
<tr style="background:#EDF4EF;">
<td valign="top"><br/>Rails</td>
<td valign="top">
<ul>
<li>Large and active community</li>
<li>Ruby gems are available, such as ActiveMerchant, ActiveShipping, Paperclip.</li>
<li>A lot of documentation is available.</li>
<li>The elegant, modern, MVC conventions allow for efficient developoment.</li>
</ul>
</td>
<td valign="top">
<ul>
<li>Performance can be an issue at the onset of the project (relative to Ruby DSL), but there are plenty of caching options that can address this.</li>
<li>The bloat in Rails might be stuff your application doesn't need which can add complication.</li>
<li>You are essentially reinventing the wheel if you are building a standard ecommerce application.</li>
</ul>
</td>
</tr>
<tr style="background:#DDE4DF;">
<td valign="top"><br/>Open Source Ecommerce on Rails</td>
<td valign="top">
<ul>
<li>Community code, expertise and experience can be leveraged.</li>
<li>You aren't reinventing the wheel.</li>
<li>The elegant, modern, MVC conventions in Rails allow for efficient developoment.</li>
</ul>
</td>
<td valign="top">
<ul>
<li>The framework has been shaped by the clients on it. If it's a young framework, aspects of the ecommerce application can result in under or overdeveloped components (e.g. purchase order system, inventory management, ability to scale).</li>
<li>The framework can be overly complicated at the cost of genericizing it, which can cause problems in development, performance.</li>
<li>You are at the mercy of the maintainers of the framework to make decisions on the ecommerce framework involving extensibility, long-term maintenance and support, and feature inclusion in the project.</li>
</ul>
</td>
</tr>
</tbody></table>

Or, here's another way to look at things:

<img src="http://chart.apis.google.com/chart?chxl=0:|Open+Source+Ecommerce|Rails|Ruby+DSL+(Sinatra)|1:|Less|More&chxp=0,1,2,3|1,1,3&chxr=0,0,3|1,0,3.2&chxt=y,x&chbh=a,4,14&chs=750x300&cht=bhg&chco=4D89F9,97D2F0,ECBA24,376F19,80C65A&chds=0,3.2,0,3.2,0,3.2,0,3.2,0,3.2&chd=t:1,2,3|3,2,1|2,2,3|1,2,3|3,2,2&chdl=Assumptions+Made|Flexibility|Technology+Changes+Over+Time|Conventions|Initial+Coding+Required"/>
Generalizations I've made after developing in each of the scenarios.

Another thing to consider is what might happen when application changes are required a year after the project was initially implemented. Here's what might happen in each of the scenarios:

- **Ruby DSL:** You still have to write custom code. You may pick up using the conventions and organization where you left off. You may be able to use open source gems in your application. Ruby probably hasn't changed a ton. The Ruby DSL (e.g. Sinatra) may have changed.
- **Rails:** You still have to write custom code in Rails. You may be able to use open source gems in your application. Rails may have changed if there was a major release, but chances are your current version of Rails is still supported.
- **Open Source Ecommerce on Rails:** You may or may not have to write custom code because the community may provide the functionality you need. The platform may have changed significantly, and there's a chance that your current version of the platform is no longer supported.

Any one of the options presented in this article may be suitable for our clients: Sinatra for a small, simple, custom app, Rails for a complex application with custom needs, open source ecommerce on Rails for a client that follows the standard ecommerce mold. As consultants, our goal is to choose the best tool for a client to meed their business needs, long-term goals and budget.

One final note to add is that my generalizations discussed here regarding open source ecommerce on Rails and open source projects in general are highly dependent on the maturity of the framework. As an open source project matures, its stability and flexibility may improve.


