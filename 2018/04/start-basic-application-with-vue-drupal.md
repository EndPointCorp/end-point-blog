---
author: Piotr Hankiewicz
title: Start basic application with Vue.js 2 and Drupal 8
github_issue_number: 1405
tags:
- vue
- drupal
- javascript
- php
- open-source
date: 2018-04-05
---

<img src="/blog/2018/04/start-basic-application-with-vue-drupal/vue-and-drupal.jpg" width="1200" alt="Vue.js 2 and Drupal 8" />

### Introduction

The purpose of creating this post is to show how fast can you build web applications with Vue.js on the front-end and Drupal on the back-end side.

Let’s call our project “Awesome Nerds”.

### What do we need?

* Debian/Ubuntu system
* Internet
* 30 minutes
* Vagrant & VirtualBox
* Git
* Vim
* Yarn

### Step by step

Here’s what we’re going to do:

* Install Vagrant, VirtualBox, and Git
* Setup a new Drupal 8 project that will be our back-end project
* Setup a new Vue.js project that will be our front-end application
* Let’s code

### Install Vagrant, VirtualBox, and Git

Open your console and run:

`$ sudo apt-get install software-properties-common` - getting some common libraries

`$ sudo apt-add-repository ppa:ansible/ansible`

`$ sudo apt-get update`

`$ sudo apt-get install ansible` - installing Ansible

`$ wget ‘https://releases.hashicorp.com/vagrant/2.0.2/vagrant_2.0.2_x86_64.deb’ && dpkg -i vagrant_2.0.2_x86_64.deb` - installing Vagrant

`$ sudo apt-get install dkms`

`$ deb https://download.virtualbox.org/virtualbox/debian <mydist> contrib`

`$ wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -`

`$ wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -`

`$ sudo apt-get update`

`$ sudo apt-get install virtualbox-5.2 git vim nfs-kernel-server` - installing VirtualBox

`$ vagrant plugin install vagrant-vbguest`

`$ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -`

`$ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list`

`$ sudo apt-get update && sudo apt-get install yarn` - installing Yarn

Now we can continue to the back-end project installation.

### Install and setup back-end project

Create a new folder for the project:

`$ mkdir awesome_nerds && cd awesome_nerds`

`$ mkdir frontend backend`

We need to clone the DrupalVM repository. DrupalVM is a Drupal setup that helps to encapsulate services with Vagrant. Run:

`$ cd backend`

`$ git clone git@github.com:geerlingguy/drupal-vm.git .`

Let’s name our project:

`$ vim default.config.yml`

Look and set these two settings so they look like this:

```
vagrant_hostname: awesomenerds.backend                                   
vagrant_machine_name: awesomenerds_backend
```

Quit Vim and run:

`$ vagrant up`

It will take a while to set up everything, you can get a coffee or browse some memes or go to the next chapter and start creating our front-end project.

When it’s ready we will have a running Drupal 8 setup with MySQL, PHP 7, and Apache (you can configure this stack in `default.config.yml` if you prefer nginx for example).

Drupal project files are in the `drupal` directory and that’s the only folder that you would want to add to a project Git repository.

### Setup new Vue.js project

We will use a minimal project skeleton from https://github.com/vuejs-templates/webpack.

Run:

`$ cd awesome_nerds/frontend`

`$ git clone https://github.com/vuejs-templates/webpack .`

`$ yarn install -g vue-cli`

`$ vue init webpack awesome_nerds`

Name the project “awesome_nerds” (yes!) and just hit enter to install with defaults.

When you run:

`$ yarn run dev`

you will get a fresh Vue.js application running on http://localhost:8080.

### Let’s code!

Now we are ready for development. It can be really rapid, both Vue.js 2 and Drupal 8 are impressively good and it’s just a matter of finding a good idea for your new start-up.

In my next post I will continue and code a simple social application using the REST API of Drupal and our Vue.js front-end.

Thank you and good luck!
