---
author: Marina Lohova
gh_issue_number: 682
tags: rails
title: Paginating API call with Radian6
---



I wrote about Radian6 in my [earlier blog post](/blog/2012/06/29/respecting-api-call-limit-with-radian6). Today I will review one more aspect of Radian6 API - call pagination.

Most Radian6 requests return paginated data. This introduces extra complexity of making request several times in the loop in order to get all results. Here is one simple way to retrieve the paginated data from Radian6 using the powerful Ruby blocks.

I will use the following URL to fetch data:

*/data/comparisondata/1338958800000/1341550800000/2777/8/9/6/*

Let's decypher this.

- 1338958800000 is **start_date**, 1341550800000 is **end_date** for document search. It's June, 06, 2012 - July, 06, 2012 formatted with date.to_time.to_i * 1000.

- 2777 is **topic_id**, a Radian6 term, denoting a set of search data for every customer.
- 8 stands for Twitter media type. There are various media types in Radian6. They reflect where the data came from. **media_types** parameter can include a list of values for different media types separated by commas.
- 9 and 6 are **page** and **page_size** respectively.

First comes the method to fetch a single page.

In the Radian6 wrapper class:

```ruby
def page(index, &block)
  data = block.call(index) 
  articles, count = data['article'], data['article_count'].to_i  
  [articles, count]
end
```

A data record in Radian6 is called an **article**. A call returns the  'article' field for a page of articles along other useful fields.

Now we will retrieve all pages of data from Radian6:

```ruby
def paginated_call(&block)
  articles, index, count = [], 0, 0
  begin
    index += 1
    batch, count = page(index, &block)
    articles += batch 
  end while count > 0
  articles
end
```

Time to enjoy the method! I'm using [httparty](https://github.com/jnunemaker/httparty/) gem to make requests to API.

```ruby
paginated_call do |page|
  get("/data/comparisondata/1338958800000/1341550800000/2777/8/#{page}/1000/")
end
```

Thanks for flying!


