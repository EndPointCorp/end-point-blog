---
author: Brian Buchalter
gh_issue_number: 534
tags: ruby, rails
title: Importing Comments into Disqus using Rails
---



It seems everything is going to the cloud, even comment systems for blogs.  Disqus is a platform for offloading the ever growing feature set users expect from commenting systems.  Their website boasts over a million sites using their platform and offers a robust feature set and good performance.  But before you can drink the Kool-Aid, you’ve got to get your data into their system.

If you’re using one of the common blog platforms such as WordPress or Blogger, there are fairly direct routes Disqus makes available for automatically importing your existing comment content.  For those with an unsupported platform or a hand-rolled blog, you are left with exporting your comments into XML using WordPress’s WXR standard.

Disqus leaves a lot up to the exporter, providing only one page in there knowledge base for using what they describe as a [Custom XML Import Format](https://help.disqus.com/developer/custom-xml-import-format).  In my experience the import error messages were cryptic and my email support request is still unanswered 5 days later.  (Ok, so it was Christmas weekend!)

So let’s get into the nitty gritty details.  First, the sample code provided in this article is based on Rails 3.0.x, but should work with Rails 3.1.x as well.  Rails 2.x would work just as well by modifying the way the Rails environment is booted in the first lines.  I chose to create a script to dump the output to standard output which could be piped in to a file for upload.  Let’s see some of the setup work.

### Setting up a Rails script

I choose to place the script in the RAILS_ROOT/scripts directory and named it wxr_export.rb.  This would allow me to call the script with the Rails 2.x style syntax (ahh, the nostalgia):

```bash
script/wxr_export.rb > comments.xml
```

This would fire up the full Rails enviornment, execute our Ruby code, and pipe the standard output to a file called comments.xml.  Pretty straightforward, but it’s not that often Rails developers think about creating these kind of scripts, so it’s worth discussing to see the setup mechanics.

```bash
#!/usr/bin/env ruby
require File.expand_path('../../config/boot', __FILE__)
require File.expand_path('../../config/environment', __FILE__)
```

I think the first line is best explained by this excerpt from [Ruby Programming](https://en.wikibooks.org/wiki/Ruby_Programming/Hello_world#Using_env):

> First, we use the env command in the shebang line to search for the ruby executable in your PATH and execute it.  This way, you will not need to change the shebang line on all your Ruby scripts if you move them to a computer with Ruby installed a different directory.

The next two lines are essentially asking the script to boot the correct Rails environment (development, testing, production).  It’s worth briefly offering an explanation of the syntax of these two somewhat cryptic lines.  [File#expand_path](https://ruby-doc.org/core-1.9.3/File.html#method-c-expand_path) converts a pathname to an absolute pathname.  If passed only the first string, it would use the current working path to evaluate, but since we pass __FILE__ we are asking it to use the current file’s path as the starting point.

The config/boot.rb file is well documented in the [Rails guides](http://guides.rubyonrails.org/initialization.html#config-boot-rb) which explains that boot.rb defines the location of your Gemfile, hooks up Bundler, which adds the dependencies of the application (including Rails) to the load path, making them available for the application to load.

The config/enviornment.rb file is also [well documented](http://guides.rubyonrails.org/initialization.html#config-environment-rb) and effectively loads the Rails packages you’ve specified, such as ActiveModel, ActiveSupport, etc...

### Exporting WXR content

Having finally loaded our Rails enviornment in a way we can use it, we are ready to actually build the XML we need.  First, let’s setup our XML and the gerenal format we’ll use to popualate our file:

```ruby
# script/wxr_export.rb

xml = Builder::XmlMarkup.new(:target => STDOUT, :indent => 2)

xml.instruct! :xml, :version=>"1.0", :encoding=>"UTF-8"

xml.rss 'version' => "2.0",
        'xmlns:content' => "http://purl.org/rss/1.0/modules/content/",
        'xmlns:dsq' => "http://www.disqus.com/",
        'xmlns:dc' => "http://purl.org/dc/elements/1.1/",
        'xmlns:wp' => "http://wordpress.org/export/1.0/" do
 
  xml.channel do
    Articles.all.each do |article|
      if should_be_exported?(article)
        xml.item do

          #Article XML goes here

   article.comments.each do |comment|
      
     #Comments XML goes here

   end #article.comments.each
 end   #xml.item
      end     #if should_be_exported?
    end       #Articles.all.each
  end         #xml.channel
end           #xml.rss
```

This is the general form for the [WXR format](http://docs.disqus.com/developers/export/import_format/) as described by Disqus’s knowledge base article. Note that you need to nest the comments inside each specific Article’s XML. I found that I needed to filter some of my output so I added a helper function called should_be_exported? which can be defined at the top of the script. This would allow you to exclude Articles without comments, or whatever criteria you might find helpful.

With our basic format in place, let’s look at the syntax for exporting the Article fields. Keep in mind that the fields you’ll want to pull from in your system will likely be different, but the intention is the same.

### Inside the Article XML block

```ruby
# script/wxr_export.rb

# Inside the Article XML block

xml.title article.title

xml.link create_url_for(article)

xml.content(:encoded) { |x| x << "<!--[CDATA[" + article.body + "]]-->" }

xml.dsq(:thread_identifier) { |x| x << article.id }

xml.wp(:post_date_gmt) { |x| x << article.created_at.utc.to_formatted_s(:db) }

xml.wp(:comment_status) { |x| x << "open" } #all comments open
```

Let’s look at each of these fields one by one:

- **xml.title**: This is pretty straight forward, just the plain text tile of the blog article.
- **xml.link**: Disqus can use URLs for determining which comments to display on your page, so it asks you to provide a URL associated with this article.  I found that for this particular app, it would be easier to write another helper function to generate the URLs then using the Rails routes.  If you wish to use the Rails routes (and I suggest you do), then I suggest checking out this excellent post for [using routes outside of views](https://steve.dynedge.co.uk/2010/04/29/rails-3-rake-and-url_for/).
- **xml.content(:encoded)**: The purpose of this field is clear, but the syntax is not. Hope this saves you some time and headache!
- **xml.dsq(:thread_identifier)**: The other way Disqus can identify your article is by a unique identifier. This is strongly recommended over the use of a URL. We’ll just use your unique identifier in the database.
- **xml.wp(:post_date_gmt)**: The thing to keep in mind here is that we need the date in a very particular format. It needs to be in YYYY-MM-DD HH:MM:SS 24-hour format and adjusted to GMT which [typically implies UTC](https://en.wikipedia.org/wiki/Coordinated_Universal_Time#Definition_and_relationship_to_other_standards). Rails 3 makes this very easy for us, bless their hearts.
- **xml.wp(:comment_status)**: This app wanted to leave all comments open. You may have different requirements so consider adding a helper function.

### Inside the Comment XML block

```ruby
article.comments.each do |comment|
  
  xml.wp(:comment) do

    xml.wp(:comment_id) { |x| x << comment.id }

    xml.wp(:comment_author) do |x| 
      if comment.user.present? && comment.user.name.present?
        x << comment.user.name
      else
 x << ""
      end 
    end 
                  
    xml.wp(:comment_author_email) do |x| 
      if comment.user.present? && comment.user.email.present?
        x << comment.user.email
      else
        x << ""
      end 
    end 

    xml.wp(:comment_author_url) do |x|
      if comment.user.present? && comment.user.url.present?
        x << comment.user.url
      else
        x << ""
      end
    end

    xml.wp(:comment_author_IP) { |x| x << "255.255.255.255" }

    xml.wp(:comment_date_gmt) { |x| x << comment.created_at.utc.to_formatted_s(:db) }

    xml.wp(:comment_content) { |x| x << "<!--[CDATA[" + comment.body + "]]-->" }

    xml.wp(:comment_approved) { |x| x << 1 } #approve all comments

    xml.wp(:comment_parent) { |x| x << 0 }

  end #xml.wp(:comment)
end #article.comments.each
```

Again, let’s inspect this one field at a time:

- **xml.wp(:comment_id)**: Straightforward, a simple unique identifier for the comment.
- **xml.wp(:comment_author)**: Because some commentors may not have a user associated with them, I added some extra checks to make sure the author’s user and name were present. I’m sure there’s a way to shorten the number of lines used, but I was going for readability here. I’m not certain it was necessary to include the blank string, but after some of the trouble I had importing, I wanted to minimize the chance of strange XML syntax issues.
- **xml.wp(:comment_author_email)**: More of the same safe guards of having empty data.
- **xml.wp(:comment_author_url)**: More of the same safe guards of having empty data.
- **xml.wp(:comment_author_IP)**: We were not collecting user IP data, so I put in some bogus data which Disqus did not seem to mind.
- **xml.wp(:comment_date_gmt)**: See xml.wp(:post_date_gmt) above for comments about date/time format.
- **xml.wp(:comment_content)**: See xml.content(:encoded) above for comments about encoding content.
- **xml.wp(:comment_approved)**: Two options here, 0 or 1.  Typically you’d want to automatically approve your existing comments, unless of course you wanted to give a moderator a huge backlog of work.
- **xml.wp(:comment_parent)**: This little field turned out to be the cause of a lot of trouble for me.  In the comments on Disqus’s XML example, it says parent id (match up with wp:comment_id), so initially, I just put in the comment’s ID in this field.  This returned the very unhelpful error * url * URL is required to which I still have my unanswered supprot email in to Disqus.  By trial error, I found that by just setting the comment_parent to zero, I could successfully upload my comment content.  If you are using threaded comments, I suspect this field will be of more importance to you then it was to me.  When I hear from Disqus, I will update this article with more information.


