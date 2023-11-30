---
author: Wojtek Ziniewicz
title: Testing your chef repo pull requests with chef-zero, Vagrant and Jenkins
github_issue_number: 1093
tags:
- chef
- devops
- git
- vagrant
date: 2015-02-18
---

All [Liquid Galaxy](https://www.visionport.com/) setups deployed by End Point are managed by [Chef](https://www.chef.io/chef/). Typical deployment consists of approx 3 to 9 Linux boxes from which only 1 is managed and the rest is an ISO booted from this machine via network with copy-on-write root filesystem. Because of this, typical deployment involves more steps than just updating your code and restarting application. Deployment + rollback may be even 10 times longer compared with typical web application. Due to this fact, we need to test our infrastructure extensively.

What are we to do in order to make sure that our infrastructure is **tested** **well** **before it hits production?**

<div class="separator" style="clear: both; text-align: center;">
<br/></div>

Scary? It’s not.

<div class="separator" style="clear: both; text-align: center;">
<a href="/blog/2015/02/testing-your-chef-repo-pull-requests/image-0.png" imageanchor="1" style="margin-left: 1em; margin-right: 1em; text-align: left;"><img border="0" height="550" src="/blog/2015/02/testing-your-chef-repo-pull-requests/image-0.png" width="640"/></a></div>

#### Workflow broken down by pieces

- **lg_chef.git repo**—​where we keep cookbooks, environments and node definitions
- **GitHub pull request**—​artifact of infrastructure source code tested by Jenkins
- **Vagrant**—​virtual environment in which chef is run in order to test the artifact. There’s always 1 master node and few Vagrant boxes that boot an ISO from master via tftp protocol
- **chef-zero**—​Chef flavor used to converge and test the infrastructure on the basis of GitHub pull request
- **chef-server/chef-client**—​Chef flavor used to converge and test production and pre-production environment
- **Jenkins** — Continuous Integration environment that runs the converge process and part of the tests
- **Tests**—​two frameworks used—​[BATS](https://github.com/sstephenson/bats) (for the integration tests on the top) and [minitest](https://github.com/seattlerb/minitest) (for after-converge tests)
- **lg-live-build**—​our fork of [Debian live build](https://www.debian.org/devel/debian-live/) used to build the ISO that is booted by Vagrant slaves

#### Workflow broken down by the order of actions

1. User submits **GitHub pull request** to **lg_chef.git** repo
1. **GitHub pull request** gets picked up by **Jenkins**
1. **Jenkins** creates 1 **master** **Vagrant** node and several slave nodes to act as **slaves**
1. **chef-zero** converges master **Vagrant** box and runs **minitest**
1. **BATS** tests run on the freshly converged **Vagrant master**box. Few steps are performed here: ISO is built, it’s distributed to the slaves, slaves boot the ISO and final integration tests are run to see whether slaves have all the goodness.
1. If points 1 to 5 are **green,**developer merges the changes, uploads the updated cookbooks, node definitions, roles and environments and runs the final tests.

**What didn’t work for us and why**

- [kitchen-vagrant ](https://github.com/test-kitchen/kitchen-vagrant)—​because it didn’t play well with Jenkins (or JVM itself) and didn’t know how to use advanced Vagrant features for specifying multiple networking options, interfaces and drivers. However it supports using your own [Vagrantfile.erb](https://github.com/test-kitchen/kitchen-vagrant/blob/master/templates/Vagrantfile.erb)
- We’ve had some doubts about keeping all the cookbooks, environments and node definitions in one repo because chef-server/chef-client tests can only test your stuff if it’s uploaded to the Chef server, but **chef-zero** came in handy

#### The code

As previously mentioned, we needed our own vagrant template file.

```ruby
Vagrant.configure("2") do |config|
  <% if @data[:chef_type] == "chef_zero" %>
  config.chef_zero.enabled = true
  config.chef_zero.chef_server_url = "<%= @data[:chef_server_url] %>"
  config.chef_zero.roles = "../../roles/"
  config.chef_zero.cookbooks = "../../cookbooks/"
  config.chef_zero.environments = "../../environments/"
  config.chef_zero.data_bags = "../integration/default/data_bags/"
  <% else %>
  config.chef_zero.enabled = false
  <% end %>
  config.omnibus.chef_version = "<%= @data[:chef_version] %>"
  config.vm.define "<%= @data[:headnode][:slug] %>" do |h|
  h.vm.box = "<%= @data[:headnode][:box] %>"
    h.vm.box_url = "<%= @data[:headnode][:box_url] %>"
    h.vm.hostname = "<%= @data[:headnode][:hostname] %>"
    h.vm.network(:private_network, {:ip => '10.42.41.1'})
    h.vm.synced_folder ".", "/vagrant", disabled: true
    h.vm.provider :virtualbox do |p|
      <% @data[:headnode][:customizations].each do |key, value| %>
        p.customize ["modifyvm", :id, "<%= key %>", "<%= value %>"]
      <% end %>
    end
    h.vm.provision :chef_client do |chef|
      <% if @data[:chef_type] == "chef_zero" %>
      chef.environment = "<%= @data[:headnode][:provision][:environment] %>"
      chef.run_list = <%= @data[:run_list] %>
      chef.json = <%= @data[:node_definition] %>
      chef.chef_server_url = "<%= @data[:chef_server_url] %>"
      <% else %>
      chef.chef_server_url = "<%= @data[:headnode][:provision][:chef_server_url] %>"
      <% end %>
      chef.validation_key_path = "<%= @data[:headnode][:provision][:validation_key_path] %>"
      chef.encrypted_data_bag_secret_key_path = "<%= @data[:headnode][:provision][:encrypted_data_bag_secret_key_path] %>"
      chef.verbose_logging = <%= @data[:headnode][:provision][:verbose_logging] %>
      chef.log_level = "<%= @data[:headnode][:provision][:log_level] %>"
  <% end %>
  config.omnibus.chef_version = "<%= @data[:chef_version] %>"
  config.vm.define "<%= @data[:headnode][:slug] %>" do |h|
  h.vm.box = "<%= @data[:headnode][:box] %>"
    h.vm.box_url = "<%= @data[:headnode][:box_url] %>"
    h.vm.hostname = "<%= @data[:headnode][:hostname] %>"
    h.vm.network(:private_network, {:ip => '10.42.41.1'})
    h.vm.synced_folder ".", "/vagrant", disabled: true
    h.vm.provider :virtualbox do |p|
      <% @data[:headnode][:customizations].each do |key, value| %>
        p.customize ["modifyvm", :id, "<%= key %>", "<%= value %>"]
      <% end %>
    end
    h.vm.provision :chef_client do |chef|
      <% if @data[:chef_type] == "chef_zero" %>
      chef.environment = "<%= @data[:headnode][:provision][:environment] %>"
      chef.run_list = <%= @data[:run_list] %>
      chef.json = <%= @data[:node_definition] %>
      chef.chef_server_url = "<%= @data[:chef_server_url] %>"
      <% else %>
      chef.chef_server_url = "<%= @data[:headnode][:provision][:chef_server_url] %>"
      <% end %>
      chef.validation_key_path = "<%= @data[:headnode][:provision][:validation_key_path] %>"
      chef.encrypted_data_bag_secret_key_path = "<%= @data[:headnode][:provision][:encrypted_data_bag_secret_key_path] %>"
      chef.verbose_logging = <%= @data[:headnode][:provision][:verbose_logging] %>
      chef.log_level = "<%= @data[:headnode][:provision][:log_level] %>"
      chef.node_name = "<%= @data[:headnode][:provision][:node_name] %>"
    end
  end

  #display nodes
  <% @data[:display_nodes][:nodes].each do |dn| %>
  config.vm.define "<%= dn[:slug] %>" do |dn_config|
    dn_config.vm.box_url = "<%= @data[:display_nodes][:global][:box_url] %>"
    dn_config.vm.hostname = "<%= dn[:hostname] %>"
    dn_config.vm.box = "<%= @data[:display_nodes][:global][:box] %>"
    dn_config.vm.synced_folder ".", "/vagrant", disabled: true
    dn_config.vm.boot_timeout = 1
    dn_config.vm.provider :virtualbox do |p|
    <% @data[:display_nodes][:global][:customizations].each do |key, value| %>
      p.customize ["modifyvm", :id, "<%= key %>", "<%= value %>"]
    <% end %>
      p.customize ["modifyvm", :id, "--macaddress1", "<%= dn[:mac] %>"]
      p.customize ["createhd", "--filename", "../files/<%= dn[:slug] %>.vmdk", "--size", 80*1024]
      p.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 0, "--device", 0, "--type", "hdd", "--medium", "none"]
      p.customize ["storageattach", :id, "--storagectl", "IDE Controller", "--port", 0, "--device", 0, "--type", "hdd", "--medium", "../files/<%= dn[:slug] %>.vmdk"]
      p.customize ["storagectl", :id, "--name", "SATA Controller", "--add", "sata",  "--controller", "IntelAHCI", "--hostiocache", "on"]
      p.customize ["storageattach", :id, "--storagectl", "SATA Controller", "--port", 1, "--device", 0, "--type", "hdd", "--medium", "../files/ipxe_<%= dn[:slug] %>.vmdk"]
    end
  end
  <% end %>
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

As a result we get an on-the-fly Vagrantfile that’s used during the testing:

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
    h.vm.network(:private_network, {:ip => '10.42.41.1'})
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
      chef.json = {:sysctl=>{:params=>{:vm=>{:swappiness=>20}, :net=>{:ipv4=>{:ip_forward=>1}}}}, :test_mode=>true, :call_ep=>{:keyname=>"ProjectX CI Production", :fwdport=>33299}, :tftproot=>{:managed=>true}, :tags=>[], :lg_cms=>{:remote=>"github"}, :monitor=>true, :lg_grub=>{:cmdline=>"nomodeset biosdevname=0"}, :projectX=>{:repo_branch=>"development", :display_host=>"42-a", :kiosk_host=>"42-b", :sensors_host=>"42-b", :maps_url=>"https://www.google.com/maps/@8.135687,-75.0973243,17856994a,40.4y,1.23h/data=!3m1!1e3?esrch=Tactile::TactileAcme,Tactile::ImmersiveModeEnabled"}, :liquid_galaxy=>{:touchscreen_link=>"/dev/input/lg_active_touch", :screenshotd=>{:screen_rows=>"1", :screen_columns=>"1"}, :screenshot_service=>true, :display_nodes=>[{:hostname=>"42-c"}, {:allowed_pages=>["Google Maps", "Pacman Doodle", "jellyfish", "Doodle Selection", "ProjectX Video Player", "Composer kiosk"], :hostname=>"42-b", :mac=>"5c:a1:ab:1e:00:02", :features=>"mandatory_windows, plain_gray, starry_skies", :bad_windows_names=>"Google Earth - Login Status", :mandatory_windows_names=>"awesome", :screens=>[{:display=>":0", :crtc=>"default", :grid_order=>"0"}], :screen_rotation=>"normal", :audio_device=>"{type hw; card DGX; device 0}", :onboard_enable=>true, :keyboard_enable=>true, :mouse_enable=>true, :cursor_enable=>true, :background_extension=>"jpg", :background_mode=>"zoom-fill", :projectX=>{:extensions=>{:kiosk=>"ProjectX Kiosk", :google_properties_menu=>"Google Properties Menu", :onboard=>"Onboard", :no_right_click=>"Right Click Killer", :render_statistics=>"Render Statistics"}, :browser_slug=>"lgS0", :urls=>"https://www.google.com/maps", :ros_nodes=>[{:name=>"rfreceiver_reset", :pkg=>"rfreceiver", :type=>"kill_browser.py"}, {:name=>"proximity", :pkg=>"maxbotix", :type=>"sender.py"}, {:name=>"spacenav", :pkg=>"spacenav_node", :type=>"spacenav_node"}, {:name=>"leap", :pkg=>"leap_motion", :type=>"sender.py"}, {:name=>"projectX_nav", :pkg=>"projectX_nav", :type=>"projectX_nav"}, {:name=>"onboard", :pkg=>"onboard", :type=>"listener.py"}, {:name=>"rosbridge", :pkg=>"rosbridge_server", :type=>"rosbridge_websocket", :params=>[{:name=>"certfile", :value=>"/home/lg/etc/ros.crt"}, {:name=>"keyfile", :value=>"/home/lg/etc/ros.key"}]}]}, :browser_infinite_url=>"http://lg-head/projectX-loader.html"}, {:hostname=>"42-a", :mac=>"5c:a1:ab:1e:00:01", :features=>"mandatory_windows, plain_gray, starry_skies, erroneous_text", :bad_windows_names=>"Google Earth - Login Status", :mandatory_windows_names=>"awesome", :screens=>[{:display=>":0", :crtc=>"default", :grid_order=>"1"}], :keyboard_enable=>true, :mouse_enable=>true, :cursor_enable=>true, :background_extension=>"jpg", :background_mode=>"zoom-fill", :nvidia_mosaic=>true, :manual_layout=>{:default=>"1024x768+0+0"}, :projectX=>{:extensions=>{:display=>"ProjectX Large Display", :pacman=>"pacman", :render_statistics=>"Render Statistics"}, :browser_slug=>"lgS0", :urls=>"https://www.google.com/maps", :ros_nodes=>[{:name=>"geodata", :pkg=>"geodata", :type=>"geodata_server.py"}]}, :browser_infinite_url=>"http://lg-head/projectX-loader.html", :default_browser_bin=>"google-chrome", :allowed_pages=>["Google Maps", "Pacman Doodle", "jellyfish", "ProjectX Video Player", "Composer wall"]}], :has_cec=>false, :google_office=>false, :viewsync_master=>"42-b", :has_touchscreen=>false, :has_spacenav=>true, :support_name=>"projectX-ci", :podium_interface=>"http://lg-head", :podium_display=>"42-b:default"}}
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

echo "Not managing knife client because => chef_zero "
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

Elapsed time—​between 40 and 50 minutes.
