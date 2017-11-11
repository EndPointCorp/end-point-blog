---
author: Kamil Ciemniewski
gh_issue_number: 877
tags: ruby, rails
title: Specify versions for your dependencies in your Gemfiles
---



How often have you been too lazy to put a version spec for gems you depended on in your projects? Do you fear updating the gems your app uses in production?

Here is an elusive-obvious tip for you: **Always** specify version numbers for your dependencies in your app's Gemfile.

Version specs should:

- be strict numbers for very fragile gems like Rails

- use the pessimistic operator for others (with ~>)

## Updating apps with versionless Gemfiles is painful

Newer gem versions often break compatibility. That makes updating a disaster if you don't have any restrictions in place for your dependencies.

We should coin a new term in the field of psychology: **Update Anxiety**.

That's precisely the state the vast majority of us is in when proceeding to update dependencies in our projects.

In Rails, having a versionless Gemfile makes clean updates **impossible**.

## Fearing the update makes your app susceptible to bugs

Newer versions of gems are there, not only for delivering new features. The history of changes between different versions mostly show changes related to bug fixes. If you see a gem which mostly delivers new features without fixing bugs - stay **away** from it!

If you do not update the gem set out of fear - you could be missing out on available security updates and bug fixes.

## Fragile gems influence the whole stack

There are some gems that you should update **very** carefully. These updates require planning and consideration before they are applied.

Every Rails application is a stack of components which are built upon others. Rails operate on top of Rack and some middleware. Active Admin operates on top of many others like Active Record or meta search.

Updating components that "live" at the bottom of the stack can influence **every** component above them.

This it the reason you should treat such dependencies with care and specify a static version number like:

```ruby
gem 'rails', '3.2.14'
```

## In "semantic versioning" we trust

Ruby Gem authors strongly advise following the "semantic versioning policy". A versioning policy is just a way of incrementing next version numbers for a project.

You can find a link to more info about this in the links at the bottom of this post.

As per the ruby gems guides "semantic versioning" explains:

*PATCH 0.0.x level changes for implementation level detail changes, such as small bug fixes

MINOR 0.x.0 level changes for any backwards compatible API changes, such as new functionality/features

MAJOR x.0.0 level changes for backwards incompatible API changes, such as changes that will break existing users code if they update*

There is no enforcement of this by RubyGems for gems that are being pushed. Most of gems (if not almost all) follow it quite well though.

### The 'pessimistic operator'

Ever seen the '~>' operator in Gemfiles? It's called pessimistic because it:

- allows for update up to the maximum number of the last specified digit

- disallows any higher

In tandem with the semantic versioning this gives us a possibility to say: "Allow any bug fix for the version 1.2.0 but reject minor changes".

You could specify it by placing:

```ruby
gem 'music-beers-and-unicorns', '~> 1.2.0'
```

This allows you to use

```bash
bundle update
```

Without **that** much fear and hassle.

## More to read

Interested in reading more? Here are some links for you:

[http://guides.rubygems.org/patterns/#semantic_versioning](http://guides.rubygems.org/patterns/#semantic_versioning)

[http://semver.org](http://semver.org)

[http://robots.thoughtbot.com/post/2508037841/rubys-pessimistic-operator](http://robots.thoughtbot.com/post/2508037841/rubys-pessimistic-operator)

[http://robots.thoughtbot.com/post/35717411108/a-healthy-bundle](http://robots.thoughtbot.com/post/35717411108/a-healthy-bundle)

[https://github.com/thoughtbot/guides/tree/master/best-practices#bundler](https://github.com/thoughtbot/guides/tree/master/best-practices#bundler)


