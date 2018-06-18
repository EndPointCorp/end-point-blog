---
author: Steph Skardal
gh_issue_number: 201
tags: seo
title: 'SEO: External Links and PageRank'
---

I had a flash of inspiration to write an article about external links in the world of search engine optimization. I’ve created many SEO reports for End Point’s clients with an emphasis on technical aspects of search engine optimization. However, at the end of the SEO report, I always like to point out that search engine performance is dependent on having high quality fresh and relevant content and popularity (for example, PageRank). The number of external links to a site is a large factor in popularity of a site, and so the number of external links to a site can positively influence search engine performance.

After wrapping up a report yesterday, I wondered if the external link data that I provide to our clients is meaningful to them. What is the average response when I report, “You should get high quality external links from many diverse domains”?

So, I investigated some data of well known and less well known sites to display a spectrum of external link and PageRank data. Here is the origin of some of the less well known domains referenced in the data below:

- [https://www.petfinder.com/](petfinder.com): This is where my dogs came from.
- [https://www.endpoint.com/](endpoint.com): That’s us!
- [http://www.sonypictures.com/movies/district9/](d-9.com): The site for the movie District 9 that I saw last weekend.
- [https://marketstreetgrill.com/](marketstreetgrill.com): Market Street Grill is a great seafood restaurant in Salt Lake City.
- [http://divascupcakes.com/](divascupcakes.com): This is a great gourmet cupcake place in Salt Lake City.
- [http://rediguana.com/](rediguana.com): A great Mexican food restaurant in Salt Lake City.

And here is the data:

<img alt="" border="0" src="/blog/2009/09/17/seo-external-links-and-pagerank/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer"/>

I retrieved the PageRank from a generic PageRank tool. [SEOmoz](https://moz.com/) was used to collect external link counts and external linking subdomains. Finally, Yahoo Site Explorer was used to retrieve external link counts to the domain in question. (Update: Sadly, Yahoo Site Explorer is no more, and was merged into [Bing Webmaster Tools](https://www.bing.com/toolbox/webmaster). See the [Webology History of Yahoo Site Explorer](https://www.webology.technology/2018/06/17/yahoo-site-explorer/) for more details.)

I chose to examine both external link counts from SEOmoz and Yahoo Site Explorer to get a better representation of data. SEOmoz compiles their data about once a month and does not have as many urls indexed as Yahoo, which explains why their numbers may be lagging behind the Yahoo Site Explorer external link counts.

Out of curiosity, I went on to plot the Page Rank data vs. Log (base 10) of the other data.

PageRank vs Log of SEOmoz external link count

<img alt="" border="0" src="/blog/2009/09/17/seo-external-links-and-pagerank/image-0.png" style="display:block; margin:0px auto 10px; text-align:center"/>

PageRank vs Log of SEOmoz external linking subdomain count

<img alt="" border="0" src="/blog/2009/09/17/seo-external-links-and-pagerank/image-0.png" style="display:block; margin:0px auto 10px; text-align:center"/>

PageRank vs Log of Yahoo SiteExplorer external link count

<img alt="" border="0" src="/blog/2009/09/17/seo-external-links-and-pagerank/image-0.png" style="display:block; margin:0px auto 10px; text-align:center"/>

PageRank is described as a theoretical probability value on a logarithmic scale and it’s based on inbound links, PageRank of inbound links, and other factors such as Google visit data, search click-through rates, etc. The true popularity rank is a rank between 1 and X, where X is equal to the total number of webpages crawled by search engine A. After pages are individually ranked between 1 and X, they are scaled logarithmically between 0 and 10.

The takeaway from this data is when an "SEO report" gives advice to "get more external links", it means:

- If your site has a PageRank of < 4, getting external links on the scale of hundreds may impact your existing PageRank or popularity
- If your site has a PageRank of >= 4 and < 6, getting external links on the scale of thousands may impact your existing PageRank or popularity
- If your site has a PageRank of >= 6 and < 8, getting external links on the scale of tens to hundreds of thousands may impact your existing PageRank or popularity
- If your site has a PageRank of >= 8, you probably are already doing something right...

Furthermore, even if a site improves external link counts, other factors will play into the PageRank algorithm. Additionally, keyword relevance and popularity play key roles in search engine results.
