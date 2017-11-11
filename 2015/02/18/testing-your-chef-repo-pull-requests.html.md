---
author: Wojtek Ziniewicz
gh_issue_number: 1093
tags: chef, devops, git, vagrant
title: Testing your chef repo pull requests with chef-zero, Vagrant and Jenkins
---

All [Liquid Galaxy](https://liquidgalaxy.endpoint.com/) setups deployed by End Point are managed by [Chef](https://www.chef.io/chef/). Typical deployment consists of approx 3 to 9 Linux boxes from which only 1 is managed and the rest is an ISO booted from this machine via network with copy-on-write root filesystem. Because of this, typical deployment involves more steps than just updating your code and restarting application. Deployment + rollback may be even 10 times longer compared with typical web application. Due to this fact, we need to test our infrastructure extensively.

What are we to do in order to make sure that our infrastructure is **tested** **well** **before it hits production?**

<div class="separator" style="clear: both; text-align: center;">
<br/></div>

Scary? - It's not.

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/02/18/testing-your-chef-repo-pull-requests/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em; text-align: left;"><img border="0" height="550" src="/blog/2015/02/18/testing-your-chef-repo-pull-requests/image-0.png" width="640"/></a></div>

#### Workflow broken down by pieces

- **lg_chef.git repo** - where we keep cookbooks, environments and node definitions
- **GitHub pull request** - artifact of infrastructure source code tested by Jenkins
- **Vagrant** - virtual environment in which chef is run in order to test the artifact. There's always 1 master node and few Vagrant boxes that boot an ISO from master via tftp protocol
- **chef-zero** - Chef flavor used to converge and test the infrastructure on the basis of GitHub pull request
- **chef-server/chef-client**- Chef flavor used to converge and test production and pre-production environment
- **Jenkins** - Continuous Integration environment that runs the converge process and part of the tests
- **Tests -**two frameworks used - [BATS](https://github.com/sstephenson/bats) (for the integration tests on the top) and [minitest](https://github.com/seattlerb/minitest) (for after-converge tests)
- **lg-live-build -**our fork of [Debian live build](http://live.debian.net/devel/live-build/) used to build the ISO that is booted by Vagrant slaves

#### Workflow broken down by the order of actions

1. User submits **GitHub pull request** to **lg_chef.git** repo
1. **GitHub pull request** gets picked up by **Jenkins**
1. **Jenkins** creates 1 **master** **Vagrant** node and several slave nodes to act as **slaves**
1. **chef-zero** converges master **Vagrant** box and runs **minitest**
1. **BATS** tests run on the freshly converged **Vagrant master**box. Few steps are performed here: ISO is built, it's distributed to the slaves, slaves boot the ISO and final integration tests are run to see whether slaves have all the goodness.
1. If points 1 to 5 are **green,**developer merges the changes, uploads the updated cookbooks, node definitions, roles and environments and runs the final tests.

**What didn't work for us and why**

- [kitchen-vagrant ](https://github.com/test-kitchen/kitchen-vagrant) - because it didn't play well with Jenkins (or JVM itself) and didn't know how to use advanced Vagrant features for specifying multiple networking options, interfaces and drivers. However it supports using your own [Vagrantfile.erb](https://github.com/test-kitchen/kitchen-vagrant/blob/master/templates/Vagrantfile.erb)
- We've had some doubts about keeping all the cookbooks, environments and node definitions in one repo because chef-server/chef-client tests can only test your stuff if it's uploaded to the Chef server, but **chef-zero** came in handy

#### The code

As previously mentioned, we needed our own vagrant template file.

```ruby
Vagrant.configure("2") do |config|
  &lt;% if @data[:chef_type] == "chef_zero" %&gt;
  config.chef_zero.enabled = true
  config.chef_zero.chef_server_url = "&lt;%= @data[:chef_server_url] %&gt;"
  config.chef_zero.roles = "../../roles/"
  config.chef_zero.cookbooks = "../../cookbooks/"
  config.chef_zero.environments = "../../environments/"
  config.chef_zero.data_bags = "../integration/default/data_bags/"
  &lt;% else %&gt;
  config.chef_zero.enabled = false
  &lt;% end %&gt;
  config.omnibus.chef_version = "&lt;%= @data[:chef_version] %&gt;"
  config.vm.define "&lt;%= @data[:headnode][:slug] %&gt;" do |h|
  h.vm.box = "&lt;%= @data[:headnode][:box] %&gt;"
    h.vm.box_url = "&lt;%= @data[:headnode][:box_url] %&gt;"
    h.vm.hostname = "&lt;%= @data[:headnode][:hostname] %&gt;"
    h.vm.network(:private_network, {:ip =&gt; '10.42.41.1'})
    h.vm.synced_folder ".", "/vagrant", disabled: true
    h.vm.provider :virtualbox do |p|
      &lt;% @data[:headnode][:customizations].each do |key, value| %&gt;
        p.customize ["modifyvm", :id, "&lt;%= key %&gt;", "&lt;%= value %&gt;"]
      &lt;% end %&gt;
    end
    h.vm.provision :chef_client do |chef|
      &lt;% if @data[:chef_type] == "chef_zero" %&gt;
      chef.environment = "&lt;%= @data[:headnode][:provision][:environment] %&gt;"
      chef.run_list = &lt;%= @data[:run_list] %&gt;
      chef.json = &lt;%= @data[:node_definition] %&gt;
      chef.chef_server_url = "&lt;%= @data[:chef_server_url] %&gt;"
      &lt;% else %&gt;
      chef.chef_server_url = "&lt;%= @data[:headnode][:provision][:chef_server_url] %&gt;"
      &lt;% end %&gt;
      chef.validation_key_path = "&lt;%= @data[:headnode][:provision][:validation_key_path] %&gt;"
      chef.encrypted_data_bag_secret_key_path = "&lt;%= @data[:headnode][:provision][:encrypted_data_bag_secret_key_path] %&gt;"
      chef.verbose_logging = &lt;%= @data[:headnode][:provision][:verbose_logging] %&gt;
      chef.log_level = "&lt;%= @data[:headnode][:provision][:log_level] %&gt;"
  &lt;% end %&gt;
  config.omnibus.chef_version = "&lt;%= @data[:chef_version] %&gt;"
  config.vm.define "&lt;%= @data[:headnode][:slug] %&gt;" do |h|
  h.vm.box = "&lt;%= @data[:headnode][:box] %&gt;"
    h.vm.box_url = "&lt;%= @data[:headnode][:box_url] %&gt;"
    h.vm.hostname = "&lt;%= @data[:headnode][:hostname] %&gt;"
    h.vm.network(:private_network, {:ip =&gt; '10.42.41.1'})
    h.vm.synced_folder ".", "/vagrant", disabled: true
    h.vm.provider :virtualbox do |p|
      &lt;% @data[:headnode][:customizations].each do |key, value| %&gt;
        p.customize ["modifyvm", :id, "&lt;%= key %&gt;", "&lt;%= value %&gt;"]
      &lt;% end %&gt;
    end
    h.vm.provision :chef_client do |chef|
      &lt;% if @data[:chef_type] == "chef_zero" %&gt;
      chef.environment = "&lt;%= @data[:headnode][:provision][:environment] %&gt;"
      chef.run_list = &lt;%= @data[:run_list] %&gt;
      chef.json = &lt;%= @data[:node_definition] %&gt;
      chef.chef_server_url = "&lt;%= @data[:chef_server_url] %&gt;"
      &lt;% else %&gt;
      chef.chef_server_url = "&lt;%= @data[:headnode][:provision][:chef_server_url] %&gt;"
      &lt;% end %&gt;
      chef.validation_key_path = "&lt;%= @data[:headnode][:provision][:validation_key_path] %&gt;"
      chef.encrypted_data_bag_secret_key_path = "&lt;%= @data[:headnode][:provision][:encrypted_data_bag_secret_key_path] %&gt;"
      chef.verbose_logging = &lt;%= @data[:headnode][:provision][:verbose_logging] %&gt;
      chef.log_level = "&lt;%= @data[:headnode][:provision][:log_level] %&gt;"
      chef.node_name = "&lt;%= @data[:headnode][:provision][:node_name] %&gt;"
    end
  end

  #display nodes
  &lt;% @data[:display_nodes][:nodes].each do |dn| %&gt;
  config.vm.define "&lt;%= dn[:slug] %&gt;" do |dn_config|
    dn_config.vm.box_url = "&lt;%= @data[:display_nodes][:global][:box_url] %&gt;"
    dn_config.vm.hostname = "&lt;%= dn[:hostname] %&gt;"
    dn_config.vm.box = "&lt;%= @data[:display_nodes][:global][:box] %&gt;"
    dn_config.vm.synced_folder ".", "/vagrant", disabled: true
    dn_config.vm.boot_timeout = 1
    dn_config.vm.provider :virtualbox do |p|
    &lt;% @data[:display_nodes][:global][:customizations].each do |key, value| %&gt;
      p.customize ["modifyvm", :id, "&lt;%= key %&gt;", "&lt;%= value %&gt;"]
    &lt;% end %&gt;
      p.customize ["modifyvm", :id, "--macaddress1", "&lt;%= dn[:mac] %&gt;"]
      p.customize ["createhd", "--filename", "../files/&lt;%= dn[:slug] %&gt;.vmdk", "--size", 80*1024]
      p.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 0, "--device", 0, "--type", "hdd", "--medium", "none"]
      p.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 0, "--device", 0, "--type", "hdd", "--medium", "../files/&lt;%= dn[:slug] %&gt;.vmdk"]
      p.customize ["storagectl", :id, "--name", "SATA Controller", "--add", "sata",  "--controller", "IntelAHCI", "--hostiocache", "on"]
      p.customize ["storageattach", :id, "--storagectl", "SATA Controller", "--port", 1, "--device", 0, "--type", "hdd", "--medium", "../files/ipxe_&lt;%= dn[:slug] %&gt;.vmdk"]
    end
  end
  &lt;% end %&gt;
end
```

It renders a Vagrant File out of following data:

```javascript
{
  "description" : "This file is used to generate Vagrantfile and run_test.sh and also run tests. It should contain _all_ data needed to render the templates and run teh tests.",
  "chef_version" : "11.12.4",
  "chef_type" : "chef_zero",
  "vagrant_template_file" : "vagrantfile.erb",
  "run_tests_template_file" : "run_tests.sh.erb",
  "chef_server_url" : "http://192.168.1.2:4000",
  "headnode" :
    {
    "slug" : "projectX-pull-requests",
    "box" : "opscode-ubuntu-14.04",
    "box_url" : "https://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-14.04_chef-provisionerless.box",
    "hostname" : "lg-head",
    "bats_tests_dir" : "projectX-pr",
    "customizations" : {
      "--memory" : "2048",
      "--cpus": "2",
      "--nic1" : "nat",
      "--nic2": "intnet",
      "--nic3": "none",
      "--nic4" : "none",
      "--nictype1": "Am79C970A",
      "--nictype2": "Am79C970A",
      "--intnet2": "projectX-pull-requests"
    },
    "provision" : {
      "chef_server_url" : "https://chefserver.ourdomain.com:40443",
      "validation_key_path" : "~/.chef/validation.pem",
      "encrypted_data_bag_secret_key_path" : "~/.chef/encrypted_data_bag_secret",
      "node_name" : "lg-head-projectXtest.liquid.glx",
      "environment" : "pull_requests",
      "verbose_logging" : true,
      "log_level" : "info"
    }
  },
  "display_nodes" : {
    "global" : {
      "box" : "opscode-ubuntu-14.04",
      "box_url" : "https://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-14.04_chef-provisionerless.box",
      "customizations" : {
        "--memory" : "2048",
        "--cpus" : "1",
        "--boot1" : "floppy",
        "--boot2" : "net",
        "--boot3" : "none",
        "--boot4" : "none"
    },
    "provision" : {
      "chef_server_url" : "https://chefserver.ourdomain.com:40443",
      "validation_key_path" : "~/.chef/validation.pem",
      "encrypted_data_bag_secret_key_path" : "~/.chef/encrypted_data_bag_secret",
      "node_name" : "lg-head-projectXtest.liquid.glx",
      "environment" : "pull_requests",
      "verbose_logging" : true,
      "log_level" : "info"
    }
  },
  "display_nodes" : {
    "global" : {
      "box" : "opscode-ubuntu-14.04",
      "box_url" : "https://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-14.04_chef-provisionerless.box",
      "customizations" : {
        "--memory" : "2048",
        "--cpus" : "1",
        "--boot1" : "floppy",
        "--boot2" : "net",
        "--boot3" : "none",
        "--boot4" : "none",
        "--intnet1" : "projectX-pull-requests",
        "--nicpromisc1": "allow-all",
        "--nic1" : "intnet",
        "--nic2": "none",
        "--nic3": "none",
        "--nic4": "none",
        "--nictype1": "Am79C970A",
        "--ioapic": "on"
      }
    },
    "nodes" : [
      {
      "slug" : "projectX-pull-requests-kiosk",
      "hostname" : "kiosk",
      "mac" : "5ca1ab1e0001"
    },
    {
      "slug" : "projectX-pull-requests-display",
      "hostname" : "display",
      "mac" : "5ca1ab1e0002"
    }
    ]
  }
}
```

As a result we get an on-the-fly Vagrantfile that's used during the testing:

```javascript
Vagrant.configure("2") do |config|

  config.chef_zero.enabled = true
  config.chef_zero.chef_server_url = "http://192.168.1.2:4000"
  config.chef_zero.roles = "../../roles/"
  config.chef_zero.cookbooks = "../../cookbooks/"
  config.chef_zero.environments = "../../environments/"
  config.chef_zero.data_bags = "../integration/default/data_bags/"

  config.omnibus.chef_version = "11.12.4"
  config.vm.define "projectX-pull-requests" do |h|
  h.vm.box = "opscode-ubuntu-14.04"
    h.vm.box_url = "https://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-14.04_chef-provisionerless.box"
    h.vm.hostname = "lg-head"
    h.vm.network(:private_network, {:ip =&gt; '10.42.41.1'})
    h.vm.synced_folder ".", "/vagrant", disabled: true
    h.vm.provider :virtualbox do |p|
        p.customize ["modifyvm", :id, "--memory", "2048"]
        p.customize ["modifyvm", :id, "--cpus", "2"]
        p.customize ["modifyvm", :id, "--nic1", "nat"]
        p.customize ["modifyvm", :id, "--nic2", "intnet"]
        p.customize ["modifyvm", :id, "--nic3", "none"]
        p.customize ["modifyvm", :id, "--nic4", "none"]
        p.customize ["modifyvm", :id, "--nictype1", "Am79C970A"]
        p.customize ["modifyvm", :id, "--nictype2", "Am79C970A"]
        p.customize ["modifyvm", :id, "--intnet2", "projectX-pull-requests"]
    end
    h.vm.provision :chef_client do |chef|

      chef.environment = "pull_requests"
      chef.run_list = ["role[lg-head-nocms]", "recipe[lg_live_build]", "recipe[lg_tftproot]", "recipe[lg_projectX]", "recipe[lg_test]", "recipe[test_mode::bats]", "recipe[hostsfile::projectX]"]
      chef.json = {:sysctl=&gt;{:params=&gt;{:vm=&gt;{:swappiness=&gt;20}, :net=&gt;{:ipv4=&gt;{:ip_forward=&gt;1}}}}, :test_mode=&gt;true, :call_ep=&gt;{:keyname=&gt;"ProjectX CI Production", :fwdport=&gt;33299}, :tftproot=&gt;{:managed=&gt;true}, :tags=&gt;[], :lg_cms=&gt;{:remote=&gt;"github"}, :monitor=&gt;true, :lg_grub=&gt;{:cmdline=&gt;"nomodeset biosdevname=0"}, :projectX=&gt;{:repo_branch=&gt;"development", :display_host=&gt;"42-a", :kiosk_host=&gt;"42-b", :sensors_host=&gt;"42-b", :maps_url=&gt;"https://www.google.com/maps/@8.135687,-75.0973243,17856994a,40.4y,1.23h/data=!3m1!1e3?esrch=Tactile::TactileAcme,Tactile::ImmersiveModeEnabled"}, :liquid_galaxy=&gt;{:touchscreen_link=&gt;"/dev/input/lg_active_touch", :screenshotd=&gt;{:screen_rows=&gt;"1", :screen_columns=&gt;"1"}, :screenshot_service=&gt;true, :display_nodes=&gt;[{:hostname=&gt;"42-c"}, {:allowed_pages=&gt;["Google Maps", "Pacman Doodle", "jellyfish", "Doodle Selection", "ProjectX Video Player", "Composer kiosk"], :hostname=&gt;"42-b", :mac=&gt;"5c:a1:ab:1e:00:02", :features=&gt;"mandatory_windows, plain_gray, starry_skies", :bad_windows_names=&gt;"Google Earth - Login Status", :mandatory_windows_names=&gt;"awesome", :screens=&gt;[{:display=&gt;":0", :crtc=&gt;"default", :grid_order=&gt;"0"}], :screen_rotation=&gt;"normal", :audio_device=&gt;"{type hw; card DGX; device 0}", :onboard_enable=&gt;true, :keyboard_enable=&gt;true, :mouse_enable=&gt;true, :cursor_enable=&gt;true, :background_extension=&gt;"jpg", :background_mode=&gt;"zoom-fill", :projectX=&gt;{:extensions=&gt;{:kiosk=&gt;"ProjectX Kiosk", :google_properties_menu=&gt;"Google Properties Menu", :onboard=&gt;"Onboard", :no_right_click=&gt;"Right Click Killer", :render_statistics=&gt;"Render Statistics"}, :browser_slug=&gt;"lgS0", :urls=&gt;"https://www.google.com/maps", :ros_nodes=&gt;[{:name=&gt;"rfreceiver_reset", :pkg=&gt;"rfreceiver", :type=&gt;"kill_browser.py"}, {:name=&gt;"proximity", :pkg=&gt;"maxbotix", :type=&gt;"sender.py"}, {:name=&gt;"spacenav", :pkg=&gt;"spacenav_node", :type=&gt;"spacenav_node"}, {:name=&gt;"leap", :pkg=&gt;"leap_motion", :type=&gt;"sender.py"}, {:name=&gt;"projectX_nav", :pkg=&gt;"projectX_nav", :type=&gt;"projectX_nav"}, {:name=&gt;"onboard", :pkg=&gt;"onboard", :type=&gt;"listener.py"}, {:name=&gt;"rosbridge", :pkg=&gt;"rosbridge_server", :type=&gt;"rosbridge_websocket", :params=&gt;[{:name=&gt;"certfile", :value=&gt;"/home/lg/etc/ros.crt"}, {:name=&gt;"keyfile", :value=&gt;"/home/lg/etc/ros.key"}]}]}, :browser_infinite_url=&gt;"http://lg-head/projectX-loader.html"}, {:hostname=&gt;"42-a", :mac=&gt;"5c:a1:ab:1e:00:01", :features=&gt;"mandatory_windows, plain_gray, starry_skies, erroneous_text", :bad_windows_names=&gt;"Google Earth - Login Status", :mandatory_windows_names=&gt;"awesome", :screens=&gt;[{:display=&gt;":0", :crtc=&gt;"default", :grid_order=&gt;"1"}], :keyboard_enable=&gt;true, :mouse_enable=&gt;true, :cursor_enable=&gt;true, :background_extension=&gt;"jpg", :background_mode=&gt;"zoom-fill", :nvidia_mosaic=&gt;true, :manual_layout=&gt;{:default=&gt;"1024x768+0+0"}, :projectX=&gt;{:extensions=&gt;{:display=&gt;"ProjectX Large Display", :pacman=&gt;"pacman", :render_statistics=&gt;"Render Statistics"}, :browser_slug=&gt;"lgS0", :urls=&gt;"https://www.google.com/maps", :ros_nodes=&gt;[{:name=&gt;"geodata", :pkg=&gt;"geodata", :type=&gt;"geodata_server.py"}]}, :browser_infinite_url=&gt;"http://lg-head/projectX-loader.html", :default_browser_bin=&gt;"google-chrome", :allowed_pages=&gt;["Google Maps", "Pacman Doodle", "jellyfish", "ProjectX Video Player", "Composer wall"]}], :has_cec=&gt;false, :google_office=&gt;false, :viewsync_master=&gt;"42-b", :has_touchscreen=&gt;false, :has_spacenav=&gt;true, :support_name=&gt;"projectX-ci", :podium_interface=&gt;"http://lg-head", :podium_display=&gt;"42-b:default"}}
      chef.chef_server_url = "http://192.168.1.2:4000"

      chef.validation_key_path = "~/.chef/validation.pem"
      chef.encrypted_data_bag_secret_key_path = "~/.chef/encrypted_data_bag_secret"
      chef.verbose_logging = true
      chef.log_level = "info"
      chef.node_name = "lg-head-projectXtest.liquid.glx"
    end
  end

  #display nodes

  config.vm.define "projectX-pull-requests-kiosk" do |dn_config|
    dn_config.vm.box_url = "https://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-14.04_chef-provisionerless.box"
    dn_config.vm.hostname = "kiosk"
    dn_config.vm.box = "opscode-ubuntu-14.04"
    dn_config.vm.synced_folder ".", "/vagrant", disabled: true
    dn_config.vm.boot_timeout = 1
    dn_config.vm.provider :virtualbox do |p|
      p.customize ["modifyvm", :id, "--memory", "2048"]
      p.customize ["modifyvm", :id, "--cpus", "1"]
      p.customize ["modifyvm", :id, "--boot1", "floppy"]
      p.customize ["modifyvm", :id, "--boot2", "net"]
      p.customize ["modifyvm", :id, "--boot3", "none"]
      p.customize ["modifyvm", :id, "--boot4", "none"]
      p.customize ["modifyvm", :id, "--intnet1", "projectX-pull-requests"]
      p.customize ["modifyvm", :id, "--nicpromisc1", "allow-all"]
      p.customize ["modifyvm", :id, "--nic1", "intnet"]
      p.customize ["modifyvm", :id, "--nic2", "none"]
      p.customize ["modifyvm", :id, "--nic3", "none"]
      p.customize ["modifyvm", :id, "--nic4", "none"]
      p.customize ["modifyvm", :id, "--nictype1", "Am79C970A"]
      p.customize ["modifyvm", :id, "--ioapic", "on"]
      p.customize ["modifyvm", :id, "--macaddress1", "5ca1ab1e0001"]
      p.customize ["createhd", "--filename", "../files/projectX-pull-requests-kiosk.vmdk", "--size", 80*1024]
      p.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 0, "--device", 0, "--type", "hdd", "--medium", "none"]
      p.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 0, "--device", 0, "--type", "hdd", "--medium", "../files/projectX-pull-requests-kiosk.vmdk"]
      p.customize ["storagectl", :id, "--name", "SATA Controller", "--add", "sata",  "--controller", "IntelAHCI", "--hostiocache", "on"]
      p.customize ["storageattach", :id, "--storagectl", "SATA Controller", "--port", 1, "--device", 0, "--type", "hdd", "--medium", "../files/ipxe_projectX-pull-requests-kiosk.vmdk"]
    end
  end

  config.vm.define "projectX-pull-requests-display" do |dn_config|
    dn_config.vm.box_url = "https://opscode-vm-bento.s3.amazonaws.com/vagrant/virtualbox/opscode_ubuntu-14.04_chef-provisionerless.box"
    dn_config.vm.hostname = "display"
    dn_config.vm.box = "opscode-ubuntu-14.04"
    dn_config.vm.synced_folder ".", "/vagrant", disabled: true
    dn_config.vm.boot_timeout = 1
    dn_config.vm.provider :virtualbox do |p|
      p.customize ["modifyvm", :id, "--memory", "2048"]
      p.customize ["modifyvm", :id, "--cpus", "1"]
      p.customize ["modifyvm", :id, "--boot1", "floppy"]
      p.customize ["modifyvm", :id, "--boot2", "net"]
      p.customize ["modifyvm", :id, "--boot3", "none"]
      p.customize ["modifyvm", :id, "--boot4", "none"]
      p.customize ["modifyvm", :id, "--intnet1", "projectX-pull-requests"]
      p.customize ["modifyvm", :id, "--nicpromisc1", "allow-all"]
      p.customize ["modifyvm", :id, "--nic1", "intnet"]
      p.customize ["modifyvm", :id, "--nic2", "none"]
      p.customize ["modifyvm", :id, "--nic3", "none"]
      p.customize ["modifyvm", :id, "--nic4", "none"]
      p.customize ["modifyvm", :id, "--nictype1", "Am79C970A"]
      p.customize ["modifyvm", :id, "--ioapic", "on"]
      p.customize ["modifyvm", :id, "--macaddress1", "5ca1ab1e0002"]
      p.customize ["createhd", "--filename", "../files/projectX-pull-requests-display.vmdk", "--size", 80*1024]
      p.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 0, "--device", 0, "--type", "hdd", "--medium", "none"]
      p.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 0, "--device", 0, "--type", "hdd", "--medium", "../files/projectX-pull-requests-display.vmdk"]
      p.customize ["storagectl", :id, "--name", "SATA Controller", "--add", "sata",  "--controller", "IntelAHCI", "--hostiocache", "on"]
      p.customize ["storageattach", :id, "--storagectl", "SATA Controller", "--port", 1, "--device", 0, "--type", "hdd", "--medium", "../files/ipxe_projectX-pull-requests-display.vmdk"]
    end
  end

end
```

Finally we have the environment stored in one Vagrantfile. The missing part is to how to run tests on it.

The testing script does the following:

```shell
#/bin/bash
set -e
# FUNCTIONS

function halt_vm () {
  vms=`vboxmanage list vms | grep "vagrant_$1_" | awk {'print $1'} | sed s/'"'//g`
  echo "Stopping VM $vms"
  stop_result=$(for vm in $vms ; do vboxmanage controlvm $vm poweroff; echo $?; done)
  echo "Output of stopping VM $1 : $stop_result"
}

function boot_vm () {
  vms=`vboxmanage list vms | grep "vagrant_$1_" | awk {'print $1'} | sed s/'"'//g`
  echo "Booting VM $vms"
  start_result=$(for vm in $vms ; do vboxmanage startvm $vm --type headless; echo $?; done)
  echo "Output of booting VM $1 : $start_result"
  echo "Sleeping additional 15 secs after peacefull boot"
  sleep 15
}

function add_keys () {
  for i in `find /var/lib/jenkins/.ssh/id_rsa* | grep -v '.pub'` ; do ssh-add $i ; done
}

#vars

knifeclient_name=lg-head-projectXtest.liquid.glx
headnode_name=projectX-pull-requests

# TEST SCENARIO

cd test/vagrant

# teardown of previous sessions
vagrant destroy projectX-pull-requests-kiosk -f
vagrant destroy projectX-pull-requests-display -f
vagrant destroy $headnode_name -f

echo "Not managing knife client because =&gt; chef_zero "
echo "All ssh keys presented below"
ssh-add -l

# headnode
vagrant up ${headnode_name}

# displaynodes

result=$(vboxmanage convertfromraw ../files/ipxe.usb ../files/ipxe_projectX-pull-requests-kiosk.vmdk --format=VMDK ; vagrant up projectX-pull-requests-kiosk; echo $?)
echo "projectX-pull-requests-kiosk : $result"

result=$(vboxmanage convertfromraw ../files/ipxe.usb ../files/ipxe_projectX-pull-requests-display.vmdk --format=VMDK ; vagrant up projectX-pull-requests-display; echo $?)
echo "projectX-pull-requests-display : $result"

# test phase
OPTIONS=`vagrant ssh-config  ${headnode_name} | grep -v ${headnode_name} | awk -v ORS=' ' '{print "-o " $1 "=" $2}'`
scp ${OPTIONS} ../integration/projectX-pr/bats/*.bats vagrant@${headnode_name}:/tmp/bats_tests

ssh ${OPTIONS} ${headnode_name} '/usr/local/bin/bats /tmp/bats_tests/pre_build_checks.bats'

halt_vm projectX-pull-requests-kiosk
halt_vm projectX-pull-requests-display

echo "Building teh ISO (it may take a long time)"
ssh ${OPTIONS} ${headnode_name} '/usr/local/bin/bats /tmp/bats_tests/build_iso.bats'

ssh ${OPTIONS} ${headnode_name} '/usr/local/bin/bats /tmp/bats_tests/set_grub_to_make_partitions.bats'

echo "Booting nodes"

boot_vm projectX-pull-requests-kiosk
boot_vm projectX-pull-requests-display

echo "Sleeping 30 secs for the DNS to boot and setting the grub to boot the ISO"
sleep 30

ssh ${OPTIONS} ${headnode_name} '/usr/local/bin/bats /tmp/bats_tests/set_grub_to_boot_the_iso.bats'
echo "Sleeping for 4 mins for the displaynodes to boot fresh ISO"
sleep 240

echo "Running the tests inside the headnode:"

ssh ${OPTIONS} ${headnode_name} '/usr/local/bin/bats /tmp/bats_tests/post_checks.bats'
```

So finally we get the following pipeline:

1. Clone Chef pull request from GitHub
1. Create Vagrantfile on the basis of Vagrantfile template
1. Create run_tests.sh script for running the tests
1. Destroy all previously created Vagrant boxes
1. Create one Chef Vagrant box
1. Create ISO Vagrant boxes with ipxe bootloader
1. Converge the Vagrant box with Chef
1. Copy BATS tests onto the headnode
1. Run initial BATS tests that build an ISO
1. Boot display nodes with the newly created ISO
1. Run final integration tests on the stack

Elapsed time - between 40 and 50 minutes.


