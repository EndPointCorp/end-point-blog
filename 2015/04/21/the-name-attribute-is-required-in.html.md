---
author: Greg Davidson
gh_issue_number: 1118
tags: chef, devops, sysadmin, vagrant
title: "The `name' attribute is required in cookbook metadata: Solving a Vagrant/Chef Provisioning Issue"
---

## When Vagrant/Chef Provisioning Goes South

I recently ran into the following error when provisioning a new vagrant machine via the `vagrant up` command: 

```
[2015-04-21T17:10:35+00:00] FATAL: Stacktrace dumped to /var/chef/cache/chef-stacktrace.out
[2015-04-21T17:10:35+00:00] ERROR: Cookbook loaded at path(s) [/tmp/vagrant-chef/path/to/my-cookbook] has invalid metadata: The `name' attribute is required in cookbook metadata
[2015-04-21T17:10:35+00:00] FATAL: Chef::Exceptions::ChildConvergeError: Chef run process exited unsuccessfully (exit code 1)
```

After some googling and digging I learned version 12 of chef-client introduced a breaking change. From version 12 on, every cookbook [requires a name attribute in their metadata.rb file](https://docs.chef.io/release/12-0/release_notes.html#metadata-rb-settings). A quick grep through the metadata.rb files in the project revealed several did not include name attributes. You would be correct at this point to suggest I could have added name attributes to the cookbook metadata files and been done with this. However, in this case I was a consumer of the cookbooks and was not involved in maintaining them so an alternate solution was preferable. 

## Selecting a Specific Version of Chef in Vagrant

My idea for a solution was to install the most recent chef-client release prior to   version 12. I was not sure how to do this initially but along the way I learned that   by default, Vagrant will install the most recent release of chef-client. The [Vagrant documentation for Chef   provisioners](http://docs.vagrantup.com/v2/provisioning/chef_common.html) described what I needed to do. The Chef version could be specified   in config.vm.provision block in the Vagrantfile:

```ruby
config.vm.provision :chef_solo do |chef|
      chef.version = "11.18"
      chef.cookbooks_path = "cookbooks"
      chef.data_bags_path = "data_bags"

      # List of recipes to run
      chef.add_recipe "vagrant_main::my_project"
  end
  
```

With this configuration change, chef-client 11.18 completed the provisioning step successfully.
