---
author: Brian Buchalter
gh_issue_number: 543
tags: javascript, rails
title: Using Disqus and Ruby on Rails
---

Recently, I posted about how to [import comments from a Ruby on Rails app to Disqus](/blog/2011/12/27/importing-comments-into-disqus-using). This is a follow up to that post where I outline the implementation of Disqus in a Ruby on Rails site. Disqus provides what it calls [Universal Code](http://docs.disqus.com/developers/universal/) which can be added to any site. This universal code is just JavaScript, which asynchronously loads the Disqus thread based on one of two unique identifiers Disqus uses.

### Disqus in a development environment

Before we get started, I’d recommend that you have two Disqus “sites”; one for development and one for production. This will allow you to see real content and experiment with how things will really behave once you’re in production. Ideally, your development server would be publicly accessible to allow you to fully use the Disqus moderation interface, but it isn’t required. Simply register another Disqus site, and make sure that you have your shortname configured by environment. Feel free to use whatever method you prefer for defining these kinds of application preferences. If you’re looking for an easy way, considering checking out my article on [Working with Constants in Ruby](/blog/2011/12/05/working-with-constants-in-ruby). It might look something like this:

```ruby
# app/models/article.rb

DISQUS_SHORTNAME = Rails.env == "development" ? "dev_shortname".freeze : "production_shortname".freeze

```

### Disqus Identifiers

Each time you load the universal code, you need to specify a few configuration variables so that the correct thread is loaded:

- **disqus_shortname**: tells Disqus which website account (called a forum on Disqus) this system belongs to.
- **disqus_identifier**: tells Disqus how to uniquely identify the current page.
- **disqus_url**: tells Disqus the location of the page for permalinking purposes.

Let’s create a Rails partial to set up these variables for us, so we can easily call up the appropriate comment thread.

```javascript
# app/views/disqus/_thread.html.erb
# assumes you've passed in the local variable 'article' into this partial
# from http://docs.disqus.com/developers/universal/

<div id="disqus_thread"></div>
<script type="text/javascript">

    var disqus_shortname = '<%= Article::DISQUS_SHORTNAME %>';
    var disqus_identifier = '<%= article.id %>';
    var disqus_url = '<%= url_for(article, :only_path => false) %>';

    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>
```

The above code will populate the div#disqus_thread with the correct content based on your disqus_identifier. By setting up a single partial that will always render your threads, it becomes very easy to adjust this code if needed.

### Disqus Identifier Gotcha

We found during our testing a surprising and unexpected behavior in how Disqus associates a thread to a URL. In our application, the landing page was designed to show the newest article as well as the Disqus comments thread. We found that once a new article was posted, the comments from the previous article were still shown! It seems Disqus ignored the unique disqus_identifier we had specified and instead associated the thread with the landing page URL. In our case, a simple routing change allowed us to forward the user to the unique URL for that content and thread. In your case, there may not be such an easy work around, so be certain you include both the disqus_identifier and disqus_url JavaScript configuration variables above to minimize the assumptions Disqus will make. When at all possible, always use unique URLs for displaying Disqus comments.

### Comment Counters

Often an index page will want to display a count of how many comments are in a particular thread. Disqus uses the same asynchronous approach to loading comment counts. Comment counts are shown by adding code such as the following where you want to display your count:

```ruby
# HTML
<a href="http://example.com/article1.html#disqus_thread" 
   data-disqus-identifier="<%=@article.id%>">
This will be replaced by the comment count
</a>

# Rails helper
<%= link_to "This will be replaced by the comment count", 
    article_path(@article, :anchor => "disqus_thread"), 
    :"data-disqus-identifer" => @article.id %>
```

At first this seemed strange, but it is the exact same pattern used to display the thread. It would likely be best to remove the link text so nothing is shown until the comment count is loaded, but I felt for my example, having some meaning to the test would help understanding. Additionally, you’ll need to add the following JavaScript to your page.

```javascript
# app/view/disqus/_comment_count_javascript.html.erb
# from http://docs.disqus.com/developers/universal/
# add once per page, just above </body>

<script type="text/javascript">
   
    var disqus_shortname = '<%= Article::DISQUS_SHORTNAME %>';

    /* * * DON'T EDIT BELOW THIS LINE * * */
    (function () {
        var s = document.createElement('script'); s.async = true;
        s.type = 'text/javascript';
        s.src = 'http://' + disqus_shortname + '.disqus.com/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
</script>
```

Disqus recommends adding it just before the closing </body> tag. You only need to add this code ONCE per page, even if you’re planning on showing multiple comment counts on a page. You will need this code on any page with a comment count, so I do recommend putting it in a partial. If you wanted, you could even include it in a layout.

### Styling Comment Counts

Disqus provides [extensive CSS documentation](http://docs.disqus.com/help/69/) for its threads, but NONE for its comment counters. In our application, we had some very particular style requirements for these comment counts. I found that in Settings > Appearance, I could add HTML tags around the output of the comments.

<a href="/blog/2012/01/14/using-disqus-and-rails/image-0-big.png"><img src="/blog/2012/01/14/using-disqus-and-rails/image-0.png" width="400"/></a>

This allowed me to style my comments as needed, although these fields are pretty small, so make sure to compress your HTML as much as possible.
