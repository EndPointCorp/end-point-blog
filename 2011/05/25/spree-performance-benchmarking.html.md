---
author: Steph Skardal
gh_issue_number: 458
tags: interchange, performance, rails, scalability, spree, magento
title: Spree Performance Benchmarking
---

I see a lot of questions regarding Spree performance in the [spree-user group](http://groups.google.com/group/spree-user), but they are rarely answered with metrics. I put together a quick script using the generic benchmark tool [ab](http://httpd.apache.org/docs/2.0/programs/ab.html) to review some data. Obviously, the answer to how well a site performs and scales is highly dependent on the host and the consumption of the web application, so the data here needs to be taken with a grain of salt. Another thing to note is that only two of the following use cases are running on Rails 3.0 — many of our current Spree clients are on Spree 0.11.2 or older. I also included one non-Spree Rails ecommerce application, in addition to a few non-Rails applications for comparison. All of the tests were run from my home network, so in theory there shouldn't be bias on performance tests for sites running on End Point servers.

<table cellpadding="5" cellspacing="0" width="100%"><tbody><tr>   <td></td>   <td align="center" colspan="4">ab -n 100</td>   <td></td>  </tr>
<tr>   <td></td>   <td align="center">-c 2 homepage</td>   <td align="center">-c 20 homepage</td>   <td align="center">-c 2<br/>
product page</td>   <td align="center">-c 20<br/>
product page</td>   <td></td>  </tr>
<tr style="background-color:#424242;">   <td rowspan="2">    <b>Client #1</b><br/>
Spree: 0.11.2<br/>
Hosting: 4 cores, 512 GB RAM<br/>
DB: MySQL<br/>
# Products: &lt;100   </td>   <td>7.49</td>   <td>24.75</td>   <td>6.49</td>   <td>19.87</td>   <td>Requests per second</td>  </tr>
<tr style="background-color:#424242;">   <td>266.889</td><td>808.041</td><td>307.997</td><td>1006.552</td>   <td>Time per request (ms)</td>  </tr>
<tr>   <td rowspan="2">    <b>Client #2</b><br/>
Spree 0.11.2<br/>
Hosting: Engineyard, medium instance<br/>
DB: MySQL<br/>
# Products: 100s   </td>   <td>5.32</td><td>20.28</td><td>5.36</td><td>18.03</td>   <td>Requests per second</td>  </tr>
<tr>   <td>375.713</td><td>986.309</td><td>373.289</td><td>1109.524</td>   <td>Time per request (ms)</td>  </tr>
<tr style="background-color:#424242;">   <td rowspan="2">    <b>Client #3</b><br/>
Spree: 0.9.0<br/>
Hosting: 4 cores, 1 GB RAM<br/>
DB: PostgreSQL<br/>
# Products: &lt;100   </td>   <td>4.91</td><td>25.39</td><td>1.98</td><td>6.54</td>   <td>Requests per second</td>  </tr>
<tr style="background-color:#424242;">   <td>407.135</td><td>787.782</td><td>1011.875</td><td>3060.062</td>   <td>Time per request (ms)</td>  </tr>
<tr>   <td rowspan="2">    <b>(Former) Client #4</b><br/>
Spree: 0.11.2<br/>
Hosting: Unknown<br/>
DB: PostgreSQL<br/>
# Products: &gt;5000   </td>   <td>20.69</td><td>8.84</td><td>10.15</td><td>19.28</td>   <td>Requests per second</td>  </tr>
<tr>   <td>96.673</td><td>2262.105</td><td>196.996</td><td>1037.146</td>   <td>Time per request (ms)</td>  </tr>
<tr style="background-color:#424242;">   <td rowspan="2">    <b>Client #5</b><br/>
Spree: 0.11.2<br/>
Hosting: EngineYard, small instance<br/>
DB: MySQL<br/>
# Products: 1   </td>   <td>12.28</td><td>16.23</td><td>N/A</td><td>N/A</td>   <td>Requests per second</td>  </tr>
<tr style="background-color:#424242;">   <td>162.909</td><td>1231.945</td><td>N/A</td><td>N/A</td>   <td>Time per request (ms)</td>  </tr>
<tr>   <td rowspan="2">    <b>Client #6</b><br/>
Spree: 0.40<br/>
Hosting: 4 cores, 1 GB RAM<br/>
DB: MySQL<br/>
# Products: 50-100   </td>   <td>3.61</td><td>8.93</td><td>2.96</td><td>3.06</td>   <td>Requests per second</td>  </tr>
<tr>   <td>553.569</td><td>2240.657</td><td>675.306</td><td>6539.433</td>   <td>Time per request (ms)</td>  </tr>
<tr style="background-color:#424242;">   <td rowspan="2">    <b>SpreeDemo</b><br/>
Spree: Edge<br/>
Hosting: Heroku, 2 dynos<br/>
DB: Unknown<br/>
# Products: 100s   </td>   <td>8.17</td><td>12.79</td><td>4.7</td><td>5.48</td>   <td>Requests per second</td>  </tr>
<tr style="background-color:#424242;">   <td>244.831</td><td>1563.642</td><td>425.27</td><td>3652.927</td>   <td>Time per request (ms)</td>  </tr>
<tr>   <td rowspan="2">    <b>Client #7</b><br/>
*custom Rails ecommerce app<br/>
Hosting: 1.0 GB RAM<br/>
DB: MySQL<br/>
# Products: 1000s   </td>   <td>5.43</td><td>29.8</td><td>4.45</td><td>23.14</td>   <td>Requests per second</td>  </tr>
<tr>   <td>368.409</td><td>671.082</td><td>448.962</td><td>864.24</td>   <td>Time per request (ms)</td>  </tr>
<tr style="background-color:#424242;">   <td rowspan="2">    <b>Interchange Demo</b><br/>
Hosting: 4 cores, 2 GB RAM<br/>
DB: MySQL<br/>
# Products: &gt;500   </td>   <td>7.41</td><td>55.27</td><td>7.5</td><td>13.93</td>   <td>Requests per second</td>  </tr>
<tr style="background-color:#424242;">   <td>269.942</td><td>361.875</td><td>266.492</td><td>1435.51</td>   <td>Time per request (ms)</td>  </tr>
<tr>   <td rowspan="2">    <b>Client #8</b><br/>
*PHP site,<br/>
serves fully cached pages<br/>
with nginx with no app server or db hits<br/>
Hosting: 4 cores, 4 GB RAM   </td>   <td>10.81</td><td>30.54</td><td>6.05</td><td>9.87</td>   <td>Requests per second</td>  </tr>
<tr>   <td>184.994</td><td>654.858</td><td>330.727</td><td>2027.092</td>   <td>Time per request (ms)</td>  </tr>
<tr style="background-color:#424242;">   <td rowspan="2">    <b>Magento Demo</b><br/>
Hosting: Unknown<br/>
DB: Unknown<br/>
# Products: 100s   </td>   <td>4.26</td><td>44.85</td><td>2.68</td><td>36.29</td>   <td>Requests per second</td>  </tr>
<tr style="background-color:#424242;">   <td>469.831</td><td>445.931</td><td>745.472</td><td>551.11</td>   <td>Time per request (ms)</td>  </tr>
</tbody></table>

Here's the same data in graphical form:

## Requests per Second

<a href="/blog/2011/05/25/spree-performance-benchmarking/image-0-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5610751500251002546" src="/blog/2011/05/25/spree-performance-benchmarking/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 740px;"/></a>

## Time Per Request (ms)

<a href="/blog/2011/05/25/spree-performance-benchmarking/image-1-big.png" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5610751511624706978" src="/blog/2011/05/25/spree-performance-benchmarking/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 740px;"/></a>

We expect to see high performance on some of the sites with significant performance optimization. On smaller VPS, we expect to see the the server choke with higher concurrency.
