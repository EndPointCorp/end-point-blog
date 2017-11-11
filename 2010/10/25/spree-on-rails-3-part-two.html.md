---
author: Steph Skardal
gh_issue_number: 377
tags: ecommerce, rails, spree
title: 'Spree on Rails 3: Part Two'
---

Yesterday, I [discussed my experiences on getting Rails 3 based Spree](http://blog.endpoint.com/2010/10/spree-on-rails-3-part-one.html) up and running. I've explained in several blog articles ([here](http://blog.endpoint.com/2010/03/spree-software-development.html) and [here](http://blog.endpoint.com/2010/01/rails-ecommerce-spree-hooks-tutorial.html)) that customizing Spree through extensions will produce the most maintainable code – it is not recommended to work directly with source code and make changes to core classes or views. Working through extension development was one of my primary goals after getting Spree up and running.

To create an extension named "foo", I ran rails g spree:extension foo. Similar to pre-Rails 3.0 Spree, a foo directory is created (albeit inside the sandbox/) directory as a Rails Engine. The generator appends the foo directory details to the sandbox/ Gemfile. Without the Gemfile update, the rails project won't include the new foo extension directory (and encompassed functionality). I reviewed the extension directory structure and files and found that foo/lib/foo.rb was similar to the the *_extension.rb file.

<table cellpadding="20" cellspacing="0" width="100%">
<tbody><tr><td valign="top">
<b>New</b>
<pre class="brush:ruby">
require 'spree_core'

module Foo
  class Engine < Rails::Engine

    config.autoload_paths += %W(#{config.root}/lib)

    def self.activate
      # Activation logic goes here.
      # A good use for this is performing
      # class_eval on classes that are defined
      # outside of the extension
      # (so that monkey patches are not
      # lost on subsequent requests in
      # development mode.)
    end

    config.to_prepare &method(:activate).to_proc
  end
end
</pre>
</td><td valign="top">
<b>Old</b>
<pre class="brush:ruby">
class FooExtension < Spree::Extension
  version "1.0"
  description "Describe your extension here"
  url "http://www.endpoint.com/"

  def activate
    # custom application functionality here
  end
end
</pre>
</td></tr>
</tbody></table>

I verified that the activate method was called in my extension with the following change:

```ruby
require 'spree_core'

module Foo
  class Engine < Rails::Engine

    config.autoload_paths += %W(#{config.root}/lib)

    def self.activate
      Spree::BaseController.class_eval do
        logger.warn "inside base controller class eval"
      end
    end

    config.to_prepare &method(:activate).to_proc
  end
end
```

From here, [The Spree Documentation on Extensions](http://edgeguides.spreecommerce.com/extension_tutorial.html) provides insight on further extension development. As I began to update an older extension, I ensured that my_extension/lib/my_extension.rb had all the necessary includes in the activate method and I copied over controller and library files to their new locations.

One issue that I came across was that migrations are not run with rake db:migrate and the public assets are not copied to the main project public directory on server restart. The documentation recommends building the migration within the application root (sandbox/), but this is not ideal to maintain modularity of extensions – each extension must include all of its migration files. To work-around this, it was recommended to copy over the install rake tasks from one of the core gems that copies migrations and public assets:

```ruby
namespace :foo do
  desc "Copies all migrations and assets (NOTE: This will be obsolete with Rails 3.1)"
  task :install do
    Rake::Task['foo:install:migrations'].invoke
    Rake::Task['foo:install:assets'].invoke
  end

  namespace :install do

    desc "Copies all migrations (NOTE: This will be obsolete with Rails 3.1)"
    task :migrations do
      source = File.join(File.dirname(__FILE__), '..', '..', 'db')
      destination = File.join(Rails.root, 'db')
      puts "INFO: Mirroring assets from #{source} to #{destination}"
      Spree::FileUtilz.mirror_files(source, destination)
    end

    desc "Copies all assets (NOTE: This will be obsolete with Rails 3.1)"
    task :assets do
      source = File.join(File.dirname(__FILE__), '..', '..', 'public')
      destination = File.join(Rails.root, 'public')
      puts "INFO: Mirroring assets from #{source} to #{destination}"
      Spree::FileUtilz.mirror_files(source, destination)
    end

  end
end
```

After creating the extension based migration files and creating the above rake tasks, one would run the following from the application (sandbox/) directory:

```nohighlight
steph@machine:/var/www/spree/sandbox$ rake foo:install
(in /var/www/spree/sandbox)
INFO: Mirroring assets from /var/www/spree/sandbox/foo/lib/tasks/../../db to /var/www/spree/sandbox/db
INFO: Mirroring assets from /var/www/spree/sandbox/foo/lib/tasks/../../public to /var/www/spree/sandbox/public

steph@machine:/var/www/spree/sandbox$ rake db:migrate
(in /var/www/spree/sandbox)
# migrations run
```

Some quick examples of differences in projeect setup and extension generation between Rails 3.* and Rails 2.*:

<table cellpadding="20" cellspacing="0" width="100%">
<tbody><tr><td valign="top">
<b>New</b>
<pre class="brush:plain">
#clone project
#bundle install
rake sandbox
rails server
rails g spree:extension foo
rails g migration FooThing
</pre>
</td><td valign="top">
<b>Old</b>
<pre class="brush:plain">
#clone project into "sandbox/"
rake db:bootstrap
script/server
script/generate extension Foo
script/generate extension_model Foo thing name:string start:date
</pre>
</td></tr>
</tbody></table>

Some of my takeaway comments after going through these exercises:

If there's anything I might want to learn about to work with edge Spree, it's Rails Engines. When you run Spree from source and use extensions, the architecture includes several layers of stacked Rails Engines:

<a href="/blog/2010/10/25/spree-on-rails-3-part-two/image-0-big.jpeg" onblur="try {parent.deselectBloggerImageGracefully();} catch(e) {}"><img alt="" border="0" id="BLOGGER_PHOTO_ID_5532069288049287234" src="/blog/2010/10/25/spree-on-rails-3-part-two/image-0.jpeg" style="display:block; margin:0px auto 10px; text-align:center;cursor:pointer; cursor:hand;width: 400px; height: 200px;"/></a>

Layers of Rails Engines in Spree with extensions.

After some quick googling, I found two helpful articles on Engines in Rails 3 [here](http://www.themodestrubyist.com/2010/03/01/rails-3-plugins---part-1---the-big-picture/) and [here](http://www.themodestrubyist.com/2010/03/05/rails-3-plugins---part-2---writing-an-engine/). The Spree API has been inconsistent until now - hopefully the introduction of Rails Engine will force the API to become more consistent which may improve the extension community.

I didn't notice much deviation of controllers, models, or views from previous versions of Spree, except for massive reorganization. Theme support (including [Spree hooks](http://blog.endpoint.com/2010/01/rails-ecommerce-spree-hooks-tutorial.html)) is still present in the core. Authorization in Spree still uses authlogic, but I heard rumors of moving to devise eventually. The spree_dash (admin dashboard) gem still is fairly lightweight and doesn't contain much functionality. Two fairly large code changes I noticed were:

- The checkout state machine has been merged into order and the checkout model will be eliminated in the future.
- The spree_promo gem has a decent amount of new functionality.

Browsing through the [spree-user](http://groups.google.com/group/spree-user) Google Group might reveal that there are still several kinks that need to be worked out on edge Spree. After these issues are worked out and the documentation on edge Spree is more complete, I will be more confident in making a recommendation to develop on Rails 3 based Spree.


