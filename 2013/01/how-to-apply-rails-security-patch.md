---
author: Brian Buchalter
title: How to Apply a Rails Security Patch
github_issue_number: 754
tags:
- rails
- security
date: 2013-01-29
---

With [the announcement of CVE-2013-0333](https://groups.google.com/forum/?hl=en&fromgroups=#!topic/rubyonrails-security/1h2DR63ViGo), it’s time again to secure your Rails installation. ([Didn’t we just do this?](/blog/2013/01/rails-cve-2013-0156-metasploit)) If you are unable to upgrade to the latest, secure release of Rails, this post will help you apply a Rail security patch, using CVE-2013-0333 as an example.

### Fork Rails, Patch

The CVE-2013-0333 patches so kindly released by [Michael Koziarski](https://twitter.com/nzkoz) are intended for use with folks who have forked the Rails repository. If you are unable to keep up with the latest releases, a forked repo can help you manage divergences and make it easy to apply security patches. Unfortunately, you cannot use wget to download the attached patches directly from Google Groups, so you’ll have to do this in the browser and put the patch into the root of your forked Rails repo. To apply the patch:

```bash
cd $RAILS_FORK_PATH
git checkout $RAILS_VERSION
# Download attachment from announcement in browser, sorry no wget!
git am < $CVE.patch
```

You should see the newly committed patch(es) at the HEAD of your branch. Push out to GitHub and then bundle update rails on your servers.

### Patching without Forks

If you are in the unfortunate case where there have been modifications or patches applied informally outside version control or you are otherwise compelled to modify the Rails source on your server directly, you are still able to use the provided patches.

Before begining, take a look at the diffstat at the top of the patch:

```diff
 .../lib/active_support/json/backends/okjson.rb     |  644 ++++++++++++++++++++
 .../lib/active_support/json/backends/yaml.rb       |   71 +---
 activesupport/lib/active_support/json/decoding.rb  |    2 +-
 activesupport/test/json/decoding_test.rb           |    4 +-
```

As you can see the base path of the diff is “activesupport”. (The triple dots are simply there to truncate the paths so the diffstats line up nicely.) However, when the activesupport gem is installed on your system, the version number is appended in the path. This means we need to use the -p2 argument for [patch](http://linux.die.net/man/1/patch) to “strip the smallest prefix containing *num* leading slashes from each file name found in the patch file.” We’ll see how to do this in just a second, but first, let’s find the source files we need to patch.

### Locating Rails Gems

To find the installed location of your Rails gems, make sure you are using the desired RVM installation@gemset (check with rvm current), and then run “gem env” and look for the “GEM PATHS” section. If you’re using the user-based installation of RVM it might look something like this:

```bash
/home/$USER/.rvm/gems/ree-1.8.7-2012.02
```

Now that we know where the installed gems are, we need to get our patch and apply.

```bash
cd /home/$USER/.rvm/gems/ree-1.8.7-2012.0/gems/activesupport-2.3.15
# Download attachment from announcement in browser, sorry no wget!
patch -p2 < $CVE.patch
```

Often times these patches will include changes to tests which are not included in the ActiveSupport gem installations. You may get an error like this while patching CVE-2013-0333:

```bash
patch -p2 < cve-2013-0333.patch                                                 
patching file lib/active_support/json/backends/okjson.rb
patching file lib/active_support/json/backends/yaml.rb
patching file lib/active_support/json/decoding.rb
can’t find file to patch at input line 768
Perhaps you used the wrong -p or --strip option?
The text leading up to this was:
--------------------------
|diff --git a/activesupport/test/json/decoding_test.rb b/activesupport/test/json/decoding_test.rb
|index e45851e..a7f7b46 100644
|--- a/activesupport/test/json/decoding_test.rb
|+++ b/activesupport/test/json/decoding_test.rb
--------------------------
File to patch: 
Skip this patch? [y] y
Skipping patch.
1 out of 1 hunk ignored
```

This error is just saying it cannot find the file test/json/decoding_test.rb. It’s OK to skip this patch, because the file doesn’t exist to patch.

### Verify the Patch is Installed

When doing any kind of security patching it is essential that you have confidence your actions were applied successfully. The strategies on doing this will verify based on the type of changes made. For CVE-2013-0333, it’s a fairly simple check.

```bash
# Before applying patch
script/console
Loading development environment (Rails 2.3.15)
>> ActiveSupport::JSON::DECODERS
=> ["Yajl", "Yaml"]

# After applying patch
script/console
Loading development environment (Rails 2.3.15)
>> ActiveSupport::JSON::DECODERS
=> ["Yajl", "OkJson"]
```

