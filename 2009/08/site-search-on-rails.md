---
author: Steph Skardal
title: Site Search on Rails
github_issue_number: 184
tags:
- rails
- seo
date: 2009-08-14
---

I was recently tasked with implementing site search using a commercially available site search application for one of our clients ([Gear.com](https://www.gear.com/)). The basic implementation requires that a SOAP request be made and the XML data returned be parsed for display. The SOAP request contains basic search information, and additional information such as product pagination and sort by parameters. During the implementation in a Rails application, I applied a few unique solutions worthy of a blog article. :)

The first requirement I tackled was to design the web application in a way that produced search engine friendly canonical URLs. I used Rails routing to implement a basic search:

```ruby
map.connect ':id', :controller => 'basic', :action => 'search'
```

Any simple search path would be sent to the basic search query that performed the SOAP request followed by XML data parsing. For example,
[https://www.gear.com/s/climb](https://www.gear.com/s/climb) is a search for “climb” and
[https://www.gear.com/s/bike](https://www.gear.com/s/bike) for “bike”.

After the initial search, a user can refine the search by brand, merchant, category or price, or choose to sort the items, select a different page, or modify the number of items per page. I chose to force the order of refinement, for example, brand and merchant order were constrained with the following Rails routes:

```ruby
map.connect ':id/brand/:rbrand', :controller => 'basic', :action => 'search'
map.connect ':id/merch/:rmerch', :controller => 'basic', :action => 'search'
map.connect ':id/brand/:rbrand/merch/:rmerch', :controller => 'basic', :action => 'search'
```

Rather than allow different order of refinement parameters in the URLs, such as
`http://www.gear.com/s/climb/brand/Arcteryx/merch/Altrec` and `http://www.gear.com/s/climb/merch/Altrec/brand/Arcteryx`, the order of search refinement is always limited to the Rails routes specified above and the former URL would be allowed in this example.

For example, `http://www.gear.com/s/climb/brand/Arcteryx/merch/Altrec` is a valid URL for Arcteryx Altrec climb, `http://www.gear.com/s/climb/brand/Arcteryx` for Arcteryx climb, and `http://www.gear.com/s/climb/merch/Altrec` for Altrec climb.

All URLs on any given search result page are built with a single Ruby method to force the refinement and parameter order. The method input requires the existing refinement values, the new refinement key, and the new refinement value. The method builds a URL with all previously existing refinement values and adds the new refinement value. Rather than generating millions of URLs with the various refinement combinations of brand, merchant, category, price, items per page, pagination number, and sort method, this logic minimizes duplicate content. The use of Rails routes and the chosen URL structure also creates search engine friendly URLs that can be targeted for traffic. Below is example pseudocode with the URL-building method:

```ruby
def build_url(parameters, new_key, new_value)
  # set url to basic search information
  # append brand info to url if parameters[:brand] exists or if new_key is brand
  # append merchant info to url if parameters[:merchant] exists or if new_key is merchant
  # append category info to url if parameters[:cat] exists or if new_key is cat
  # ...
end
```

The next requirement I encountered was breadcrumb functionality. Breadcrumbs are an important usability feature that provide the ability to navigate backwards in search and refinement history. Because of the canonical URL solution described above, the URL could not be used to indicate the search refinement history. For example, `http://www.gear.com/s/climb/brand/Arcteryx/merch/Altrec` does not indicate whether the user had refined by brand then merchant, or by merchant then brand. I investigated a few solutions having implemented similar breadcrumb functionality for other End Point clients, including appending the ‘#’ (hash or relative url) to the end of the URL with details of the user refinement path, using JavaScript to set a cookie containing the user refinement path whenever a link was clicked, and using a session variable to track the user refinement path. In the end, I found it easiest to use a single session variable to track the user refinement path. The session variable contained all information needed to display the breadcrumb with a bit of parsing.

For example, for the URL mentioned above, the session variable of ‘brand-Arcteryx:merch-Altrec’ would yield the breadcrumb:
`Your search: climb > Arcteryx > Altrec`
And the session variable ‘merch-Altrec:brand-Arcteryx’ would yield the breadcrumb:
`Your search: climb > Altrec > Arcteryx`. I could have used more than one session variable, but this solution worked out to be simple and comprised less than 10 lines of code.

Another interesting necessity was determining the best way to parse the XML data. I researched several XML parsers including XmlSimple, Hpricot, ReXML, and libxml. About a year ago, John Nunemaker reported on some benchmark testing of several of these packages ([Parsing XML with Ruby](http://www.railstips.org/blog/archives/2008/08/11/parsing-xml-with-ruby/)). After some investigative work, I chose Hpricot because it was very easy to implement complex selectors that reminded me of jQuery selectors (which are also easy to use). The interesting thing that I noticed throughout the implementation was that the refinement parsing took much more time than the actual product parsing and formatting. For Gear.com, the number of products returned ranges from 20-60 and products were quickly parsed. The number of refinements returned ranged from very small for a distinct search [Moccasym](https://www.gear.com/s/moccasym) (4 refinement options) to a general search [jacket](https://www.gear.com/s/jacket) (50+ refinement options). If performance is an issue in the future, I can further investigate the use of libxml-ruby or other Ruby XML parsing tools that may improve the performance.

A final point of interest was the decision to tie the Rails application to the same database that drives the product pages (which was easily done). This decision was made to allow access of frontend taxonomy information for the product categorization. For example, if a user chooses to refine a specific by a category ([jacket in Kids Clothing](https://www.gear.com/s/jacket?cat=kids-clothing)), the Rails app can retrieve all the taxonomy information for that category such as the display name, the number of products in that category, subcategories, and subsubcategories. This may be important information required for additional features, such as providing the ability to view the subcategories in this category or view other products in this category that aren’t shown in the search results.

I was happy to see the success of this project after working through the deliverables. Future work includes integration of additional search features common to many site search packages, such as implementing refinement by color and size, or retrieving recommended products or best sellers.
