---
author: Steph Skardal
gh_issue_number: 456
tags: conference, rails
title: Coding Tips from RailsConf 2011
---

A couple of the sessions I attended on Day 1 of RailsConf 2011 were along the lines of how to write good Rails code: [Keeping Rails on the Tracks](http://en.oreilly.com/rails2011/public/schedule/detail/17703) by Mikel Lindsaar and [Confident Code](http://en.oreilly.com/rails2011/public/schedule/detail/18418) by Avdi Grimm. Here's a mishmash summary from these talks. Although the talks didn't focus on Ruby and Rails techniques, both talks had plenty of  examples and tips for writing maintainable code that apply to my world of consulting and development.

<a href="/blog/2011/05/20/coding-tips-from-railsconf-2011/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5608600298183857506" src="/blog/2011/05/20/coding-tips-from-railsconf-2011/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 92px;"/></a>

In the first talk, Mikel talked about what he meant by keeping Rails on the Tracks and the balance that we might often experience between just working code and sexy code. Maintainable code lands in the middle there somewhere. And he briefly touched on the fact that budget matters in writing maintainable code, trade-offs are part of life, and that you are selling a solution and not code, which means that clients don't really care about the technology as long as it's maintainable.

Mikel's first **pro tip** for building a maintainable Rails app is to treat deployment as a first class citizen by having trivial deployment that takes advantage of existing tools like Chef and Puppet. Using Bundler will help you avoid additional pain, but be careful of avoiding locking on git repos that you don't own since you can't control these other repos. This really speaks to End Point's [camps](http://www.devcamps.org/) project — it's so easy to deploy changes on many of our campified Perl-based [Interchange](http://www.icdevgroup.org/i/dev) sites, but more difficult for clients that aren't on camps. The bottom line is that having trivial deployment saves time &amp; money.

Mikel also mentioned several performance tips that make clients happy, listed below. I wasn't sure how these recommendations fit into the talk on how to keep Rails on the tracks by writing maintainable code, but nonetheless here they are:

- combining JS, CSS, CSS sprites, utilizing [the Rails 3.1 asset pipeline](http://blog.endpoint.com/2011/05/rails-3-at-railsconf-2011.html)
- caching optimization: fragment caching, action caching, page caching
- avoid a bloated session, and avoid storing objects in the session
- push things out to the browser if possible to minimize data and web-app load

Another topic that Mikel touched on was how being smart can be stupid. He recommends to not use before and after filters for object instantiation and to minimize their use to state modifications such as authentication, authorization or related to the user session. Mikel mentioned that while meta programming is sexy and has its place, that that place is not in your Rails app because it's harder for other developers and even yourself to understand what's automagically happening when you look at the code 3 months after you wrote it.

Mikel mentioned a few examples of using the right tools for the job. He discussed two examples where using simple SQL reduced a Ruby report run-time from 45 minutes down to 15 seconds and a implementing a PostgreSQL COPY statement that completed a data migration in 74 minutes down from 150 hours. Mikel also noted that Cucumber is not unit testing, so just write unit tests!

### Confident Code

Next up, Avdi gave a nice talk about writing confident code and explained the standard narrative of a method or function:

<a href="/blog/2011/05/20/coding-tips-from-railsconf-2011/image-1-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5608892855043260754" src="/blog/2011/05/20/coding-tips-from-railsconf-2011/image-1.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 255px; height: 400px;"/></a>

When gathering input, Avdi recommends that developers employ strategies to deal with uncertain inputs such as coercion (e.g. to_s, to_i), rejection (guard clause or something more complex to return method), or ignoring invalid inputs. He also talked about his approach to having a zero tolerance for nil in Ruby because it's overused and can be indicative of too many things such as an error, missing data, the default behavior, and an uninitialized variable.

In part 2 of the narrative, perform work, I liked Avdi's comments about how conditionals should be reserved for business logic. For example, consider the following two conditionals:

```nohighlight
A) if post.published?  ... end
B) if post ... end
```

The first line of code most likely represents business logic, while the second line may not. We want to minimize occurrences of instances of the second where conditionals are not representative of business logic. Avdi also touched on writing with the confident styles of chaining and iterative style such as that used in jQuery, where a jQuery selector does nothing when empty.

In part 3 of the narrative, deliver results, Avdi suggested to employ a style to raise a special case or a null object rather than a meaningless nil if there are no results. Finally, while handling failures, Avdi suggested to write the happy path first and have a visual divide in the code between the happy and unhappy paths.

### Conclusion

My takeaways from the talks are:

- write code for people first (even yourself), then computers. This seemed to be a recurring recommendation at RailsConf.
- writing code is communicating the business logic. make sure it's clear, componentized, and each method has a single responsibility.
- like photography, sometimes the art is more about what you leave out rather than what you include.

While these takeaways aren't novel, I did like the insight into how both speakers approach development.
