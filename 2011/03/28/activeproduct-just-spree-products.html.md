---
author: Sonny Cook
gh_issue_number: 433
tags: ecommerce, rails, spree
title: ActiveProduct — Just the Spree Products
---

### ActiveProduct

I wanted to see how difficult it would be to cut out the part of
Spree that makes up the product data model and turn it into a self
sufficient Rails 3 engine. I followed the tutorial [here](https://web.archive.org/web/20100727143748/http://www.themodestrubyist.com/2010/03/05/rails-3-plugins---part-2---writing-an-engine/)
to get started with a basic engine plugin. Since it sounded good and
nobody else seems to be using it, I decided to call this endeavor ActiveProduct.

### Which Bits?

The next step was to decide which parts I needed to get. Minimally, I
need the models and migrations that support them. If that works
out, then I can decide what to do about the controllers and views later.

That said, the lines between what is needed to create a product and
the rest of the system are not always so clear cut. You have to cut
somewhere, though, so I cut like this:

- Image
- InventoryUnit
- OptionType
- OptionValue
- ProductGroup
- ProductOptionType
- ProductProperty
- Product
- ProductScope
- Property
- Prototype
- Variant

### Models

Each of these has a model file in spree/core/app/models, which I
just copied over to the app/models directory of my engine.

### Migrations

It’d be convenient if I could have just carved the appropriate parts out
of the schema.rb file for the migration. But said file does not
appear to be in evidence. Building a spree instance, and trying to
coerce one out of it just seems too annoying, so I did something else.

I started from the first migration, removed all of the table
definitions that didn’t interest me and manually applied all of the
migrations in the migration file to the remaining definitions. By
manually applied, I mean I went through each migration file one at a time
and made the specified change to the original set of definitions. There
are, of course, all kinds of reasons why this is a terrible idea. For
a reasonably small set of tables with a simple set of relations, the
trade-off isn’t too bad.

### Migration Generator

With a single migration in hand, I followed the tutorial at
[here](https://web.archive.org/web/20110423220449/http://www.themodestrubyist.com/2010/03/16/rails-3-plugins---part-3---rake-tasks-generators-initializers-oh-my/)
as a guide to create a generator for it in the engine. With
the migration set up as a generator, I went to my sandbox
rails app and ran the migration by doing the following:

```nohighlight
$ rails g active_product create_migration_file
$ rake db:migrate
```

### Did it Work?

At this point, I had some the tables in the database and the model files in
place it was time to see if things worked.

```nohighlight
$ rails console
rb(main):001:0> p = Product.new
```

...and I got a big wall of error messages. So I could not even
instantiate the class, much less start using it. Well, I kind of
expected that.

### Missing Constants

Following the error messages started with an unresolved dependency
on **delegate_belongs_to**. A little sleuthing lead me
into the Spree lib directory were a copy of this plugin lives. Some
further knocking around the interwebs lead me to 
[this project](https://web.archive.org/web/20100621082539/http://github.com:80/faber/delegate_belongs_to) which appears to be the canonical version of the plugin.
Since I was trying to create a stand alone module, I wanted set this up as an external
dependency (which I will defer figuring out how to enforce in the
engine until later).

As an aside, (the newer version of) delegate_belongs_to has an
issue with and API change in ActiveRecord for Rails 3. A version that
will at least load with ActiveProduct can be found
[here](https://github.com/sonny/delegate_belongs_to).

The active_product engine currently assumes that
delegates_belongs_to is available in the project that it is installed
in. I set it up as a normal plugin in the vendor/plugins directory.

### Circular Dependencies

With that out of the way, the next error seemed to be about Variants
and Scope. In spree/core/lib/scopes there are a couple of files that
interact with the Product and Variant classes in a somewhat messy
way. In order to make use of the scopes that are defined there, I needed to
pull them in. Ultimately, it probably makes sense to include the
changes directly into the affected class files. Since I was
still experimenting here, I just moved them to approximately the
same place in the engine.

It turns out that the dependency relationships between Product,
Variant, and the Scopes module are pretty complex. I spent a fair
amount of time trying to sort them out manually, but was unable to
find any reasonable way. Eventually, I decided to give up and fall back on
the auto loader to handle it for me.

The auto-loader in Rails seems to cover a multitude of sins.
A well behaved independent module will need to remove all of these
interdependencies. There are a couple of significant problems with leaving them be:

- Other potential users of such a module will not necessarily make
sure that everything is auto-loaded, so a this module would just be broken.
Sinatra comes to mind.
- Interdependencies increase complexity. While complexity is not
inherently bad, it can be a source of bugs and errors, so it ought to
be avoided when possible.

To start with, I moved the scope.rb file and the scope directory
to active_product/lib/auto. And I added the following to the
ActiveProduct module definition in active_product/lib/active_product/engine.rb:

```ruby
module ActiveProduct
  class Engine < Rails::Engine
    config.autoload_paths += %W(#{config.root}/lib/auto)
```

There are two interesting things about this to note:

- The engine lib directory is **not** auto-loaded in
the same way that app/models, app/controllers, etc are. There
apparently is no convention for loading a lib directory. I picked
'lib/auto', but there are not any constraints on what can be added.

- The engine has its own config variable that is loaded and honored
as part of the Rails app config.

### Now What?

Now when I tried to instantiate the class I found that it called a
couple of methods that I’m not quite sure what I am going to do with
yet. These are:

```nohighlight
make_permalink
search_methods
```

**make_permalink** is provided by an interestingly
named Railslove module in the spree_core lib and seems harmless
enough. For now, I commented the call out of the Product lib.

**search_methods** is provided by the
[MetaSearch](https://github.com/activerecord-hackery/meta_search)
plugin which is a Spree dependency. Search is neat, but I’ll sort it
out later. Again, I commented it out and will deal with it if it
causes problems.

### Where are we now

I can now instantiate a new product object from the console. That
seems to somewhat validate the effort to isolate the module. You may
be tempted to ask if you could use that product instance for anything;
saving a copy to the data store, for instance. Here’s a hint:
circular dependencies.

The code that I’ve worked on up till now can be seen [here](https://github.com/sonny/active_product/tree/blog_post_1).
