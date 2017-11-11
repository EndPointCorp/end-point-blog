---
author: Steph Skardal
gh_issue_number: 404
tags: company, analytics, ruby
title: In Our Own Words
---

What do our words say about us?

<img border="0" src="/blog/2011/02/02/in-our-own-words/image-0.png" width="800px"/>

Recently, I came across [Wordle](http://www.wordle.net/), a Java-based Google App Engine application that generates word clouds from websites and raw text. I wrote a cute little rake task to grab text from our blog to plug into Wordle. The rake task grabs the blog contents, uses REXML for parsing, and then lowercases the results. The task also applies a bit of aliasing since we use postgres, postgreSQL and pg interchangeably in our blog.

```ruby
task :wordle =&gt; :environment do
   data = open('http://blog.endpoint.com/feeds/posts/default?alt=rss&amp;max-results=999', 'User-Agent' =&gt; 'Ruby-Wget').read
   doc = REXML::Document.new(data)
   text = ''
   doc.root.each_element('//item') do |item|
     text += item.elements['description'].text.gsub(/&lt;\/?[^&gt;]*&gt;/, "") + ' '
     text += item.elements['title'].text.gsub(/&lt;\/?[^&gt;]*&gt;/, "") + ' '
   end
   text = text.downcase \
     .gsub(/\./, ' ')   \
     .gsub(/^\n/, '')   \
     .gsub(/ postgres /, ' postgresql ') \
     .gsub(/ pg /, ' postgresql ')
   file = File.new(ENV['filename'], "w")
   file.puts text
   file.close
 end
```

So, you tell me: Do you think we write like engineers? How well does this word cloud represent our skillset?
