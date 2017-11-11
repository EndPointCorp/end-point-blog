---
author: Steph Skardal
gh_issue_number: 561
tags: ecommerce, interchange, rails, spree
title: Multi-store Architecture for Ecommerce
---



Something that never seems to go out of style in ecommerce development is the request for multi-site or multi-store architecture running on a given platform. Usually there is interest in this type of setup to encourage build-out and branding of unique stores that have shared functionality.

<a href="http://www.backcountry.com/"><img src="/blog/2012/02/29/multi-store-architecture-ecommerce/image-0.gif" style="padding-right: 10px" width="250"/></a>

<a href="http://www.steepandcheap.com/"><img border="0" src="http://www.steepandcheap.com/images/steepcheap/header/logo.png" width="200"/></a>

<img src="/blog/2012/02/29/multi-store-architecture-ecommerce/image-0.gif" style="padding-left: 10px" width="200"/>

A few of Backcountry.com's stores driven by a multi-store architecture, developed with End Point support.

End Point has developed several multi-store architectures on open source ecommerce platforms, including [Backcountry.com](http://www.backcountry.com/) (Interchange/Perl), [College District](http://www.collegedistrict.com/) (Interchange/Perl), and Fantegrate (Spree/Rails). Here's an outline of several approaches and the advantages and disadvantages for each method.

### Option #1: Copy of Code Base and Database for Every Site

This option requires multiple copies of the ecommerce platform code base, and multiple database instances connected to each code base. The stores could even be installed on different servers. This solution isn't a true multi-store architecture, but it's certainly the first stop for a quick and dirty approach to deploy multiple stores.

The **advantages** to this method are:

- Special template logic doesn't have to be written per site — the templates would simply follow the ecommerce platform's template pattern.
- Relative to Option #3 described below, no custom database development is required.
- Custom business logic may be more easily applied to a set of the stores, without affecting the other stores.

The **disadvantages** to this method are:

- Maintenance of the applications can be time consuming, as changes must be applied to all instances.
- Custom changes must be applied to all multi-store instances.
- Users and administrator accounts are not shared across multiple stores.

<table cellpadding="0" cellspacing="0" width="100%">
<tbody><tr>
<td valign="top">
<h3>Option #2: Single Code Base, Single Database</h3>
<p>In this method, there is one copy of the source code that interacts with one database. The single database would be modified to contain a store specific id per product, order, and peripheral tables. The code base would also have to be modified to be able to limit the visible products described <a href="http://blog.endpoint.com/2010/05/spree-multi-store-architecture.html">here</a>. In this method, the individual store may be identified by the domain or subdomain. With this method, there may also be code customization that allows for custom templates per store.</p>

<p>The <b>advantages</b> to this method are:</p>
<ul>
<li>Relative to Option #1, maintenance for one code base is relatively simple.</li>
<li>User and administrator accounts are shared across multiple stores.</li>
<li>Super administrators may view and manage data from one backend administrative interface.</li>
</ul>

<p>The <b>disadvantages</b> to this method are:</p>
<ul>
<li>Rights and role management can be complicated.</li>
<li>Development is required for code and database customization.</li>
<li>Development is required for coding to handle flexible templating across stores.</li>
</ul>

</td>
<td style="padding:10px 0px 0px 10px;" valign="top">
<img src="/blog/2012/02/29/multi-store-architecture-ecommerce/image-1.png" style="padding-bottom:10px;"/>
<p>
A second option in multi-store architecture may use a data model with store specific entries in various tables, described 
<a href="http://blog.endpoint.com/2010/05/spree-multi-store-architecture.html">here</a>.</p>
</td>
</tr>
</tbody></table>

### Option #3: Single Code Base, Single Database with Schemas or Views Per Store

In this method, there is one copy of the source code that interacts with a database that has views specific to that store, or a schema specific to that store. In this case, the code base would not necessarily need customization since the data model it accesses should follow the conventions of the ecommerce platform. However, moderate database customization is required in this method. With this method, there may also be code customization that allows for custom templates per store.

The **advantages** to this method are:

- Relative to Option #1, maintenance for one code base is relatively simple.
- Relative to option #2, code base changes are minimal.
- User accounts may or may not be shared across stores.
- Relative to option #2, there may be a potential performance gain by removing time spent limiting data to the current store instance.

The **disadvantage** to this method is:

- Customization and development is required for database configuration and management of multi-store database schemas.

A tangential variation on the methods above are two different codebases and functionality attached to one back-end web service and backing database, such as the architecture we implemented for Locate Express. And a similar tangential variation I've investigated before is one that might use a [Sinatra driven front-end](http://blog.endpoint.com/2011/02/ecommerce-sinatra-shopping-cart.html) and a Rails backed admin, such as [RailsAdmin](https://github.com/sferik/rails_admin) used in [Piggybak](http://blog.endpoint.com/2012/01/piggybak-mountable-ecommerce-ruby-on.html).

<a href="http://www.collegedistrict.com/"><img src="/blog/2012/02/29/multi-store-architecture-ecommerce/image-2.png" width="700"/></a>

College District has a collection of stores driven by a multi-store architecture, developed with End Point support.

### Conclusion

In most cases for our clients, there is cost-benefit analysis that drives the decision between the three options described above. Option #1 might be an acceptable solution for someone interested in building out two or three stores, but the latter two options would be more suitable for someone interested in spinning up many additional instances quickly with lower long term maintenance costs.


