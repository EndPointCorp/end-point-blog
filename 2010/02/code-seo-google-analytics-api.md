---
author: Steph Skardal
title: More Code and SEO with the Google Analytics API
github_issue_number: 271
tags:
- analytics
- ecommerce
- seo
date: 2010-02-22
---



My latest blog article inspiration came from an [SEOmoz](https://moz.com/) pro webinar on Actionable Analytics. This time around, I wrote the article and it was published on SEOmoz’s YOUmoz Blog and I thought I’d summarize and extend the article here with some technical details more appealing to our audience. The article is titled [Visualizing Keyword Data with the Google Analytics API](https://moz.com/ugc/visualizing-keyword-data-with-the-google-analytics-api).

In the article, I discuss and show examples of how the number of unique keywords receiving search traffic has diversified or expanded over time and that our SEO efforts (including writing blog articles) are likely resulting in this diversification of keywords. Some snapshots from the articles:

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5440105453691734738" src="/blog/2010/02/code-seo-google-analytics-api/image-0.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 650px;"/>
<img alt="" border="0" id="BLOGGER_PHOTO_ID_5440105457342635154" src="/blog/2010/02/code-seo-google-analytics-api/image-1.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 650px;"/>
The unique keyword (keywords receiving at least one search visit)
count per month (top) compared to the number of articles available
on our blog at that time (bottom).

I also briefly examined how unique keywords receiving at least one visit overlapped between each month and saw about 10-20% of overlapping keywords (likely the short-tail of SEO).

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5440105468382437666" src="/blog/2010/02/code-seo-google-analytics-api/image-2.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 650px;"/>
The keyword overlap per month, where the keywords receiving at least
one visit in consecutive months are shown in the overlap section.

Now, on to things that End Point’s audience may find more interesting. Something that might appeal more to our developer-types is the code written to use the Google Analytics API to generate the data used for this article. I researched a bit and tried writing my own ruby code (gem-less) to pull from the Google API, followed by using the Gattica gem, and finally the garb gem. After wrestling with the former two options, I settled on the [garb](https://github.com/vigetlabs/garb) gem, which had decent documentation [here](https://github.com/vigetlabs/garb/wiki) to get me up and running with a Google Analytics report quickly. Here’s an example of the code required to create your first Google Analytics API report:

```ruby
#!/usr/bin/ruby

require 'rubygems'
require 'garb'

# set email, password, profile_id
Garb::Session.login(email, password)
profile = Garb::Profile.first(profile_id)

report = Garb::Report.new(profile,
        :limit => 100,
        :start_date => Date.today - 30,
        :end_date => Date.today)
report.dimensions :keyword
report.metrics :visits
report.results.each do |result|
  puts "#{result.keyword}:#{result.visits}"
end
```

If you aren’t familiar with the Google Analtyics API, possible dimensions and metrics are documented [here](https://developers.google.com/analytics/devguides/reporting/core/dimsmets). There are some Google Analytics API limitations on metric and dimension combinations, but I think if you get creative you’d be able to overcome most of those limitations (assuming you won’t be exceeding the limit of 1,000 API requests per day).

Why should you care about the Google Analytics API? Well, the API allowed me to programmatically aggregate the keyword counts in monthly increments for the SEOmoz article. One thing I consider to be pretty **lame** is the inability to select more than 3 custom segments and exclude the “All Visits” segment to allow a better visual comparison of the segments. In the data below, I have 3 defined custom segments. I would prefer to compare about 10 custom segments of End Point’s blog keyword groupings (e.g., “Rails Keywords”, “Postgres Keywords”), but Google Analytics limits the selected segments and includes “All Visits” when you select more than one custom segment.

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5441118019534463634" src="/blog/2010/02/code-seo-google-analytics-api/image-3.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width:750px;"/>

Another thing I consider to be **lame** is the inability to merge Google Analytics profiles. Recently, End Point combined its corporate blog GA profile with its main website GA profile to better track conversion between the sites:

        

<img alt="" border="0" id="BLOGGER_PHOTO_ID_5441118241865576018" src="/blog/2010/02/code-seo-google-analytics-api/image-4.png" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width:750px;"/>Dead metrics from migrated profile.

With the Google Analytics API, we could compute different aggregates of data, compare more than a few custom data segments, and combine two google profiles if they have merged. Of course, these things wouldn’t necessarily be easy, but working with the gem proved to be simple, so in theory this all could be done and in the meantime we’ll keep our dead profile around.

Again, please read the original article [here](https://moz.com/ugc/visualizing-keyword-data-with-the-google-analytics-api) if you are interested :)


