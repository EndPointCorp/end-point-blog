---
author: Steph Skardal
title: Raw Caching Performance in Ruby/Rails
github_issue_number: 476
tags:
- performance
- ruby
- rails
date: 2011-07-12
---

Last week, I set up [memcached](https://memcached.org/) with a Rails application in hopes of further improving performance after getting a recommendation to pursue it. We’re already using many [Rails low-level caches](http://blog.nathanhumbert.com/2011/01/data-caching-in-rails-3.html) and [fragment caches](https://guides.rubyonrails.org/caching_with_rails.html#fragment-caching) throughout the application because of its complex role management system. Those are stored in NFS on a [NetApp](https://www.netapp.com/us/) filer, and I was hoping switching to memcached would speed things up. Unfortunately, my http request performance tests (using [ab](https://linux.die.net/man/1/ab)) did not back this up: using file caching on NFS with the NetApp was about 20% faster than memcached from my tests.

I brought this up to [Jon](/team/jon-jensen), who suggested we run performance tests on the caching mechanism only rather than testing caching via full http requests, given how many layers of the stack are involved and influence the overall performance number. From the console, I ran the following:

```ruby
$ script/console   # This app is on Rails 2.3
> require 'benchmark'
> Rails.cache.delete("test")
> Rails.cache.fetch("test") { [SomeKlass.first, SomeKlass.last] }
> # to emulate what would potentially be stored with low-level cache
> Benchmark.bm(15) { |x| x.report("times:") { 10000.times do; Rails.cache.fetch("test"); end } }
```

We ran the console test with a few different caching configurations, with the results shown below. The size of the cached data here was ~2KB.

<table cellpadding="5" cellspacing="0" width="100%">
<tbody><tr>
<th>cache_store</th>
<th>avg time/request</th>
</tr>
<tr>
<td>:mem_cache_store</td>
<td>0.00052 sec</td>
</tr>
<tr>
<td>:file_store, tmpfs (local virtual memory RAM disk)</td>
<td>0.00020 sec</td>
</tr>
<tr>
<td>:file_store, local ext4 filesystem</td>
<td>0.00017 sec</td>
</tr>
<tr>
<td>:file_store, NetApp filer NFS over gigabit Ethernet</td>
<td>0.00022 sec</td>
</tr>
</tbody></table>

<img alt="chart1" src="https://chart.apis.google.com/chart?chxl=0:|memcached|tmpfs|ext4|netapp&chxt=x&chbh=a&chs=600x300&cht=bvg&chco=A2C180&chds=0,0.6&chd=t:0.524,0.196,0.173,0.215&chtt=Small+Cache+Raw+Caching+Performance+(time+in+sec+%2F+cache+hit)"/>

I also ran the console test with a much larger cache size of 822KB, with much different results:

<table cellpadding="5" cellspacing="0" width="100%">
<tbody><tr>
<th>cache_store</th>
<th>avg time/request</th>
</tr>
<tr>
<td>:mem_cache_store</td>
<td>0.00022 sec</td>
</tr>
<tr>
<td>:file_store, tmpfs (local virtual memory RAM disk)</td>
<td>0.01685 sec</td>
</tr>
<tr>
<td>:file_store, local ext4 filesystem</td>
<td>0.01639 sec</td>
</tr>
<tr>
<td>:file_store, NetApp filer NFS over gigabit Ethernet</td>
<td>0.01591 sec</td>
</tr>
</tbody></table>

<img alt="chart2" src="https://chart.apis.google.com/chart?chxl=0:|memcached|tmpfs|ext4|netapp&chxt=x&chbh=a&chs=600x300&cht=bvg&chco=A2C180&chds=0,0.02&chd=t:0,0.017,0.016,0.016&chtt=Large+Cache+Raw+Caching+Performance+(time+in+sec+%2F+cache+hit)"/>

### Conclusion

It’s interesting to note here that the file-system caching outperformed memcached on the smaller cache, but memcached far outperformed the file-system caching on the larger cache. Ultimately, this difference is negligible compared to additional Rails optimization I applied after these tests, which I’ll explain in a future blog post.
