---
author: Matt Vollrath
title: Deploying password files with Chef
github_issue_number: 774
tags:
- automation
- chef
- devops
- hosting
date: 2013-04-03
---



Today I worked on a Chef recipe that needed to deploy an rsync password file from an encrypted data bag.  Obtaining the password from the data bag in the recipe is well documented, but I knew that great care should be taken when writing the file.  There are a plethora of ways to write strings to files in Chef, but many have potential vulnerabilities when dealing with secrets.  Caveats:

- The details of execute resources may be gleaned from globally-visible areas of proc.
- The contents of a template may be echoed to the chef client.log or stored in cache, stacktrace or backup areas.
- Some chef resources which write to files can be made to dump the diff or contents to stdout when run with verbosity.

With tremendous help from [Jay Feldblum](https://github.com/yfeldblum) in freenode#chef, we came up with a safe, optimized solution to deploy the password from a series of ruby blocks:

```ruby
pw_path = Pathname("/path/to/pwd/file")
pw_path_uid = 0
pw_path_gid = 0
pw = Chef::EncryptedDataBagItem.load("bag", "item")['password']

ruby_block "#{pw_path}-touch" do
  block   { FileUtils.touch pw_path } # so that we can chown & chmod it before writing the pw to it
  not_if  { pw_path.file? }
end

ruby_block "#{pw_path}-chown" do
  block   { FileUtils.chown pw_path_uid, pw_path_gid, pw_path }
  not_if  { s = pw_path.stat ; s.uid == pw_path_uid && s.gid == pw_path_gid }
end

ruby_block "#{pw_path}-chmod" do
  block   { FileUtils.chmod 0600, pw_path }
  not_if  { s = pw_path.stat ; "%o" % s.mode == "100600" }
end

ruby_block "#{pw_path}-content" do
  block   { pw_path.open("w") {|f| f.write pw} }
  not_if  { pw_path.read == pw } # NOTE: a secure compare method might make this even better
end
```

Further reading:

- [Chef: Encrypted Data Bags](https://docs.opscode.com/essentials_data_bags_encrypt.html)
- [Chef: Ruby Blocks](https://docs.opscode.com/resource_ruby_block.html)
- [Ruby: File Methods](https://www.ruby-doc.org/core-2.0/File.html)


